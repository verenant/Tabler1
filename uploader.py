import os

import requests

from restraunt import Restraunt
from requests.auth import HTTPBasicAuth
from tablerObject import TablerObject
import json
import re
import glob
username = "verenant@gmail.com"
password = "zrC!qFvI2Q"
token = "Bearer 0r06VbX4NlbG77N3DQ1gEyNv"
headers = {
    'Authorization': 'Bearer 0r06VbX4NlbG77N3DQ1gEyNv',
}
postUrl = "https://tabler.ru/api/v1/places"
from collections import OrderedDict

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
    dictFts["alcohol"] = True if ("своя пивоварня" in fts) else False

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
    print(schedule)

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

    return schedule













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

#fts = set()
#fts = getAllFeatures(fts)



pass
def postRest(rest):

    data = {
        "name": rest.name,          # название
        "lon": rest.lon,            # месторасположение
        "lat": rest.lat,
        "city": rest.city,          # город
        "street": rest.street,       # улица
        "building":rest.building,    # дом
        "phone":rest.phone          #телефон
    }
    #responseCreation = requests.post(postUrl, data = data, headers=headers)
    pass
def patchRest(rest):
    rest.getPatchData()
    #средний чек
    #краткая ссылка

    #описание
    #кухни
    #особенности
    #расписание
    # основное фото
    # меню

rest = Restraunt("","balabol.json","",1)
tObj = TablerObject()
# rest.avg_check = prepareCheck(rest.avg_check)
# rest.lon = prepareCoord(rest.Coordinates[1])
# rest.lat = prepareCoord(rest.Coordinates[0])
rest.timetable = prepareSchedule(rest.timetable)
rest.features = prepareFeatures(rest.features)

postRest(rest)






pass