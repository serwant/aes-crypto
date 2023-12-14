from hashlib import md5
import requests
import base64
import json
import getpass
import os

en_file = "/home/sergario/aes-crypto/Encod_Data.txt"
url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}
password = getpass.getpass("Введите пароль для дешифрования: ")
print('Pass: ', password)
password = password.encode()
iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
key = md5(password).hexdigest().encode()
print('Key: ', key)
encoded_key = base64.b64encode(key).decode('utf-8')
print("Encoded key", encoded_key)
if os.path.exists(en_file):
    try:
        f = open(en_file, 'r')
        data = f.read()
        f.close()
    except Exception as e:
        print("Произошла ошибка:", e)
else:
    print("Файл не существует:", en_file)
param = {'key': encoded_key, 'data': data, 'act': 'decod'}
resp = requests.post(url, json=param, headers=headers)
res = json.loads(resp.text)
print(res)