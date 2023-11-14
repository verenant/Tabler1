from uploader import upload
import os
# пройтись по всем файлам,где можно брать с json и отправлять в функцию upload


upload("vinil-i-vino-1.json")


files = os.listdir("Jsons")
for file in files:
    # оставить от file только latin_name (то есть убрать .json)
    print(upload(file[:-5]))
