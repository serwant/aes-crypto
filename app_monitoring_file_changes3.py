from flask import Flask, request, jsonify
import sqlite3
from threading import Lock

app = Flask(__name__)
# Устанавливаем соединение с базой данных
connection = sqlite3.connect("BaseLog2.db", check_same_thread=False)
cursor = connection.cursor()
lock = Lock()

# Создание таблицы Users
# 'cursor.execute' создает объект "курсор" для выполнения SQL-запросов и операций с базой данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Log (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL
    )
    ''')
# Сохранениее изменений и закрытие соединения
connection.commit()
#connection.close()

@app.route('/post', methods=['POST'])
def parse_request():
    temp = request.get_json() # Считывает данные из тела запроса (тип - dict)
    # Извлекает данные из JSON-данных и передает объекту класса LogBase
    content = temp['data']
    data_to_insert = content
    insert_data(data_to_insert)
    print('Record was successfully added')
    return jsonify({'data': 'Record was successfully added'}) # Отправляет JSON-данные в ответ

# функция для выполнения запроса
def insert_data(data):
    with lock:
        cursor.execute('INSERT INTO Log (content) VALUES (?)', (data,))
        connection.commit()
#        connection.close()

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)