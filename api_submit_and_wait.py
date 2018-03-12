import time
import requests


post_response = requests.post(
    'http://localhost:5000/multiply',
    json={'value': 3}
)

print('POST response:')
print(f'Status code: {post_response.status_code}')
print('Body:')
print(post_response.text)

job_id = post_response.json()['job_id']

get_response = requests.get(f'http://localhost:5000/multiply/{job_id}')

while get_response.status_code == 404:
    print('No result yet..')
    time.sleep(0.2)
    get_response = requests.get(f'http://localhost:5000/multiply/{job_id}')

print('GET response:')
print(f'Status code: {get_response.status_code}')
print('Body:')
print(get_response.text)

result = get_response.json()['result']
print(f'Result: {result}')
