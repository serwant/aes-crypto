from hashlib import md5
import requests
import base64
import json
url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}
password = input("Введите пароль для шифрования: ")
password = password.encode()
iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
key = md5(password).hexdigest().encode()
encoded_key = base64.b64encode(key).decode('utf-8')
print(key)
data = input("Введите данные для шифрования: ")
param = {'key': encoded_key, 'data': data}
resp = requests.post(url, json=param, headers=headers)
res = json.loads(resp.text)
print(res)


