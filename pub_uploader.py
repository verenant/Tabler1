import os
import string

import city
from Category import categories
from restraunt import Restraunt
from Cuisines import cuisines
from anyascii import anyascii
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
    else:
        return False

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

    #print(edit_timetable)
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
    #print(schedule_dict)

    # schedule_list = list({"isMain":schedule_dict["isMain"]}).append({"items":schedule_dict["items"]})

    # ошибка 500 '{"status":"GeneralInternalError","message":"Произошла ошибка","data":[]}'
    # scheduleList = [{"isMain":schedule_dict["isMain"],"items":json.dumps(schedule_dict["items"])}]

    # 422 '{"status":"SlugAlreadyExist","message":"Слаг занят","data":[]}' # Исправил ошибку во времени работы был пробел перед врменем
    scheduleList = [{"isMain": schedule_dict["isMain"], "items": schedule_dict["items"]}]
    #print(scheduleList)
    return scheduleList


def prepareFeatures(fts):
    dictFts = {}

    dictFts["wifi"] = False if ('No Wi-Fi' in fts) else True
    dictFts["cashfree"] = True
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
    address = address.strip()
    new_address = []
    # print(address)
    address = address.replace(",", "")
    raw_address = address.split(" ")
    string_without_number = ""
    number = ""
    # print(raw_address)
    for el in raw_address:
        #print(el)

        if "/" in el:
            number = re.findall(r'\d+/\d+', el)
            if len(number) > 0:
                #print("number = ", number)
                new_address.append(number[0])
                continue

        elif "-" in el:
            number = re.findall(r'\d+-\d+', el)
            if len(number) > 0:
                #print("number = ", number)
                new_address.append(number[0])
                continue
        elif "_" in el:
            number = re.findall(r'\d+_\d+', el)
            if len(number) > 0:
                #print("number = ", number)
                new_address.append(number[0])
                continue
        else:
            number = re.findall('\d+', el)
            if len(number) > 0:
                #print("number = ", number[0])
                new_address.append(number[0])
                continue

        string_without_number += el + " "
    if string_without_number == "":
        string_without_number = number[0]
    if len(number) == 0:
        new_address.append(string_without_number.strip())
    new_address.append(string_without_number.strip())
    #print(new_address)
    pass
    """
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
    """
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



