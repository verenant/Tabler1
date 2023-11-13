import os

from restraunt import Restraunt

from tablerObject import TablerObject
import json
import re
#import glob
#import httpx
#from collections import OrderedDict
#from PIL import Image
from restraunt import Restraunt
#from urllib import request, parse

username = "verenant@gmail.com"
password = "zrC!qFvI2Q"
token = "Bearer 0r06VbX4NlbG77N3DQ1gEyNv"
headers = {
    'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv',
    "Content-Type": "application/json"
}
postUrl = "https://tabler.ru/api/v1/places"
from tablerObject import TablerObject
import json
import re
import os
import requests
from Category import categories
from Cuisines import cuisines
import httplib2

from collections import OrderedDict



#меняем названия на те, которые на сайте
def changeKithcenName(kitchen):
    if kitchen == "рыба и морепродукты":
        return "Морепродукты"
    elif kitchen == "крафтовое пиво":
        return "Крафт"
    elif kitchen == "шашлыки":
        return "Шашлык"
    elif kitchen == "шаверма":
        return "Шаурма"
    elif kitchen == "боулы":
        return "Боул"
    else:
        return kitchen.capitalize()

def prepareKitchen(kitchens):
    kitchens_array_id = []
    for kitchen in kitchens:
        kitchen = changeKithcenName(kitchen)
        for i in cuisines["cuisines"]:
            if i["name"] == kitchen:
                kitchens_array_id.append(i["id"])
    return kitchens_array_id

#разбиваем адресс на улицу и дом, есть адресса без дома
def prepareAddress(address):
    address = address.split("\xa0")
    return address
# def prepareAddress(address):
#     street = address
#     building = ""
#     list = ["0","1","2","3","4","5","6","7","8","9"]
#     while street[-1] in list:
#         building += street[-1]
#         street = street[:-1]
#     return street, building[::-1]
#Делаем из описания короткое
def prepareShortDescription(description):
    short_description = description.split(".", 1)
    short_description = short_description[0].split("                ")
    return short_description[0] + "."

def prepareDescription(description):
    description = description.split("                ")
    return description[1]

def prepareFeatures(fts):
    dictFts = {}

    dictFts["wifi"] = True
    dictFts["cashfree"] = True
    dictFts["terrace"] = False
    dictFts["mobileCharge"] = True
    dictFts["smokeZone"] = 2

    dictFts["hookah"] = True if ("кальян" in fts) else False
    dictFts["karaoke"] = True if ("караоке" in fts) else False
    dictFts["delivery"] = True if ("доставка" in fts) else False
    dictFts["businessLunch"] = True if ("бизнес-ланч" in fts) else False
    dictFts["sportTranslations"] = True if ("спортивные трансляции" in fts) else False
    dictFts["childrenRoom"] = True if (("детская комната" in fts) or ("детские мастер-классы" in fts)) else False

    # по алкоголю лучше уточнить перед загрузкой
    dictFts["alcohol"] = True #if ("своя пивоварня" in fts) else False

    dictFts["entertainment"] = 1 if ("кальян" in fts) or ("dj" in fts) or ("стриптиз" in fts) \
                                    or ("боулинг" in fts) or ("бильярд" in fts) or ("настольные игры" in fts) \
                                    or ("кулинарные мастер-классы" in fts)else 0
    dictFts["liveMusic"] = 1 if ("живая музыка" in fts) or ("dj" in fts) else 0
    dictFts["dancefloor"] = 1 if ("здесь танцуют" in fts) else 0
    dictFts["parkingType"] = 2 if ("парковка" in fts) else 0

    return dictFts




#Перевод координат в float
def prepareCoord(x):
    return float(x)

def prepareCheck(check):
    if isinstance(check,int):
        return check
    if check == "no_avg_check" or check =="":
        return ""
    pos = check.index(" ")
    if pos < 0:
        return int(check)
    return int(check[:pos])

