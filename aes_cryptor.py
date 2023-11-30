import pyAesCrypt
import os

file = "/dev/shm/text"
en_file = "/home/sergario/Python_projects/text.crp"

# функция шифрования файла
def encryption(file, password):
    # задаём размер буфера
    buffer_size = 512 * 1024
    # вызываем метод шифрования
    if os.path.exists(file):
        try:
            pyAesCrypt.encryptFile(
            str(file),
            str(en_file)
            ,password, buffer_size)
            # вывод на печать имени зашифрованного файла
            print("[Файл '" + str(os.path.splitext(file)[0]) + "' зашифрован]")
            # удаляем исходный файл
            os.remove(file)
        except Exception as e:
            print("Произошла ошибка:", e)
    else:
        print("Файл не существует:", file)

# функция дешифровки файла
def decryption(en_file, password):
    # задаём размер буфера
    buffer_size = 512 * 1024
    if os.path.exists(en_file):
        try:
            # вызываем метод расшифровки
            pyAesCrypt.decryptFile(
            str(en_file),
            str(os.path.splitext(file)[0]),
            password,
            buffer_size
            )
            print("[Файл '" + str(os.path.splitext(file)[0]) + "' дешифрован]")
        except Exception as e:
            print("Произошла ошибка:", e)
    else:
        print("Файл не существует:", en_file)

print("e - encoding file\nd - decoding file\n")
menu = input("Select an action: ")
match menu:
    case 'e':
        password = input("Введите пароль для шифрования: ")
        # вызов функции шифрования файла
        encryption(file, password)
    case 'd':
        password = input("Введите пароль для дешифровки: ")
        # вызов функции дешифровки файла
        decryption(en_file, password)




