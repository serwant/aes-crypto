from flask import Flask, request, jsonify

app = Flask(__name__)

serv_file = "/home/sergario/aes-crypto/serv_file.txt"
@app.route('/post', methods=['POST'])
def parse_request():
    temp = request.get_json() # Считывает данные из тела запроса (тип - dict)
    data = (temp['data'])  # Извлекает данные из JSON-данных
    # открыть файл в режиме чтения:
    f = open(serv_file, 'a')
    f.write(data)
    f.close()
    return jsonify({'data': 'Ok'}) # Отправляет JSON-данные в ответ


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
#    app.run(debug=True)

