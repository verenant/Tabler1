from uploader import upload
import os
# пройтись по всем файлам,где можно брать с json и отправлять в функцию upload

#Единичная загрузка ресторана
upload("frou-frou.json")

#Общая выгрузка
files = os.listdir("Jsons")
for file in files:
    print(upload(file))
