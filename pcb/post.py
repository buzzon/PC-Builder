import requests


r = requests.post('http://127.0.0.1:8000/api/core/getToken/', json={"username": "qwer", "password": "qwer"})
print(r.status_code)
print(r.json())
mytoken = r.json()['token']
print(mytoken)


r = requests.post('http://127.0.0.1:8000/api/core/Brand/', json={"title": "12"},
                  headers={'Authorization': f'Token {mytoken}'})
print(r.status_code)
print(r.json())