def prepareSchedule(timetable):
    weekDays = [ "Пн","Вт","Ср", "Чт", "Пт","Сб", "Вс"]
    # Позиции букв
    daysPositions =[]
    # Время внутри букв
    scheduletime = []
    # Подготовка расписания делаем паттерн БУКВА+буква и ищем позиции букв дней
    pattern= r'[А-Я][а-я]+'
    daysInTimetable = re.findall(pattern, timetable)


    #убираем из списка все случайные совпадение не двух буквенные (Выходной и тп )
    for checkDay in daysInTimetable:
        if len(checkDay) != 2:
            daysInTimetable.remove(checkDay)

    #получение номеров дней в расписании
    weekDaysNumbersInSchedule = [-1,-1,-1,-1,-1,-1,-1]
    i = 0
    k = 0
    for i in range(0,7):
        if weekDays[i] == daysInTimetable[k]:
            k+=1
            weekDaysNumbersInSchedule[i] = weekDays[i]


    for i_day in range(0, len(daysInTimetable)):
        daysPositions.append(timetable.find(daysInTimetable[i_day]))
     # Изменения
    for i in range(1,len(daysPositions)):
        if daysPositions[i]-daysPositions[i-1] <5 :
            daysInTimetable[i] = -1

    for i in range(0,7):
        if weekDaysNumbersInSchedule[i] not in daysInTimetable:
            weekDaysNumbersInSchedule[i] = -1



    # Конец изменений
    # Добавляем конец строки для того чтобы работал сбор времени между разными расписаниями
    daysPositions.append(len(timetable))

    #сбор времени между разными днями версия 1.0
    #for i_day in range(1,len(daysInTimetable),2):
    #    scheduletime.append(timetable[daysPositions[i_day]+3: daysPositions[i_day+1]])

    # сбор времени между разными днями версия 2.0
    daysRanges = []
    for i in range(0,len(daysPositions)-1):
        if daysPositions[i+1]- daysPositions[i] > 4:
            scheduletime.append(timetable[daysPositions[i]+3: daysPositions[i+1]])

    for i_day in scheduletime:
        if i_day == None:
            scheduletime.remove(i_day)


    #расположить данные в словарь между правильными днями
    schedule = {
        "Пн":"",
        "Вт": "",
        "Ср": "",
        "Чт": "",
        "Пт": "",
        "Сб": "",
        "Вс": ""
    }


    k = 0
    for i in range(0,7):
        if isinstance(weekDaysNumbersInSchedule[i],str):
            schedule[weekDaysNumbersInSchedule[i]] = scheduletime[k]
            k+=1
  #  print(schedule)

    for day in schedule:
        if schedule[day] == "":
            prevDay = weekDays[weekDays.index(day)-1]
            schedule[day] = schedule[prevDay]

            pass
           # schedule[i] = schedule[i-1]
        # if weekDaysNumbersInSchedule[i] != -1:
        #     schedule[i][weekDaysNumbersInSchedule[i]] = scheduletime[k]
        #
        # if weekDaysNumbersInSchedule[i] == -1:
        #     schedule[i][weekDaysNumbersInSchedule[i]] = scheduletime[k]
        #
        # if weekDaysNumbersInSchedule[i-1] == -1 and weekDaysNumbersInSchedule[i] != -1:
        #     k=+1
        #     schedule[i][weekDaysNumbersInSchedule[i]] = scheduletime[k]
    schedule_dict = {
      #  "id": " ", "isMain": True, "items" : [
       "isMain": True, "items": [
            #{"dayOfWeek": 1, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 1, "endAt": "",  "startAt": ""},
            #{"dayOfWeek": 2, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 2, "endAt": "",  "startAt": ""},
            # {"dayOfWeek": 3, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 3, "endAt": "", "startAt": ""},
            # {"dayOfWeek": 4, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 4, "endAt": "",  "startAt": ""},
            # {"dayOfWeek": 5, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 5, "endAt": "",  "startAt": ""},
            # {"dayOfWeek": 6, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 6, "endAt": "", "startAt": ""},
            # {"dayOfWeek": 7, "endAt": "", "id": "  ", "startAt": ""},
            {"dayOfWeek": 7, "endAt": "",  "startAt": ""},

        ]
    }
    day = 0
    for i in schedule:
        sd = schedule[i].split(" — ")
        schedule_dict["items"][day]["startAt"] = sd[0][1:]
        schedule_dict["items"][day]["endAt"] = sd[1]
        day += 1
    #schedule_list = list({"isMain":schedule_dict["isMain"]}).append({"items":schedule_dict["items"]})

    # ошибка 500 '{"status":"GeneralInternalError","message":"Произошла ошибка","data":[]}'
    #scheduleList = [{"isMain":schedule_dict["isMain"],"items":json.dumps(schedule_dict["items"])}]

    # 422 '{"status":"SlugAlreadyExist","message":"Слаг занят","data":[]}' # Исправил ошибку во времени работы был пробел перед врменем
    scheduleList = [{"isMain": schedule_dict["isMain"], "items": schedule_dict["items"]}]

   # '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["schedules.items"]}}'
    #scheduleList = [{"isMain": schedule_dict["isMain"], "items": schedule_dict["items"],"name":""}]

     # 400 '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["schedules.isMain"]}}'
    #scheduleList = schedule_dict["items"]

    #400 '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["schedules.isMain"]}}'
    #scheduleList = [[{"isMain": schedule_dict["isMain"], "items": schedule_dict["items"]}]]

    # 400 '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["schedules.isMain"]}}'

    return scheduleList

