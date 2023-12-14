from hashlib import md5
import requests
import base64
import json
import getpass

url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}

password = getpass.getpass("Введите пароль для шифрования: ")
print('Read: ', password)
password = password.encode()
iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
key = md5(password).hexdigest().encode()
print('Key: ',key)
encoded_key = base64.b64encode(key).decode('utf-8')
print('Encoded_key: ',encoded_key)
data = input("Введите данные для шифрования: ")
print('Data: ',data)
param = {'key': encoded_key, 'data': data, 'act': 'encod'}
resp = requests.post(url, json=param, headers=headers)
res = json.loads(resp.text)
print(res)
data = res['encoded_data']
f = open('Encod_Data.txt', 'w')
f.write(data)
f.close()
