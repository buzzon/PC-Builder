import requests


r = requests.post('http://127.0.0.1:8000/api/core/getToken/', json={"username": "qwer1", "password": "qwer1"})
print(r.status_code)
print(r.json())
mytoken = r.json()['token']
print(mytoken)


