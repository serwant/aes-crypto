import requests
import json
import re

url1 = 'http://127.0.0.1:8000/Query_Data'
url2 = 'http://127.0.0.1:8000/Query_DataTime'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}


# Отправка запроса на сервер, получение ответа
# Выборка данных по определенному столбцу, либо вся таблица
def trans_request1(param):
    # Отправка POST-запроса на указанный URL:
    resp = requests.post(url1, json=param, headers=headers)
    # Распаковка JSON-ответа от сервера:
    res = json.loads(resp.text)
    # печать ответа
    print(res)


# Отправка запроса на сервер, получение ответа
# Выборка данных по определенному диапазону времени
def trans_request2(param):
    # Отправка POST-запроса на указанный URL:
    resp = requests.post(url2, json=param, headers=headers)
    # Распаковка JSON-ответа от сервера:
    res = json.loads(resp.text)
    # печать ответа
    print(res)


menu = input("Сделайте выбор:\n1 - Название столбца (выборка данных по названию столбца)\n"
             "2 - Временной диапазон (выборка по начальной и конечной дате)\n"
             "3 - Все данные\n")
match menu:
    case '1':
        query_data = input("Введите название требуемого столбца: ")
        if query_data in {'id', 'time_of_write', 'content'}:
            param = {'data': query_data}  # данные - в словарь
            trans_request1(param)
        else:
            print("Такого названия не существует, введите корректные данные")
    case '2':
        print('Выборка по начальной и конечной дате (формат: 21/10/24 17:30:45)')
        start_data = input("Введите начальные дату и время: ")
#        start_data = '01/02/24 08:00:00'
        print(start_data)
        pattern1 = re.fullmatch(r"[0-3]\d/\d{2}/\d{2} [02]\d:\d{2}:\d{2}", start_data)
        if pattern1:
            end_data = input("Введите конечные дату и время: ")
            print(end_data)
            pattern2 = re.fullmatch(r"[0-3]\d/\d{2}/\d{2} [02]\d:\d{2}:\d{2}", end_data)
            if pattern2:
                param = {'data1': start_data, 'data2': end_data}  # данные - в словарь
                trans_request2(param)
            else:
                print('Конечная дата-время введена некорректно. Введите корректные данные')
        else:
            print('Начальная дата-время введена некорректно. Введите корректные данные')
    case '3':
        query_data = input('Для выборки всех данных нажмите "ENTER"')
        if query_data == '':
            param = {'data': query_data}  # данные - в словарь
            trans_request1(param)
        else:
            print('Неверные данные. Для выборки всех данных нажмите "ENTER"')
