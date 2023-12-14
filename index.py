from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import json
import base64
class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        self._set_headers() # Устанавливает HTTP-заголовки для ответа
        self.send_response(200) # Отправляет успешный HTTP-ответ
        self.send_header("Content-type", "application/json") # Устанавливает тип содержимого в ответе
        iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c' # Инициализирует вектор инициализации для шифрования
        content_length = int(self.headers['Content-Length']) # Получает длину тела POST-запроса
        post_data = self.rfile.read(content_length)  # Считывает данные из тела запроса (тип - string)
        temp = json.loads(post_data) # Декодирует JSON-данные из тела запроса
        key = (temp['key']) # Извлекает зашифрованный ключ из JSON-данных
        decoded_key = base64.b64decode(key) # Декодирует ключ из base64
        data = (temp['data'])  # Извлекает зашифрованные данные из JSON-данных
        data = data.encode() # Кодирует данные в байты
        act = (temp['act']) # Извлекает маркер ввыбора действия из JSON-данных
        cipher = Cipher(algorithms.AES(decoded_key), modes.CBC(iv)) # Создает объект шифра с использованием ключа и вектора инициализации
        if act == 'encod':
            # Шифрование
            print('Encoding')
            encryptor = cipher.encryptor() # Создает объект шифратора
            padder = padding.PKCS7(128).padder() # Создает объект дополнителя для дополнения данных до размера блока
            padded_data = padder.update(data) + padder.finalize() # Дополняет данные и сохраняет результат
            ciphertext = encryptor.update(padded_data) + encryptor.finalize() # Шифрует данные и сохраняет результат
            encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8') # Кодирует зашифрованные данные в base64
            param = json.dumps({'encoded_data': encoded_ciphertext}) # Подготавливает JSON-данные для ответа
            self.wfile.write(param.encode()) # Отправляет JSON-данные в ответ

        elif act == 'decod':
            # Дешифрование
            print('Decoding')
            ciphertext = base64.b64decode(data) # Декодирует зашифрованные данные из base64
            decryptor = cipher.decryptor() # Создает объект дешифратора
            unpadder = padding.PKCS7(128).unpadder() # Создает объект дешифратора
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize() # Дешифрует данные и сохраняет результат
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize() # Удаляет дополнение и сохраняет результат
            unpadded_data = unpadded_data.decode() # Декодирует данные в строку
             # Результат в переменной data
            param = json.dumps({'decoded_data': unpadded_data}) # Подготавливает JSON-данные для ответа
            self.wfile.write(param.encode())  # Отправляет JSON-данные в ответ
def run(addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = HTTPServer(server_address, S)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

run()