def prepareKitchenIds(rest):
        kitchen_guru = rest.kitchen
        if "no_info" in kitchen_guru:
            return False
        kitchen_tabler = []
        kitchen_tabler_ids = []
        for k in kitchen_guru:
            if k == "Wine bars":
                kitchen_tabler_ids.append(132)
            if k == "New American":
                kitchen_tabler_ids.append(10)
            if k == 'Central European':
                kitchen_tabler_ids.append(2)
                kitchen_tabler_ids.append(28)
            if k == 'Beer bars':
                kitchen_tabler_ids.append(39)
            if k == 'Asian':
                kitchen_tabler_ids.append(5)
            if k == "European":
                kitchen_tabler_ids.append(2)
                kitchen_tabler_ids.append(28)
            if k == "German":
                kitchen_tabler_ids.append(73)
            if k == "Delis":
                kitchen_tabler_ids.append(60)
            if k == 'Fast food':
                kitchen_tabler_ids.append(11)
            if k == "Czech":
                kitchen_tabler_ids.append(89)
            if k == "Soups":
                kitchen_tabler_ids.append(126)
                kitchen_tabler_ids.append(98)
            if k == "Mediterranean":
                kitchen_tabler_ids.append(4)
            if k == "International":
                kitchen_tabler_ids.append(119)
                kitchen_tabler_ids.append(62)
            if k == "Sandwiches":
                kitchen_tabler_ids.append(120)
            if k == "Vietnamese":
                kitchen_tabler_ids.append(19)
            if k == "Ukrainian":
                kitchen_tabler_ids.append(84)
            if k == "Salads":
                kitchen_tabler_ids.append(112)
            if k == "Eastern European":
                kitchen_tabler_ids.append(2)
                kitchen_tabler_ids.append(28)
            if k == "Greek":
                kitchen_tabler_ids.append(57)
            if k == "Grill":
                kitchen_tabler_ids.append(40)
            if k == "Cocktail bars":
                kitchen_tabler_ids.append(125)
            if k == "Barbecue":
                kitchen_tabler_ids.append(102)
                kitchen_tabler_ids.append(40)
            if k == "Mexican":
                kitchen_tabler_ids.append(32)
            if k == "Contemporary":
                kitchen_tabler_ids.append(62)
            if k == "Sushi":
                kitchen_tabler_ids.append(19)
                kitchen_tabler_ids.append(27)
            if k == "Vegetarian":
                kitchen_tabler_ids.append(31)
            if k == "Dessert":
                kitchen_tabler_ids.append(123)
            if k == "Seafood":
                kitchen_tabler_ids.append(75)
            if k == "Italian":
                kitchen_tabler_ids.append(8)
            if k == "Gluten-free":
                kitchen_tabler_ids.append(112)
            if k == "Steakhouses":
                kitchen_tabler_ids.append(40)
            if k == "Healthy food":
                kitchen_tabler_ids.append(112)
            if k == "South American":
                kitchen_tabler_ids.append(10)
            if k == "Pizza":
                kitchen_tabler_ids.append(18)
            if k == "Chinese":
                kitchen_tabler_ids.append(5)
            if k == "Turkish":
                kitchen_tabler_ids.append(30)
        return kitchen_tabler_ids

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
            "street": rest.address[1],  # улица
            "building": rest.address[0],  # дом
            "phone_number": rest.phone[1:], #json.dumps(rest.phone),  # телефоны
            #"city_id": city_id, # город
            "city_id": rest.city,  # город
            "category_id": rest.category,
        }
    if rest.category == "no_info":
        return "sry bad restraunt --closed(no category)"
    if data["phone_number"] == "o_info":
        del data["phone_number"]
    #if data["subcategory"] == "":
    #    del data["subcategory"]
    postUrl = "https://tabler.pub/api/v1/places"
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    #responseCreation = requests.post(postUrl, data=json.dumps(data), headers=headers)
    patchUrl = response.text
    rest.id = patchUrl[patchUrl.find("latinName") + len("latinName") + 3:patchUrl.find("city") - 3]
    patchUrl = postUrl + "/" + patchUrl[patchUrl.find("latinName") + len("latinName") + 3:patchUrl.find("city") - 3]
    return patchUrl