def getCategoryId(rest):
    restCat = rest.category
    for category in categories:
        if category["name"] == restCat:
            return category["id"]
        rest.subcategory = restCat
        if restCat == "Пекарня":
            return 1
        if restCat== "Банкетный зал":
            return 9
        if restCat== "Паб":
            return 12
        if restCat== "Бургерная":
            return 14
        if restCat== "Кондитерская":
            return 1
        if restCat== "Чайная":
            return 23
        if restCat== "Пиццерия":
            return 9
        if restCat== "Семейный ресторан":
            return 9
        if restCat== "Кафе-мороженое":
            return 1
        if restCat== "Винотека":
            return 14
        if restCat== "Стейк-хаус":
            return 9
        if restCat== "Рюмочная":
            return 12

        if restCat== "Клуб":
            return 13
        if restCat== "Лаунж":
            return 13
        if restCat== "Ресторанный комплекс":
            return 9
        if restCat== "Детское кафе":
            return 1
        if restCat== "Караоке-клуб":
            return 13
        if restCat == "Корабль":
            return 9
        if restCat == "Гастробар":
            return 12
        if restCat == "Корнер":
            return 117


def postRest(rest):
    city_id = 0
    if "/spb/" in rest.additional_url:
        city_id = 8
    if "/msk/" in rest.additional_url:
        city_id = 9

    data = {

            "name": rest.name,  # название
            "latinName": rest.latin_name,
            "lon": rest.lon,  # месторасположение
            "lat": rest.lat,
           # "city": rest.city,
            "street": rest.address[0],  # улица
            "building": rest.address[1],  # дом
            "phone_number": rest.phone, #json.dumps(rest.phone),  # телефоны
            "city_id": city_id, # город
            "category_id": rest.category,
            "subcategory": rest.subcategory
        }

    if data["phone_number"] == "no_phone":
        del data["phone_number"]
    if data["subcategory"] == "":
        del data["subcategory"]

    isExists = requests.get("https://tabler.ru/api/v1/places?response_type=short&query=" + rest.latin_name, headers = headers)
    if isExists.status_code == 404:


        responseCreation = requests.post(postUrl, data=json.dumps(data), headers=headers)
        patchUrl = responseCreation.text

        patchUrl =postUrl+"/"+ patchUrl[patchUrl.find("latinName") + len("latinName") + 3:patchUrl.find("city") - 3]
        # print(patchUrl)
        with open("postRests.txt","a") as fP:
            fP.write(rest.latin_name + "     tabler.ru" + patchUrl[patchUrl.rfind("/"):])
            fP.write("\n")

        responcePatch = patchRest(rest, patchUrl)
        if responcePatch.status_code == 200:
            responsePublish = requests.post(patchUrl+"/moderation-status/published",headers = headers)
            #ошибка 403 недостаточно прав
            return responsePublish
        pass
        return responcePatch

  # основное фото Загрузка основного фото и других изображений


