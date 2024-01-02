from hashlib import md5
import requests
import base64
import json
import getpass

#url = 'http://127.0.0.1:8000/encode'
url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}
# запрос у пользователя ввод пароля, скрывая введенные символы:
password = getpass.getpass("Введите пароль для шифрования: ")
# преобразование в байты:
password = password.encode()
# вектор инициализации для дешифрования:
iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
# Генерация ключа для дешифрования, применяя MD5-хеш к паролю и преобразуя результат в байты:
key = md5(password).hexdigest().encode()
# Кодирование ключа в формат base64 для отправки на сервер:
encoded_key = base64.b64encode(key).decode('utf-8')
# запрос у пользователя ввод данных:
data = input("Введите данные для шифрования: ")
# Формирование словаря параметров для отправки запроса на сервер:
param = {'key': encoded_key, 'data': data, 'act': 'encod'}
# Отправка POST-запроса на указанный URL:
resp = requests.post(url, json=param, headers=headers)
# Распаковка JSON-ответа от сервера:
res = json.loads(resp.text)
# получение закодированных данных
data = res['encoded_data']
# открытие файла в режиме записи и запись данных в файл
f = open('Encod_Data.txt', 'w')
f.write(data)
f.close()
