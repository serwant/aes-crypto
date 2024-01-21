from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BaseLog.db'

db = SQLAlchemy(app)

class LogBase(db.Model): # создает форму таблицы базы в объекте LogBase
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(60), nullable=False)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<LogBase %r>' % self.id # к выбираемому объекту додается "id"

# Запуск контекста приложения перед выполнением операций с базой данных
# with app.app_context():
#     db.create_all()

@app.route('/post', methods=['POST'])
def parse_request():
    temp = request.get_json() # Считывает данные из тела запроса (тип - dict)
    # Извлекает данные из JSON-данных и передает объекту класса LogBase
    content = LogBase(temp['data'])
    db.session.add(content) # добавляет данные в базу
    db.session.commit() # сохраняет обновленные данные
    print('Record was successfully added')
    return jsonify({'data': 'Record was successfully added'}) # Отправляет JSON-данные в ответ


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