def patchRest(rest,patchUrl):
        avatar_id = postMainImage(rest.latin_name)
        data = {
       # "phones": rest.phone,  # телефоны
        "avatar_id": avatar_id,
        "background_id": avatar_id,
        "average_check": prepareCheck(rest.avg_check),  # средний чек
        "latin_name" : rest.latin_name,   # краткая ссылка
        "description": rest.description,  # описание
        "short_description": prepareShortDescription(rest.description),
        "cuisine_ids": prepareKitchen(rest.kitchen),  # кухни_id
        "subcategory": rest.subcategory,
        # особенности
        "wifi": rest.features["wifi"],
        "cashfree": rest.features["cashfree"],
        "terrace": rest.features["terrace"],
        "alcohol": rest.features["alcohol"],  #  уточнить по поводу заполнения
        "mobile_charge": rest.features["mobileCharge"],
        "smokezone": rest.features["smokeZone"],
        "hookah": rest.features["hookah"],
        "karaoke": rest.features["karaoke"],
        "delivery": rest.features["delivery"],
        "business_lunch": rest.features["businessLunch"],
        "sport_translations": rest.features["sportTranslations"],
        "entertainment": rest.features["entertainment"],
        "liveMusic": rest.features["liveMusic"],
        "dancefloor": rest.features["dancefloor"],
      #  "parkingType": rest.features["parkingType"],
        "children_room": rest.features["childrenRoom"],


        "schedules": prepareSchedule(rest.timetable),  # расписание


        }

    #Загрузка текстового json + Avatar_id(ссылка на Main_photo)
       # patchResponse = requests.patch(patchUrl, json=data, headers=headers)


        # Альбом
        i = 0
      #  postImage("Album",rest.latin_name,jpg)
        album_arr = os.listdir("Album/" + rest.latin_name)
        # for album_dir in album_arr:
        #  jpg_arr = os.listdir("Album/" + rest.latin_name + "/" + album_dir)
        album_ids = []
        for jpg in album_arr:
            album_ids.append(postImage("Album", rest.latin_name, jpg))
           # with open("Album/" + rest.latin_name + "/" + jpg, "rb") as f:
           #     album_image = f.read()
          #  data["album_image" + str(i)] = album_image
            i += 1

        album = prepareAlbum(album_ids)
        data["albums"] = [album]
        patchResponse = requests.patch(patchUrl, json=data, headers=headers)

            # Загрузка Меню
        i = 0
        menu_arr = os.listdir("Menu/" + rest.latin_name)
        for menu_dir in menu_arr:
            jpg_arr = os.listdir("Menu/" + rest.latin_name + "/" + menu_dir)
            for jpg in jpg_arr:
                with open("Menu/" + rest.latin_name + "/" + menu_dir + "/" + jpg, "rb") as f:
                    menu_image = f.read()
                data["menu_image" + str(i)] = menu_image
                i += 1

        if data["average_check"] == "no_avg_check":
            del data["averageCheck"]
        if data["schedules"] == "no_timetable":
            del data["schedules"]
        if data["subcategory"] == "":
            del data["subcategory"]
        if data["description"] == "no_description":
            del data["description"]
        if data["description"] == "no_description":
            del data["short_description"]
        # xx = json.loads(data)
        # yy = json.dumps(data)
        patchResponse = requests.patch(patchUrl, data=data, headers=headers)
        return patchResponse

