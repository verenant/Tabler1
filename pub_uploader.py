import os
import string

from restraunt import Restraunt

from tablerObject import TablerObject
import json
import re

from restraunt import Restraunt


username = "verenant@gmail.com"
password = "G@dpIABvvT"
token = "Bearer 0r06VbX4NlbG77N3DQ1gEyNv"
headers = {
    'Authorization': 'Bearer fkMjBV6wTJPnm4FnRMOVvfYG',
    "Content-Type": "application/json;charset=UTF-8"
}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}
postUrl = "https://tabler.ru/api/v1/places"


#разбиваем адрес на улицу и дом, есть адреса без дома
#если номер дома заканчиваетсяна ".", то ее убираем
def prepareAddress(address):
    address = address.split("\xa0")
   # if address[1][-1]=="." or address[1][-1]==",":
    if address[1][-1] in string.punctuation:
        address[1] = address[1][:-1]

    return address

#Делаем из описания короткое
def prepareShortDescription(description):
    short_description = description.split(".", 1)
    #short_description = short_description[0].split("                ")
    return short_description[0]


def prepareCheck(check):
    if check != "no_info":
        return int(check)

def prepareTimetable(timetable):
    guru_timetable = timetable["timetable"]
    edit_timetable = []
    k = 0
    # Убираем перерывы
    for i in range(len(guru_timetable)):
        if i==0:
            edit_timetable.append(guru_timetable[0])
            continue
        # если в предыдущем есть текущий день, то конец текущего дня добавить в конец прошлого, а прошлый конец убрать

        if guru_timetable[i][:2] in edit_timetable[i-k-1]:
            edit_timetable[i-k-1] = edit_timetable[i-k-1][:edit_timetable[i-k-1].find("-")] + guru_timetable[i][guru_timetable[i].find("-"):]
            k+=1
            continue
        edit_timetable.append(guru_timetable[i])

    print(edit_timetable)
    schedule_dict1 = {

        "isMain": True, "items": [
            {"dayOfWeek": 1, "endAt": "", "startAt": ""},
            {"dayOfWeek": 2, "endAt": "", "startAt": ""},
            {"dayOfWeek": 3, "endAt": "", "startAt": ""},
            {"dayOfWeek": 4, "endAt": "", "startAt": ""},
            {"dayOfWeek": 5, "endAt": "", "startAt": ""},
            {"dayOfWeek": 6, "endAt": "", "startAt": ""},
            {"dayOfWeek": 7, "endAt": "", "startAt": ""},

        ]
    }

    schedule_dict = {

        "isMain": True, "items": [
        ]
    }

    i = 0
    for day in edit_timetable:
        dayOfWeek = -1
        if day[:2] == "Mo":
            dayOfWeek = 0
        if day[:2] == "Tu":
            dayOfWeek = 1
        if day[:2] == "We":
            dayOfWeek = 2
        if day[:2] == "Th":
            dayOfWeek = 3
        if day[:2] == "Fr":
            dayOfWeek = 4
        if day[:2] == "Sa":
            dayOfWeek = 5
        if day[:2] == "Su":
            dayOfWeek = 6
        if dayOfWeek == -1:
            continue
        sd = day[3:].split("-")
        schedule_dict["items"].append({})

        schedule_dict["items"][i]["dayOfWeek"] = int(dayOfWeek)+1
        schedule_dict["items"][i]["startAt"] = sd[0]
        schedule_dict["items"][i]["endAt"] = sd[1]
        i += 1

    #for day in schedule_dict["items"]:
    #    if day["startAt"] == "" and day["endAt"] == "":
    #        del schedule_dict
    print(schedule_dict)

    # schedule_list = list({"isMain":schedule_dict["isMain"]}).append({"items":schedule_dict["items"]})

    # ошибка 500 '{"status":"GeneralInternalError","message":"Произошла ошибка","data":[]}'
    # scheduleList = [{"isMain":schedule_dict["isMain"],"items":json.dumps(schedule_dict["items"])}]

    # 422 '{"status":"SlugAlreadyExist","message":"Слаг занят","data":[]}' # Исправил ошибку во времени работы был пробел перед врменем
    scheduleList = [{"isMain": schedule_dict["isMain"], "items": schedule_dict["items"]}]
    #print(scheduleList)
    return scheduleList


def prepareFeatures(fts):
    dictFts = {}

    dictFts["wifi"] = True if ('Wi-Fi' in fts) else False
    if ('Cash only' in fts):
        dictFts["cashfree"] = False
    if ('Сredit cards accepted' in fts):
        dictFts["cashfree"] = True
    dictFts["terrace"] = True if ('Outdoor seating' in fts) else False
    dictFts["mobileCharge"] = True
    dictFts["smokeZone"] = 2

    dictFts["hookah"] = False
    dictFts["karaoke"] = False
    dictFts["delivery"] = False if ("No delivery" in fts) else True
    dictFts["businessLunch"] = False
    dictFts["sportTranslations"] = True if ("TV" in fts) else False
    dictFts["childrenRoom"] = False
    # по алкоголю лучше уточнить перед загрузкой
    dictFts["alcohol"] = True

    dictFts["entertainment"] = 0
    dictFts["liveMusic"] = 0
    dictFts["dancefloor"] = 0
    if ("No parking" in fts):
        dictFts["parkingType"] = 0
    if ("Parking" in fts):
        dictFts["parkingType"] = 3

    return dictFts


t1 = {"timetable": [
        "Fr 16:00-20:00",
        "Sa 11:30-13:30",
        "Sa 16:00-20:00",
        "Su 11:30-13:30",
        "Su 16:00-20:00"
]}

t2 = { "timetable": [
        "Mo 14:00-22:00",
        "Tu 14:00-00:00",
        "We 14:00-00:00",
        "Th 14:00-00:00",
        "Fr 14:00-03:00",
        "Sa 13:00-03:00",
        "Su 12:00-22:00"
    ]}
prepareTimetable(t2)