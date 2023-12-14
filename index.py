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
        self._set_headers()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        iv = b'\x8d\xae\xbae\xc9l_%\xa5j\xe5\x91R\\F\x0c'
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Decode bytes to string
        print(post_data)
        temp = json.loads(post_data)
        key = (temp['key'])
        print('Key: ', key)
        decoded_key = base64.b64decode(key)
        print("Decoded key: ", decoded_key)
        data = (temp['data'])
        data = data.encode()
        print("Data: ",data)
        act = (temp['act'])
        print(act)
        cipher = Cipher(algorithms.AES(decoded_key), modes.CBC(iv))
        if act == 'encod':
            # Шифрование
            print('Encoding:')
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
            print(encoded_ciphertext)
            param = json.dumps({'encoded_data': encoded_ciphertext})
            print(param)
            self.wfile.write(param.encode())

        elif act == 'decod':
            # Дешифрование
            print('Decoding:')
            ciphertext = base64.b64decode(data)
            print(ciphertext)
            decryptor = cipher.decryptor()
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
            print(unpadded_data)  # Вывод: b'Секретное сообщение'
            unpadded_data = unpadded_data.decode()
             # Результат в переменной data
            param = json.dumps({'decoded_data': unpadded_data})
            print('Param: ',param)
            self.wfile.write(param.encode())
def run(addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = HTTPServer(server_address, S)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

run()