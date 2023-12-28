from hashlib import md5
import requests
import base64
import json
import getpass
import os

en_file = "/home/sergario/aes-crypto/Encod_Data.txt"
url = 'http://127.0.0.1:8000/decode'
# данные в виде словаря:
headers = {'Content-Type': 'application/json'}
# запрос у пользователя ввод пароля, скрывая введенные символы:
password = getpass.getpass("Введите пароль для дешифрования: ")
# преобразование в байты:
password = password.encode()
# вектор инициализации для дешифрования:
iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
# Генерация ключа для дешифрования, применяя MD5-хеш к паролю и преобразуя результат в байты:
key = md5(password).hexdigest().encode()
# Кодирование ключа в формат base64 для отправки на сервер:
encoded_key = base64.b64encode(key).decode('utf-8')
# Если закодированный файл существует:
if os.path.exists(en_file):
    try:
        # открыть файл в режиме чтения:
        f = open(en_file, 'r')
        data = f.read()
        f.close()
    except Exception as e:
        print("Произошла ошибка:", e)
else:
    print("Файл не существует:", en_file)
# Формирование словаря параметров для отправки запроса на сервер:
param = {'key': encoded_key, 'data': data, 'act': 'decod'}
# Отправка POST-запроса на указанный URL:
resp = requests.post(url, json=param, headers=headers)
# Распаковка JSON-ответа от сервера:
res = json.loads(resp.text)
print(res)