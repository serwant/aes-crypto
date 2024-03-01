from flask import Flask, request, jsonify
from datetime import datetime
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
    time_of_write DATE, 
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
    time_of_write = datetime.now()  # получение текущего времени
    print(time_of_write)
    insert_data(time_of_write, content)
    print('Record was successfully added')
    return jsonify({'data': 'Record was successfully added'})  # Отправляет JSON-данные в ответ


# функция получения запроса на выборку данных из таблицы
@app.route('/Query_Data', methods=['POST'])
def get_request():
    temp = request.get_json()  # Считывает данные из тела запроса (тип - dict)
    row_names = temp['row_names']  # Извлекает row_names из JSON-данных
    start_data_str = temp['start_time']  # Извлекает start_time из JSON-данных
    end_data_str = temp['end_time']  # Извлекает end_time из JSON-данных
    data = query(row_names, start_data_str, end_data_str)
    return jsonify(data)


# функция запроса на выборку данных
def query(row_names: list, start_data_str, end_data_str):
    base_sql = "SELECT {} FROM Log {}"  # базовый SQL-запрос
    row_names_str = ''
    result = []
    if not row_names:  # если название столбцов в запросе отсутствуют
        row_names_str = '*'
    else:
        row_names_lst = []
        for row_name in row_names:  # цикл создания  запрашиваемых столбцов в виде списка
            if row_name in {'id', 'time_of_write', 'content'}:
                row_names_lst.append(row_name)
            else:
                result = ['Такого столбца не существует, введите корректные данные']
                return result
            row_names_str = ','.join(row_names_lst)  # преобразование списка запрашиваемых столбцов в строку
    if start_data_str or end_data_str:  # если в запросе имеется интервал времени
        try:
            # проверка запрашиваемого времени start_data на корректность
            start_data = datetime.strptime(start_data_str, "%Y-%m-%d %H:%M:%S")  # Форат "String" - в "Time"
        except ValueError:
            result = ['Начальная дата введена некорректно. Введите корректные данные']
        else:
            if start_data:
                print(start_data)
                try:
                    # проверка запрашиваемого времени end_data на корректность
                    end_data = datetime.strptime(end_data_str, "%Y-%m-%d %H:%M:%S")  # Форат "String" - в "Time"
                except ValueError:
                    result = ['Конечная дата введена некорректно. Введите корректные данные']
                else:  # если start_data и end_data корректны
                    if end_data:
                        print(end_data)
                        where_filters = 'WHERE time_of_write  BETWEEN ? AND ?'
                        sql_prepared_parameters = (start_data, end_data)  # переменные к запросу выборки по времени
                        print(row_names_str)
                        final_sql = base_sql.format(row_names_str, where_filters)
                        print(final_sql)
                        cursor.execute(final_sql, sql_prepared_parameters)
                        result = cursor.fetchall()
    else:  # если в запросе отсутствуют какие-либо данные
        where_filters = ''
        final_sql = base_sql.format(row_names_str, where_filters)
        cursor.execute(final_sql)
        result = cursor.fetchall()
    return result


# функция для выполнения запроса на запись в базу
def insert_data(time_of_write, content):
    with lock:
        cursor.execute('INSERT INTO Log (time_of_write,content) VALUES (?,?)', (time_of_write, content,))
        connection.commit()
    return


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
