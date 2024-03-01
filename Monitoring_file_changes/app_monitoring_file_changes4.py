from flask import Flask, request, jsonify
import json
import datetime as dt
import sqlite3
from threading import Lock

app = Flask(__name__)
# Устанавливаем соединение с базой данных
connection = sqlite3.connect("BaseLog2.db", check_same_thread=False)
cursor = connection.cursor()
#
lock = Lock()

# Создание таблицы Log
# 'cursor.execute' создает объект "курсор" для выполнения SQL-запросов и операций с базой данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Log (
    id INTEGER PRIMARY KEY,
    time_of_write STRING, 
    content TEXT NOT NULL
    )
    ''')
# Сохранениее изменений
connection.commit()
''' получает запрос на запись данных от клиента , передает эти данные
 функции "insert_data" для записи в базу BaseLog2.db '''


# Получение данных от клиента и запись в базу данных, если данные соответствуют требованиям
@app.route('/post', methods=['POST'])
def parse_request():
    temp = request.get_json()  # Считывает данные из тела запроса (тип - dict)
    content = temp['data']  # Извлекает данные из JSON-данных
    time_of_write = dt.datetime.now()  # получение текущего времени
    time_of_write_str = time_of_write.strftime('%d/%m/%y %H:%M:%S')  # Формат "Time" - в "String"
    insert_data(time_of_write_str, content)
    print('Record was successfully added')
    return jsonify({'data': 'Record was successfully added'})  # Отправляет JSON-данные в ответ


# функция получения запроса на выборку данных из таблицы
@app.route('/Query_Data', methods=['POST'])
def get_request():
    temp = request.get_json()  # Считывает данные из тела запроса (тип - dict)
#    menu_act = temp.get('menu_act')  # Извлекает данные из JSON-данных
    menu_act = temp['menu_act']  # Извлекает из JSON-данных номер запроса
    row_name = data = str()
    # условие получения запроса на выборку данных по определенному столбцу
    if menu_act == '1':
        print('menu_act: ', menu_act)
        row_name = temp['row_name']
        if row_name in ('id', 'time_of_write', 'content'):
            data = query_row_name(row_name)
        else:
            data = {'data': 'Название столбца не корректно. Введите корректные данные.'}
    # условие получения запроса на выборку данных по диапазону времени
    elif menu_act == '2':
        print('act: ', menu_act)
        start_str = temp['start_time']  # Извлекает data1 из JSON-данных
        end_str = temp['end_time']  # Извлекает data2 из JSON-данных
        if start_str and end_str:
            data = query_range(row_name, start_str, end_str)
        else:
            data = {'data': 'Запрос выборки по времени не корректен. Введите корректные данные.'}
    # условие получения запроса на выборку всех данных
    elif menu_act == '3':
        row_name = temp['row_name']
        if row_name == '':
            data = query_all()
    else:
        data = {'data': 'Запрос не корректен. Введите корректные данные.'}
    return jsonify(data)


#  функция для выполнения запроса на выборку столбца данных
def query_row_name(row_name='*', start_date=False, end_date=False) -> list:
    # def query_row_name(row_name) -> list:
    with lock:
        print(row_name)
        cursor.execute(f"SELECT {row_name} FROM Log")
        data = cursor.fetchall()
        return data


# функция для выполнения запроса на выборку данных по диапазону времени
def query_range(row_name='*', start_str='*', end_str='*'):
    with lock:
        print(start_str, end_str)
        cursor.execute("SELECT * FROM Log WHERE time_of_write  BETWEEN ? AND ?",
                       (start_str, end_str))
        data = cursor.fetchall()
        print('Data: ', data)
        jdata = json.dumps(data)
        print('Jdata: ', jdata)
        return jdata


# функция для выполнения запроса всех данных из базы
def query_all():
    with lock:
        cursor.execute("SELECT * FROM Log")
        data = cursor.fetchall()
        print('Data: ', data)
        jdata = json.dumps(data)
        print('Jdata: ', jdata)
        return jdata


# функция для выполнения запроса на запись в базу
def insert_data(time, data):
    with lock:
        cursor.execute('INSERT INTO Log (time_of_write,content) VALUES (?,?)', (time, data,))
        connection.commit()
    return


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
