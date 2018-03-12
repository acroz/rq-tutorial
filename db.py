import sqlalchemy
import os
import sys
from collections import namedtuple


ENGINE = sqlalchemy.create_engine('sqlite:///jobs.db')

Job = namedtuple('Job', ['job_id', 'status', 'input', 'output'])


def list_jobs():
    jobs = []
    with ENGINE.connect() as conn:
        result = conn.execute('SELECT * FROM jobs')
        for row in result:
            jobs.append(
                Job(row['job_id'], row['status'], row['input'], row['output'])
            )
    return jobs


def get_job(job_id):
    with ENGINE.connect() as conn:
        result = conn.execute(
            'SELECT * FROM jobs WHERE job_id = :job_id',
            job_id=job_id
        )
        row = result.fetchone()
    return Job(row['job_id'], row['status'], row['input'], row['output'])


def create_job(job_id, status, input_):
    with ENGINE.connect() as conn:
        conn.execute(
            """
                INSERT INTO jobs (job_id, status, input)
                VALUES (:job_id, :status, :input_)
            """,
            job_id=job_id, status=status, input_=input_
        )


def set_job_status(job_id, status):
    with ENGINE.connect() as conn:
        conn.execute(
            'UPDATE jobs SET status = :status WHERE job_id = :job_id',
            job_id=job_id, status=status
        )


def set_job_status_and_output(job_id, status, output):
    with ENGINE.connect() as conn:
        conn.execute(
            """
                UPDATE jobs SET status = :status, output = :output
                WHERE job_id = :job_id
            """,
            job_id=job_id, status=status, output=output
        )


def new():
    """Create a new datbase file, removing the old one."""

    try:
        os.remove('jobs.db')
    except FileNotFoundError:
        pass

    with ENGINE.connect() as conn:
        conn.execute("""
            CREATE TABLE jobs (
                job_id text,
                status text,
                input real,
                output real
            )
        """)


if __name__ == '__main__':
    if '--new' in sys.argv:
        new()
