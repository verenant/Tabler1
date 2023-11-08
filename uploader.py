import os

from restraunt import Restraunt

from tablerObject import TablerObject
import json
import re
import glob

from collections import OrderedDict
from PIL import Image
from restraunt import Restraunt

username = "verenant@gmail.com"
password = "zrC!qFvI2Q"
token = "Bearer 0r06VbX4NlbG77N3DQ1gEyNv"
headers = {
    'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv',
}
postUrl = "https://tabler.ru/api/v1/places"
from tablerObject import TablerObject
import json
import re
import os
import requests
from Category import categories
from Cuisines import cuisines

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
    kitchens_array = []
    for kitchen in kitchens:
        kitchen = changeKithcenName(kitchen)
        for i in cuisines["cuisines"]:
            if i["name"] == kitchen:
                kitchens_array.append(i)
    return kitchens_array

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
    if check == "no_avg_check":
        return "no_avg_check"
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
    #schedule = OrderedDict()
    #schedule["Пн"]=""
    #schedule["Вт"] = ""
    #schedule["Ср"] = ""
    #schedule["Чт"] = ""
    #schedule["Пт"] = ""
    #schedule["Сб"] = ""
    #schedule["Вс"] = ""

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
        #print(schedule[i].split(" — "))
        sd = schedule[i].split(" — ")
        schedule_dict["items"][day]["startAt"] = sd[0]
        schedule_dict["items"][day]["endAt"] = sd[1]
        day += 1
    #schedule_list = list({"isMain":schedule_dict["isMain"]}).append({"items":schedule_dict["items"]})
    scheduleList = [schedule_dict["isMain"],schedule_dict["items"]]
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
           # "city": rest.city,  # город
            "street": rest.address[0],  # улица
            "building": rest.address[1],  # дом
            "phone": rest.phone,  # телефон
            "city_id": city_id,
            "category_id": rest.category,
            "subcategory": rest.subcategory
        }
    if data["phone"] == "no_phone":
        del data["phone"]
    if data["subcategory"] == "":
        del data["subcategory"]

    responseCreation = requests.post(postUrl, json=data, headers=headers)
    patchUrl = responseCreation.text
    # нахожу айди латин нейма прибавляю к нему длину этого слова плюс 3 символа двоеточие и кавычки(х2) и до следующего элемента(city) минус 3 символа запятая и кавычки(х2)
    patchUrl =postUrl+"/"+ patchUrl[patchUrl.find("latinName") + len("latinName") + 3:patchUrl.find("city") - 3]
    # print(patchUrl)
    responcePatch = patchRest(rest, patchUrl)
    if responcePatch.status_code == 200:
        responsePublish = requests.post(patchUrl+"/moderation-status/published")


    pass

def patchRest(rest,patchUrl):
    #rest.getPatchData()


    data = {

        "averageCheck": rest.avg_check,  # средний чек
        "latinName" : rest.latin_name,   # краткая ссылка

        "description": rest.description,  # описание
        "short_description": prepareShortDescription(rest.description),
        "cuisines": prepareKitchen(rest.kitchen),  # кухни
        "subcategory": rest.subcategory,
        # особенности
        "wifi": rest.features["wifi"],
        "cashfree": rest.features["cashfree"],
        "terrace": rest.features["terrace"],
        "alcohol": rest.features["alcohol"],  #  уточнить по поводу заполнения
        "mobileCharge": rest.features["mobileCharge"],
        "smokeZone": rest.features["smokeZone"],
        "hookah": rest.features["hookah"],
        "karaoke": rest.features["karaoke"],
        "delivery": rest.features["delivery"],
        "businessLunch": rest.features["businessLunch"],
        "sportTranslations": rest.features["sportTranslations"],
        "entertainment": rest.features["entertainment"],
        "liveMusic": rest.features["liveMusic"],
        "dancefloor": rest.features["dancefloor"],
        "parkingType": rest.features["parkingType"],
        "childrenRoom": rest.features["childrenRoom"],


        "schedules": prepareSchedule(rest.timetable),  # расписание


    }
    # основное фото
    with open("Main_photo/"+rest.latin_name+"/main_image.jpg","rb") as f:
         main_image = f.read()
    data["main_image"] = main_image


    # Загрузка Меню
    i=0
    menu_arr = os.listdir("Menu/"+rest.latin_name)
    for menu_dir in menu_arr:
        jpg_arr = os.listdir("Menu/"+ rest.latin_name+"/"+ menu_dir)
        for jpg in jpg_arr:

            with open("Menu/"+rest.latin_name+"/" + menu_dir+"/" + jpg, "rb") as f:
                menu_image = f.read()
            data["menu_image"+str(i)] = menu_image
            i+=1

    # Альбом
    i = 0
    album_arr = os.listdir("Album/" + rest.latin_name)
   # for album_dir in album_arr:
      #  jpg_arr = os.listdir("Album/" + rest.latin_name + "/" + album_dir)
    for jpg in album_arr:
        with open("Album/" + rest.latin_name + "/" + jpg, "rb") as f:
            album_image = f.read()
        data["album_image" + str(i)] = album_image
        i += 1





    if data["averageCheck"] == "no_avg_check":
        del data["averageCheck"]
    if data["schedules"] == "no_timetable":
        del data["schedules"]
    if data["subcategory"] == "":
        del data["subcategory"]
    if data["description"] == "no_description":
        del data["description"]
    if data["description"] == "no_description":
        del data["short_description"]
    patchResponse = requests.patch(patchUrl, data=data, headers=headers)
    return patchResponse













    pass
#     """
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
rest = Restraunt("", "Jsons/chit-mil.json" ,"" "", 1)
rest.description = prepareDescription(rest.description)
rest.avg_check = prepareCheck(rest.avg_check)
rest.lon = prepareCoord(rest.Coordinates[1])
rest.lat = prepareCoord(rest.Coordinates[0])
rest.address = prepareAddress(rest.address)
rest.category = prepareCategory(rest)
rest.features = prepareFeatures(rest.features)
rest.latin_name = prepareLatinName(rest.additional_url)
postRest(rest)  # тут же и Patch внутри
pass