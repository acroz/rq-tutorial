import time
import db


def work(value):
    time.sleep(2)
    return value * 2


def work_and_save(job_id):
    db.set_job_status(job_id, 'running')
    job = db.get_job(job_id)

    result = work(job.input)

    db.set_job_status_and_output(job_id, 'done', result)
