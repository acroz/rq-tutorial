import time
from redis import Redis
from rq import Queue

from tasks import work


q = Queue(connection=Redis())

job = q.enqueue(work, 4)

while job.result is None:
    print('No result yet..')
    time.sleep(0.2)

print(f'Result: {job.result}')
