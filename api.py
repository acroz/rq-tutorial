from flask import Flask, request, abort, jsonify
from redis import Redis
from rq import Queue

from tasks import work


app = Flask(__name__)

queue = Queue(connection=Redis())


@app.route('/multiply', methods=['POST'])
def submit():
    try:
        value = request.get_json(force=True)['value']
    except KeyError:
        abort(400)  # Bad Request
    job = queue.enqueue(work, value)
    return jsonify({'job_id': job.id}), 201


@app.route('/multiply/<job_id>')
def get_result(job_id):
    job = queue.fetch_job(job_id)
    if job is None or job.result is None:
        abort(404)  # Not found
    return jsonify({'result': job.result})


if __name__ == '__main__':
    app.run(debug=True)
