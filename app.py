from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def parse_request():
    temp = request.get_json() # Считывает данные из тела запроса (тип - dict)
    iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'  # Инициализирует вектор инициализации для шифрования
    key = (temp['key'])  # Извлекает зашифрованный ключ из JSON-данных
    decoded_key = base64.b64decode(key)  # Декодирует ключ из base64
    data = (temp['data'])  # Извлекает зашифрованные данные из JSON-данных
    data = data.encode()  # Кодирует данные в байты
    act = (temp['act'])  # Извлекает маркер ввыбора действия из JSON-данных
    cipher = Cipher(algorithms.AES(decoded_key), modes.CBC(iv))  # Создает объект шифра с использованием ключа и вектора инициализации
    if act == 'encod':
        # Шифрование
        print('Encoding')
        encryptor = cipher.encryptor()  # Создает объект шифратора
        padder = padding.PKCS7(128).padder()  # Создает объект дополнителя для дополнения данных до размера блока
        padded_data = padder.update(data) + padder.finalize()  # Дополняет данные и сохраняет результат
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()  # Шифрует данные и сохраняет результат
        encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')  # Кодирует зашифрованные данные в base64
        return jsonify({'encoded_data': encoded_ciphertext}) # Отправляет JSON-данные в ответ

    elif act == 'decod':
        # Дешифрование
        print('Decoding')
        ciphertext = base64.b64decode(data)  # Декодирует зашифрованные данные из base64
        decryptor = cipher.decryptor()  # Создает объект дешифратора
        unpadder = padding.PKCS7(128).unpadder()  # Создает объект дешифратора
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()  # Дешифрует данные и сохраняет результат
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()  # Удаляет дополнение и сохраняет результат
        unpadded_data = unpadded_data.decode()  # Декодирует данные в строку
        # Результат в переменной data
#        param = json.dumps({'decoded_data': unpadded_data})  # Подготавливает JSON-данные для ответа
#        self.wfile.write(param.encode())  # Отправляет JSON-данные в ответ
        param = {'decoded_data': unpadded_data}
#        param = param.encode()
        print('param: ', param)
        return jsonify(param)
#    res = somedict['key']


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
#    app.run(debug=True)

