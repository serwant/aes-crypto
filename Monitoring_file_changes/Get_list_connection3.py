import requests
import json
import re

url = 'http://127.0.0.1:8000/Query_Data'
# данные в виде словаря
headers = {'Content-Type': 'application/json'}


# Отправка запроса на сервер, получение ответа
# Выборка данных по определенному запросу


def trans_request(param):
    # Отправка POST-запроса на указанный URL:
    resp = requests.post(url, json=param, headers=headers)
    # Распаковка JSON-ответа от сервера:
    res = json.loads(resp.text)
    # печать ответа
    print(res)


# Отправка запроса на сервер, получение ответа

menu = input("Сделайте выбор:\n1 - Название столбца (выборка данных по названию столбца)\n"
             "2 - Временной диапазон (выборка по начальной и конечной дате)\n"
             "3 - Все данные\n")
match menu:
    case '1':
        query_data = input("Введите название требуемого столбца: ")
        if query_data in {'id', 'time_of_write', 'content'}:
            param = {'menu_act': '1', 'row_name': query_data, 'start_time': '', 'end_time': ''}  # данные - в словарь
            trans_request(param)
        else:
            print("Такого названия не существует, введите корректные данные")
    case '2':
        print('Выборка по начальной и конечной дате (формат: 21/10/24 17:30:45)')
        start_data = input("Введите начальные дату и время: ")
#        start_data = '01/02/24 08:00:00'
        pattern1 = re.fullmatch(r"[0-3]\d/\d{2}/\d{2} [02]\d:\d{2}:\d{2}", start_data)
        if pattern1:
            print(start_data)
            end_data = input("Введите конечные дату и время: ")
            pattern2 = re.fullmatch(r"[0-3]\d/\d{2}/\d{2} [02]\d:\d{2}:\d{2}", end_data)
            print(end_data)
            if pattern2:
                param = {'menu_act': '2', 'row_name': '', 'start_time': start_data, 'end_time': end_data}  # данные - в словарь
                trans_request(param)
            else:
                print('Конечная дата-время введена некорректно. Введите корректные данные')
        else:
            print('Начальная дата-время введена некорректно. Введите корректные данные')
    case '3':
        query_data = input('Для выборки всех данных нажмите "ENTER"')
        if query_data == '':
            param = {'menu_act': '3', 'row_name': '', 'start_time': '', 'end_time': ''}  # данные - в словарь
            trans_request(param)
        else:
            print('Неверные данные. Для выборки всех данных нажмите "ENTER"')
