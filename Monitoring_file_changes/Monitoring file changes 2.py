import time
import requests
import json
import re

pattern1 = re.compile(r"Connection received from (\d+\.\d+\.\d+\.\d+)")
pattern2 = re.compile(r"\d+/\d+/\d+ \d+:\d+ Client (\d+\.\d+\.\d+\.\d+) disconnected")

url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}
log_file = open("../Log_file.txt", "r")  # объект файла, режим чтения
log_file.seek(0, 2)  # перевод указателя чтения/записи в конец файла
while True:
    line = log_file.readline()  # чтение всех строк
    if not line:
        time.sleep(0.1)  # Сон в 3 секунды
        continue
    else:
        temp = line[18:]  # часть строки, определяющая содержание
        temp = temp.strip()  # удалить перенос в конце строки
        if pattern1.match(line) or pattern2.match(line):
            param = {'data': line}  # данные - в словарь
            # Отправка POST-запроса на указанный URL:
            resp = requests.post(url, json=param, headers=headers)
            # Распаковка JSON-ответа от сервера:
            res = json.loads(resp.text)
            # печать ответа
            print(res['data'])