def prepareAlbum(photo_ids):
    # i = 0
    # photo_dict_list = []
    #
    # for photo in photo_ids:
    #     photo_dict = {}
    #     photo_dict["id"]=photo
    #     photo_dict_list.append(photo_dict)
    """
    ВЗЯТЬ ОТСЮДА ID + COVER ?? Если нужно будет
    mainImagePostresponseText = mainImagePostresponse.text
    pattern = r'"id":".*"'
    result = re.findall(pattern, mainImagePostresponseText)[0]
    avatar_id = result[result.find(":") + 2:len(result) - 1]
    """
    cover_id = getPhotoId(photo_ids[-1])
    #album = {"photos": photo_ids, "title": "MainAlbum","photosCount":len(photo_ids),"orderNumber":0,"cover":cover_id} #400
    # '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["albums.photos"]}}'

    album = {"photos": photo_ids, "title": "MainAlbum", "photosCount": len(photo_ids),
             "cover": cover_id}
    # '{"status":"FieldInvalid","message":"Поле содержит недопустимое значение","data":{"fields":["albums.photos"]}}'
    return album

"""
    # основное фото
def postImage(name):    
    url = "https://tabler.ru/api/v2/images"

    payload = {}
    files = [
        ('image', ('main.jpg', open("Main_photo/"+rest.latin_name+"/main_image.jpg", 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv'

    }

    mainImagePostresponse = requests.request("POST", url, headers=headers, data=payload, files=files)
    mainImagePostresponseText = mainImagePostresponse.text
    pattern = r'"id":".*"'



    result = re.findall(pattern, mainImagePostresponseText)[0]
    avatar_id = result[result.find(":")+2:len(result)-1]
    return avatar_id
"""



