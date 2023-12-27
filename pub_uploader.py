import os
import string

import city
from Category import categories
from restraunt import Restraunt
from Cuisines import cuisines

from tablerObject import TablerObject
import json
import re
import requests
from restraunt import Restraunt
from restraunt_guru import Restraunt_from_guru


cities_from_tabler = city.getCitiesFromTabler()
username = "verenant@gmail.com"
password = "j0eXOTdwxB"
token = "Bearer 5V2EABW0ODofJAaQqaz5ifkB"
headers = {
    'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB',
    "Content-Type": "application/json;charset=UTF-8"
}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}
postUrl = "https://tabler.pub/api/v1/places"

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
    guru_timetable = timetable
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
    dictFts["cashfree"] = False
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

    dictFts["parkingType"] = 2
    if ("No parking" in fts):
        dictFts["parkingType"] = 0
    if ("Parking" in fts):
        dictFts["parkingType"] = 3

    return dictFts

def prepareAddress(address):
    new_address = []
    number = re.findall('\d+', address)
    string_without_number = re.sub(r'\d+', '', address).strip()
    #print("String without number:", string_without_number)
    new_address.append(string_without_number)

    if len(number)>0:
        new_address.append(number[0])
    if string_without_number == "" or len(number)==0:
        if len(number) == 0:
            new_address.append(string_without_number)
        if len(number) > 0 and string_without_number == "":
            new_address[0] = number[0]
        #print("Number:", number[0])
    return new_address

def getCategoryId(rest):
    restCat = rest.category
    for category in categories:
        if category["name"] == restCat:
            return category["id"]
        rest.subcategory = restCat
        if restCat == "coffeehouse":
            return 23
        if restCat== "BBQ":
            return 9
        if restCat== "places to eat":
            return 1
        if restCat== "sushi restaurants":
            return 9
        if restCat== "fast food":
            return 14
        if restCat== "cafeterias":
            return 34
        if restCat== "cafeteria":
            return 34
        if restCat== "seafood restaurants":
            return 9
        if restCat== "chinese restaurant":
            return 9
        if restCat== "restaurants":
            return 9
        if restCat== "clubs":
            return 13
        if restCat== "chinese restaurants":
            return 9
        if restCat== "coffeehouses":
            return 23
        if restCat== "pizza restaurant":
            return 9
        if restCat== "vegetarian restaurant":
            return 9
        if restCat== "Ресторанный комплекс":
            return 9
        if restCat== "pubs & bars":
            return 12
        if restCat== "cafes":
            return 1
        if restCat == "restaurants with desserts":
            return 9
        if restCat == "pizza restaurants":
            return 9
        if restCat == "BBQs":
            return 9
        if restCat == "cafe":
            return 1
        if restCat == "" or restCat == "no_info":
            return "no_info"
        #Если встретилось что-то неизвестное, то делаем это кафешкой
        if restCat == rest.category:
            return 1


def getCityId(filename):
    raw_filename_end = filename.rfind("/")
    raw_filename = filename[:raw_filename_end]
    raw_filename_end = raw_filename.rfind("/")
    raw_filename = raw_filename[:raw_filename_end]
    city_filename = "1_"+raw_filename+".txt"
    f = open(city_filename,encoding="UTF-8")
    j = f.read()
    f.close()
    city_id = ""
    city_dict = json.loads(j)
    for c in cities_from_tabler:
        if "latinName" in c:
            if c["latinName"] == city_dict["latin_name"]:
                city_id = c["id"]
                return city_id
        #if "latin_name" in c:
        #    if c["latin_name"] == city_dict["latin_name"]:
        #        city_id = c["id"]
    return city_id

def getCityIdFromCity(city_dict):
    #city_latin_name = json.loads(city_dict)["latin_name"]
    city_latin_name = city_dict["latin_name"]
    for c in cities_from_tabler:
        if c["latinName"] == city_latin_name:
            city_id = c["id"]
    return city_id


