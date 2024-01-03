import datetime as dt
import time
import requests
import json

url = 'http://127.0.0.1:8000/post'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}
#dt_start = dt.datetime.now().strftime('%d/%m/%Y %H:%M')
dt_start = dt.datetime.now()
print(dt_start)
log_file = open("Log_file.txt", "r")  # объект файла, режим чтения
while True:
    line = log_file.readline()  # чтение всех строк
    if not line:
         time.sleep(3)  # Сон в 3 секунды
         continue
    else:
        temp = line[:15] # часть строки, определяющая дату
        current_time = dt.datetime.strptime(temp, '%d/%m/%Y %H:%M')  # строка - в формат "Time"
        if (dt_start < current_time):
            param = {'data': line} # данные - в словарь
            # Отправка POST-запроса на указанный URL:
            resp = requests.post(url, json=param, headers=headers)
            # Распаковка JSON-ответа от сервера:
            res = json.loads(resp.text)
            # печать ответа
            print(res['data'])