#
#     # Подготовка расписания делаем паттерн на цифр+буква (идеальный вариант)
#     # затем проходим по расписанию и берем разбиение до следующего изменения расписания
#     # после заполнения списка week его надо будет разбить на словарь с началом рабочего дня и концом рабочего дня
#     pattern = r'\d+[А-Я]+'
#     #pattern= r'[a-я][А-Я]+'
#
#     week=[]
#     # если изменение происходит в четверг. сделать и для других дней
#     # циклом заполняем все дни с начала этапа и до конца этапа
#     if timetable[3:5] == "чт" or timetable[3:5] == "ЧТ" or timetable[3:5] == "Чт":
#         pos = 0
#         for i in range(0,4):
#             match = re.findall(pattern,timetable)
#             if len(match) == 0:
#                 # особенный паттерн если работает до последнего гостя
#                 pattern = r'[a-я][А-Я]+'
#                 match = re.findall(pattern, timetable)
#             pos = timetable.find(match[0])
#             week.append(timetable[7:pos+1])
#             pass
#         timetable = timetable[pos+1:]
#     elif timetable[3:5] == "ВС" or timetable[3:5] == "вс" or timetable[3:5] == "Вс":
#         # циклом заполняем все дни с начала этапа и до конца этапа
#         for i in range(0, 7):
#             match = re.findall(pattern, timetable)
#             pos = 0
#             if len(match) == 0:
#                 pattern = r'[a-я][А-Я]+'
#             match = re.findall(pattern, timetable)
#
#             if len(match) > 0:
#                 pos = timetable.find(match[0])
#                 week.append(timetable[7:pos + 1])
#             else:
#                 week.append(timetable[7:])
#                 pos = len(timetable)
#             timetable = timetable[pos + 1:]
#             pass
#
#     pass
# """
def postMainImage(name):
    url = "https://tabler.ru/api/v2/images"
    payload = {}
    files = [
        #('image', ('image.jpg', open("Main_photo/"+rest.latin_name+"/main_image.jpg", 'rb'), 'image/jpeg'))
        ('image', ('image.jpg', open("Main_photo/" + name + "/main_image.jpg", 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv'

    }
    mainImagePostresponse = requests.request("POST", url, headers=headers, data=payload, files=files)
    mainImagePostresponseText = mainImagePostresponse.text
    pattern = r'"id":".*"'
    result = re.findall(pattern, mainImagePostresponseText)[0]
    avatar_id = result[result.find(":")+2:len(result)-1]
    return avatar_id

def getPhotoId(text):
    # pattern = r'"id":".*"'
    # result = re.findall(pattern, text)[0]
    # photo_id = result[result.find(":") + 2:len(result) - 1]
    #
    json_data = json.loads(text)
    id_value = json_data['id']

    return id_value

def postImage(dir,name,number):
    url = "https://tabler.ru/api/v2/images"
    payload = {}
    files = [
        ('image', ('image'+number+'.jpg', open(dir+"/"+name+"/"+number, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv'

    }
    mainImagePostResponse = requests.request("POST", url, headers=headers, data=payload, files=files)
    mainImagePostResponseText = mainImagePostResponse.text

    pattern = r'"imageSet":{".*"}'
    #photos = re.findall(pattern, mainImagePostresponseText)[0].replace("imageSet","photos",1) # get from imageSet
    photos = re.findall(pattern, mainImagePostResponseText)[0].replace('"imageSet":', "", 1)

    photos_dict = json.loads(photos)
    cover_url = photos_dict["cover"]["url"]
    photos_dict["cover"]["path"] = cover_url
    photos = json.dumps(photos_dict)

    photos_dict = json.loads(photos)
    thumbnail_url = photos_dict["thumbnail"]["url"]
    photos_dict["thumbnail"]["path"] = thumbnail_url
    photos = json.dumps(photos_dict)

    photos_dict = json.loads(photos)
    standard_url = photos_dict["standard"]["url"]
    photos_dict["standard"]["path"] = standard_url
    photos = json.dumps(photos_dict)

    photos_dict = json.loads(photos)
    original_url = photos_dict["original"]["url"]
    photos_dict["original"]["path"] = original_url
    photos = json.dumps(photos_dict)

    return photos



def getAllFeatures(fts):
    directory_in_str = "jsons"
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = open("jsons/"+ os.fsdecode(file),encoding="utf8").read()
        try:
            text = json.loads(filename)
            for ft in text["features"]:
                fts.add(ft)
        except json.decoder.JSONDecodeError:
            return fts
    return fts

def getAllCategoriesJson(cts):
    directory_in_str = "jsons"
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = open("jsons/"+ os.fsdecode(file),encoding="utf8").read()
        try:
            text = json.loads(filename)
            cts.add(text["category"])
        except json.decoder.JSONDecodeError:
            return cts
    return cts

def prepareCategory(ct):
    category_id = getCategoryId(ct)
    if isinstance(category_id,int):
        return category_id
def preparePhones(phone):
    if "+" in phone:
        return phone[1:]
    else:
        return phone
    # return [{"phone":phone}]
   # return {"phone": phone}
   #return [ phone ]
   # return [{"id":1,"phone":phone}]


def prepareLatinName(url):
    latinName = url.split("/")
    return latinName[-1]
#fts = set()
#fts = getAllFeatures(fts)

#cts = set("")
#cts = getAllCategoriesJson(cts)
kitchens_dict = {}


#f = open("cuisines.json").read()
#json = json.loads(f)
#cuisines_array = []
#for i in json["data"]["cuisines"]:
#    cuisines_array.append(i)


# pass
tObj = TablerObject()
rest = Restraunt("", "Jsons/chacha-2.json" ,"" "", 1)
rest.phone = preparePhones(rest.phone)
rest.description = prepareDescription(rest.description)
rest.avg_check = prepareCheck(rest.avg_check)
rest.lon = prepareCoord(rest.Coordinates[1])
rest.lat = prepareCoord(rest.Coordinates[0])
rest.address = prepareAddress(rest.address)
rest.category = prepareCategory(rest)
rest.features = prepareFeatures(rest.features)
rest.latin_name = prepareLatinName(rest.additional_url)
p = postRest(rest)  # тут же и Patch внутри
pass