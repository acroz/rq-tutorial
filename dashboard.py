import uuid

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from rq import Queue
from redis import Redis

from tasks import work_and_save
import db


queue = Queue(connection=Redis())

app = dash.Dash()


app.layout = html.Div(
    [
        html.H1('Task Queue'),
        html.Button('Submit Job', id='submit'),
        html.Ul(id='submissions'),
        dcc.Interval(id='interval', interval=500),  # 500ms
        html.Div(id='empty')
    ]
)


@app.callback(
    Output('empty', 'children'),
    [Input('submit', 'n_clicks')]
)
def submit_job(n_clicks):
    if n_clicks is not None:
        job_id = str(uuid.uuid4())
        db.create_job(job_id, 'queued', 3)
        queue.enqueue(work_and_save, job_id)
    return []


@app.callback(
    Output('submissions', 'children'),
    [Input('interval', 'n_intervals')]
)
def handle_jobs(n_intervals):
    children = []
    for job in db.list_jobs():
        item = html.Li(
            f'id: {job.job_id}, status: {job.status}, '
            f'input: {job.input}, output: {job.output}'
        )
        children.append(item)
    return children


if __name__ == '__main__':
    app.run_server(debug=True)