def prepareCityId(rest):
    city_id = ""
    if rest.city == "":
        city_id = getCityId(rest.filename)
        if city_id == "":
            print("sry, City not in Tabler")
            return "sry, City not in Tabler"
    else:
        city_id = getCityIdFromCity(rest.city)
    return city_id

def postRest(rest):
    if rest.category == "no_info":
        return "sry bad restraunt --closed(no category)"
    if rest.address == "no_info":
        return "sry bad restraunt cant post--(no address)"
    if rest.lat == "no_info":
        return "sry bad restraunt cant post--(no coords)"

    url = "https://tabler.pub/api/v1/places"
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    data = {
            "name": rest.name,  # название
            #"latinName": rest.latin_name,
            "lon": rest.lon,  # месторасположение
            "lat": rest.lat,
            "city": rest.city,
            "street": rest.address[0],  # улица
            "building": rest.address[1],  # дом
            "phone_number": rest.phone[1:], #json.dumps(rest.phone),  # телефоны
            #"city_id": city_id, # город
            "city_id": rest.city,  # город
            "category_id": rest.category,
        }
    if rest.category == "no_info":
        return "srt bad restraunt --closed(no category)"
    if data["phone_number"] == "no_info":
        del data["phone_number"]
    #if data["subcategory"] == "":
    #    del data["subcategory"]
    postUrl = "https://tabler.pub/api/v1/places"
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    #responseCreation = requests.post(postUrl, data=json.dumps(data), headers=headers)
    patchUrl = response.text
    patchUrl = postUrl + "/" + patchUrl[patchUrl.find("latinName") + len("latinName") + 3:patchUrl.find("city") - 3]
    return patchUrl


def patchRest(rest, url,category):
    patchUrl = url
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    data = {
        # "phones": rest.phone,  # телефоны
        #    "avatar_id": avatar_id,
        #    "background_id": avatar_id,
        "average_check": rest.avg_check,  # средний чек
        #  "latin_name" : rest.latin_name,   # краткая ссылка
        "description": rest.description,  # описание
        "short_description": rest.short_description,
        #"cuisine_ids": prepareKitchen(rest.kitchen),  # кухни_id
        "subcategory": rest.subcategory,
        # особенности
        "wifi": rest.features["wifi"],
        "cashfree": rest.features["cashfree"],
        "terrace": rest.features["terrace"],
        "alcohol": rest.features["alcohol"],  # уточнить по поводу заполнения
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
        # "organistaion_id":

        "schedules": rest.timetable,  # расписание
    }
    if data["average_check"] == "no_info":
        del data["averageCheck"]
    if data["schedules"] == "no_info":
        del data["schedules"]
    if data["subcategory"] == "" :#or data["no_info"] != rest.category_str:
        del data["subcategory"]
    if data["subcategory"] == category:
        del data["subcategory"]
    if data["description"] == "no_info":
        del data["description"]
    if data["description"] == "no_info":
        del data["short_description"]
    patchResponse = requests.patch(patchUrl, json=data, headers=headers)
    patchResponse_text = patchResponse.text
    pass
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

def prepareRestForPost(rest):
    rest.category = getCategoryId(rest)
    rest.city = prepareCityId(rest)
    rest.timetable = prepareTimetable(rest.timetable)
    rest.check = prepareCheck(rest.avg_check)
    rest.features = prepareFeatures(rest.features)

    pass


#получить адрес папки ресторана
country = "Czech-Republic"
letter_cities = os.listdir(country)
for letter in letter_cities:
    letter_path = country + "/" + letter
    cities = os.listdir(letter_path)
    if len(cities)>0:
        for c in cities:
            city_path = letter_path+"/"+c
            rests_in_city = os.listdir(city_path)
            for rest in rests_in_city:
                rest_path = city_path+"/"+rest
                print(rest_path)
                pass



rest = Restraunt_from_guru("", "", 1)
category = rest.category
prepareRestForPost(rest)
rest.address = prepareAddress(rest.address)
postResponse = postRest(rest)
patchResponse = patchRest(rest,postResponse,category)
print(postResponse)
pass