def patchRest(rest, url):
    patchUrl = url
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }

    #Обработка кухонь
    cuisine_id = prepareKitchenIds(rest)

    data = {
        # "phones": rest.phone,  # телефоны
        #    "avatar_id": avatar_id, # загрузка основного фото
        #    "background_id": avatar_id,
        "average_check": rest.avg_check,  # средний чек
        #"latinName" : (rest.latin_name).lower(),   # краткая ссылка
        "latin_name": (rest.latin_name).lower()+"--99992",
        "description": rest.description,  # описание
        "short_description": rest.short_description,
        #"cuisine_ids": prepareKitchen(rest.kitchen),  # кухни_id
        "subcategory": rest.subcategory,
        # особенности
        "wifi": rest.features["wifi"],
        "cuisine_ids" : cuisine_id,
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
    links = prepareLinks(rest)
    if links:
        data["links"] = links
    #Если кухонь нет, то убираем их
    if data["cuisine_ids"] == False or len(data["cuisine_ids"]) == 0:
        del data["cuisine_ids"]
    if data["average_check"] == "no_info":
        del data["average_check"]
    if data["schedules"] == "no_info":
        del data["schedules"]

    category_id = rest.category
    for c in categories:
        if c["id"] == category_id:
            category = c["latinName"]
            break
    if data["subcategory"] == category :#or data["no_info"] != rest.category_str:
        del data["subcategory"]
    if data["subcategory"] == "":
        del data["subcategory"]
    if data["description"] == "no_info":
        del data["description"]
    if data["description"] == "no_info":
        del data["short_description"]

    if (data["description"] == "" or data["short_description"] =="") and rest.last_publication != "" and (">" in rest.last_publication):
        desc =  (rest.last_publication).split(">")
        if len(desc) == 2:
            data["description"] = desc[0] + desc[1][2:]
            data["short_description"] = desc[0]
        else:
            data["description"] = desc[0]
            data["short_description"] = desc[0]
    if  "no_info" in data["description"]:
        del data["description"]
    if "no_info" in data["short_description"]:
        del data["short_description"]

    if prepareOrganisationId(rest):
        data["organisation_id"] = rest.organisation_id

    patchResponse = requests.patch(patchUrl, json=data, headers=headers)

    #patchResponse = requests.patch(patchUrl, data=json.dumps(data,ensure_ascii=False), headers=headers)

    patchResponse_text = patchResponse.text
    if patchResponse.status_code != 200:
        print(patchResponse_text)
    else:
        print("https://tabler.pub/"+(data["latin_name"]).lower())

    return patchResponse_text

    pass


def postImage(dir,name):
    url = "https://tabler.pub/api/v2/images"
    payload = {}
    files = [
        ('image', (name, open(dir+"/"+name, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    mainImagePostResponse = requests.request("POST", url, headers=headers, data=payload, files=files)
    mainImagePostResponseText = mainImagePostResponse.text

    pattern = r'"imageSet":{".*"}'
    if (len(re.findall(pattern, mainImagePostResponseText)) > 0):
        photos = re.findall(pattern, mainImagePostResponseText)[0].replace('"imageSet":', "", 1)
    else:# повтор загрузки --- потом отмена
        mainImagePostResponse = requests.request("POST", url, headers=headers, data=payload, files=files)
        mainImagePostResponseText = mainImagePostResponse.text
        if (len(re.findall(pattern, mainImagePostResponseText)) == 0):
            print("otkaz servera pri zagruzke")
            return False
    photos_dict = json.loads(photos)
    cover_url = photos_dict["cover"]["url"]
    photos_dict["cover"]["path"] = cover_url

    thumbnail_url = photos_dict["thumbnail"]["url"]
    photos_dict["thumbnail"]["path"] = thumbnail_url

    standard_url = photos_dict["standard"]["url"]
    photos_dict["standard"]["path"] = standard_url

    original_url = photos_dict["original"]["url"]
    photos_dict["original"]["path"] = original_url

    photos_dict["isLoading"] = False
    photos_dict["isDeleted"] = False

    photos_dict["orderNumber"] = name[:-4]

    return photos_dict

def getPhotoId(text):
    json_data = json.loads(text)
    id_value = json_data['id']
    return id_value

def prepareAlbum(photo_ids):
    cover_id = getPhotoId(json.dumps(photo_ids[-1]))
    album = {"photos": photo_ids, "title": "Main Album",  "cover": cover_id}
    return album

def prepareMenu(photo_ids):
    cover_id = getPhotoId(json.dumps(photo_ids[-1]))
    album = {"photos": photo_ids, "title": "Main Menu",  "cover": cover_id}
    return album

def patchMenu(rest,postResponse):
    menu_path = rest.filename + "/menu"
    menu_imgs_ids = []
    i = 0
    if os.path.exists(menu_path) and len(os.listdir(menu_path))>0:
        menu_items = os.listdir(menu_path)
        for item in menu_items:
            #print(item)
            menu_imgs_ids.append(postImage(menu_path, item))
            i += 1
            pass
        menu = prepareMenu(menu_imgs_ids)
        menuList = [menu]
        if len(menuList) == 0:
            return "no_menu"
        rest.menu = {"menus":menuList}
        pass
    else:
        return "no_menu"
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    menu_add = requests.patch(postResponse, json=rest.menu, headers=headers)
    menu_add_text = menu_add.text
    return menu_add.status_code


def patchAlbum(rest,postResponse):
    album_path = rest.filename + "/Album"
    album_imgs_ids = []
    i = 0
    if os.path.exists(album_path) and len(os.listdir(album_path))>0:
        album_items = os.listdir(album_path)
        for item in album_items:
            #print(item)
            album_imgs_ids.append(postImage(album_path, item))
            i += 1
            pass
        album = prepareAlbum(album_imgs_ids)
        albumList = [album]
        if len(albumList) == 0:
            return "no_album"
        rest.album = {"albums":albumList}
        pass
    else:
        return "no_album"
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    album_add = requests.patch(postResponse, json=rest.album, headers=headers)
    album_add_text = album_add.text
    return album_add.status_code

def prepareText(text):
    text = anyascii(text)
    text_split = text.split(". ")
    new_text = ""
    for t in text_split:
        if "Google" in t or "Facebook" in t :
            continue
        if len(t)>3:
            new_text+=t+". "
    return new_text

#Тестировать
def prepareOrganisationId(rest):
    raw_index_path= (rest.filename).rfind("/")
    city_rest_path = (rest.filename)[:raw_index_path]
    chains_file = open(city_rest_path + "/networks.txt")
    chains = chains_file.readlines()
    for chain in chains:
        json_chain = json.loads(chain)
        if rest.name == json_chain["name"]:
            rest.organisation_id = json_chain["organisationId"]
            return True
    return False

def prepareLinks(rest):
    if rest.inst_url == "" and rest.place_url == "":
        return False
    links = []
    if rest.inst_url != "":
        inst_link = {"link":"https://www.instagram.com/"+rest.inst_url[1:]}
        links.append(inst_link)
    if rest.place_url != "":
        if rest.place_url == "no_info":
            return False
        place_link = {"link":rest.place_url}
        links.append(place_link)

    #links_dict = {"links":links}
    return links


def postImageAndReturnId(dir,name):
    url = "https://tabler.pub/api/v2/images"
    payload = {}
    files = [
        ('image', (name, open(dir+"/"+name, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    mainImagePostResponse = requests.request("POST", url, headers=headers, data=payload, files=files)
    mainImagePostResponseText = mainImagePostResponse.text
    photo_json = json.loads(mainImagePostResponseText)
    photo_id = photo_json["data"]["imageSet"]["id"]
    return photo_id


# Протестировать!
def createNews():
    #загрузка текста
    #старый формат до публикаций
    #img_index = rest.last_publication[:2]

    #Разделение текста описания и текста поста из инстаграмма
    desc_and_last_publication = rest.last_publication
    if ">" in rest.last_publication:
        index_arrow = desc_and_last_publication.find(">")
        text_before_arrow = desc_and_last_publication[:index_arrow]
        text_after_arrow = desc_and_last_publication[index_arrow+1:]
        img_index = text_after_arrow[:2]

        if img_index == "0_":
            img_name = "Album/0.jpg"
        elif img_index == "1_":
            img_name = "Album/1.jpg"
        elif img_index == "2_":
            img_name = "Album/2.jpg"
        else:
            print("no ready text for publication")
            return False
    else:
        print("no ready text for publication")
        return False
    ##text = rest.last_publication[2:]
    text = text_after_arrow[2:]
    # загрузка фотографии и получение ее id
    imageSetIds = [postImageAndReturnId(rest.filename,img_name)]
    placeId = rest.id
    type = "news"
    #url = "https://tabler.pub/posts/create"
    url = "https://tabler.pub/api/v2/posts"
    data = {
        "imageSetIds": imageSetIds,
        "placeId": placeId,
        "type": type,
        "text": text,
    }


    #Post запрос на создание новости (Поста)
    headers = {
        'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
    }
    create_post_response = requests.post(url, json=data, headers=headers)
    response_text = create_post_response.text
    #print(response_text)
    return create_post_response.status_code

#Тестировать
def postMainImage(rest):
    url = "https://tabler.pub/api/v2/images"

    if os.path.exists(rest.filename+"/Album"):
        if len(os.listdir(rest.filename+"/Album"))>0:
            payload = {}
            files = [
                ('image', ('0.jpg', open(rest.filename+"/Album/0.jpg", 'rb'), 'image/jpeg'))
            ]
            headers = {
                'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'

            }
            mainImagePostresponse = requests.request("POST", url, headers=headers, data=payload, files=files)
            mainImagePostresponseText = mainImagePostresponse.text
            pattern = r'"id":".*"'
            result = re.findall(pattern, mainImagePostresponseText)[0]
            avatar_id = result[result.find(":")+2:len(result)-1]
            data = {
                "avatar_id": avatar_id,
                "background_id": avatar_id,
            }
            tabler_url = "https://tabler.pub/api/v1/places/"+rest.id
            post_main_image = requests.patch(tabler_url, json=data, headers=headers)
            return avatar_id
        else:
            return False
    else:
        return False

def prepareRestForPost(rest):
    rest.category = getCategoryId(rest)
    rest.description = prepareText(rest.description)
    rest.short_description = prepareText(rest.short_description)
    #тестировать
    if (rest.short_description == "" or ("no_info" in rest.short_description) or ("no_info" in rest.description)) and rest.last_publication != ">":
        rest.description = (rest.last_publication)[:((rest.last_publication).find(">"))]
        first_point = (rest.description).find(".")
        if first_point > 1:
            rest.short_description = (rest.description)[:first_point + 1]
        else:
            rest.short_description = rest.description

    rest.city = prepareCityId(rest)
    if rest.timetable != "no_info":
        rest.timetable = prepareTimetable(rest.timetable)
    rest.check = prepareCheck(rest.avg_check)
    rest.features = prepareFeatures(rest.features)

    pass

#prepareText("Locals recommend Czech dishes at this restaurant. Guests don't highly appreciate kama at Hotel - Restaurace Ple&scaron;ivec. The staff is said to be accommodating here. This place is remarkable for its fast service. This spot is rated on Google 4.1 by its visitors.")
#получить адрес папки ресторана
country = "Czech-Republic"
letter_cities = os.listdir(country)
for letter in letter_cities:
    print(letter+"_cities")
    if letter == "A_cities":
        pass
    letter_path = country + "/" + letter
    cities = os.listdir(letter_path)
    if len(cities)>0:
        for c in cities:
            city_path = letter_path+"/"+c
            rests_in_city = os.listdir(city_path)
            print(city_path)
            for rest in rests_in_city:
                rest_path = city_path+"/"+rest
                #print(rest_path)
                print("============================================")

                if os.path.exists(rest_path + "/json.txt" ):
                    rest = Restraunt_from_guru("", "", 1,rest_path)
                else:
                    print(rest_path + " =-> no_json_file")
                    continue
                #category = rest.category
                #подготовка ресторана
                prepareRestForPost(rest)
                #подготовка адреса
                rest.address = prepareAddress(rest.address)
                #пред загрузка ресторана(POST)
                postResponse = postRest(rest)
                print("https://tabler.pub/"+rest.id)
                #загрузка ресторана (Patch)
                patchResponse = patchRest(rest,postResponse)



                menu = patchMenu(rest,postResponse)

                album = patchAlbum(rest, postResponse)
                #Если альбом загрузился, то загружаем главное изображение
                if album == 200:
                    postMainImage(rest)
                if album == 200 and rest.last_publication != "":
                    create_post_result = createNews()
                    print("Создание первого поста для заведения = " + str(create_post_result))

                #Публикация ресторана, только если меню загрузилось
                if menu == 200 and postResponse != "" and patchResponse:
                    pass
                    #responsePublish = requests.post(postResponse + "/moderation-status/published", headers=headers)
                    #print("Результат публикации ресторана " + rest.latin_name + " = " + str(responsePublish.status_code))
                #print(postResponse)

                pass
pass