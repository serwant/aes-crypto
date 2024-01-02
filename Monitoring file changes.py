import datetime as dt
import time
#dt_start = dt.datetime.now().strftime('%d/%m/%Y %H:%M')
dt_start = dt.datetime.now()
print(dt_start)

log_file = open("Log_file.txt", "r")  # объект файла, режим чтения

while True:
    line = log_file.readline()  # чтение всех строк
    if not line:
         time.sleep(3)  # Сон в 3 секунды
         continue
    temp = line[:15] # часть строки, определяющая дату
    current_time = dt.datetime.strptime(temp, '%d/%m/%Y %H:%M')  # строка - в формат "Time"
    if (dt_start < current_time): print(line) # если появилась свежая запись