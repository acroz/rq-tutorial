from rq import Queue
from redis import Redis

from tasks import work


queue = Queue(connection=Redis())
queue.enqueue(work, 5)
