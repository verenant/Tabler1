import ipaddress
import json
import os
import random
import shutil
import time

import bs4
import requests

import insta_parsing
import parsing
import city
import restraunt_guru


def prepare_city_href(href):
    new_href_slash_index = href.rfind("/")+1
    city_end = href[new_href_slash_index:]
    new_href = href.replace(city_end, "restaurant-"+city_end+"-t1")
    return new_href


def prepare_features(features):
    s = features.strip('[]').split(',')
    s = [element.strip('\'') for element in s]
    return s


proxies_from_network = [
]
"""
city = {
    "name" : "",
    "latin_name": "",
    "lat": "",
    "lon": ""
}
"""
cities = []
main_page= "https://restaurantguru.com/"

#=================================================
stTime = time.localtime()
print(f"{stTime.tm_hour}-{stTime.tm_min}")
good_proxies = parsing.get_good_proxies()
proxies_from_network = parsing.get_new_proxies()  # получение бесплатных прокси
######get_good_proxies(main_page,proxies_from_network) #составление файла с хорошими прокси
#countries = get_countries(main_page)
countries = parsing.get_countries()
counter = 0

latin_names_list = []
"""
#заполнение ресторана, потом переместить в пункт РАБОТА НАД ПАРСИНГОМ РЕСТОРАНОВ
rest_guru_json_object = json.loads(parsing.get_json_restraunt("https://restaurantguru.com/Osteria-La-Baracca-Frydek-Mistek",good_proxies))
rest_guru_json_object["features"] = prepare_features(rest_guru_json_object["features"])

restraunt_object = restraunt_guru.Restraunt_from_guru(rest_guru_json_object,0)
menu_status = parsing.get_menu(restraunt_object.menu_href,restraunt_object.additional_url,good_proxies)
# если меню нет-> прерываем этот ресторан
pass
"""

counter_restraunt = 0
for countryIndex in range(1, 2): # не через in чтобы пропустить Алеутские острова # поменять на len(countries) при запуске на все страны
    #letters = get_city_letters(countries[4])
    #letters = get_city_letters
    country = "Czech-Republic"  #countries[countryIndex] # при полном парсинге городов
    country_path= country
    if os.path.exists(country_path):
        shutil.rmtree(country_path)
    os.mkdir(country_path)

    if os.path.exists("1_"+country_path):
        shutil.rmtree("1_" + country_path)
    os.mkdir("1_"+country_path)

    letters, city_qty = parsing.get_city_letters(country, good_proxies)
    city_qty = int(city_qty.text.replace("/ ", "").strip())
    count_downloads = 0
    for letter in letters:



        #cityHrefs = get_country_city_href(country, "B", good_proxies)  # вариант для  парсинга буквы
        cityHrefs = parsing.get_country_city_href(country, letter, good_proxies) #вариант для  парсинга страны
        #cityHrefs = get_country_city_href(countries[countryIndex], letter) #вариант для полного парсинга
        letter_path = country_path+"/"+letter+"_cities"
        if os.path.exists(letter_path):
            shutil.rmtree(letter_path)
        os.mkdir(letter_path)

        if os.path.exists("1_"+letter_path):
            shutil.rmtree("1_" + letter_path)
        os.mkdir("1_" + letter_path)

        city_index = 0
        for cityHref in cityHrefs:
            #city_name = get_full_city_name(cityHrefs[2])
            #city_name = get_full_city_name_and_coords(cityHref,good_proxies)  # старый вариант рабочий

            # пропуск загруженных кроме последнего города
            # получить количество папок
            # !!!! убрать удаление папки!!!!
            l_dir = len(os.listdir(letter_path))
            if city_index < l_dir-1:
                city_index+=1
                continue
            #============Работа над ресторанами в текущем городе ============
            city_guru = city.City(cityHref, country, good_proxies)  # новый вариант через структуру тоже рабочий
            city_path = letter_path+"/"+city_guru.latinName
            #добавление папки города
            if os.path.exists(city_path):
                shutil.rmtree(city_path)
            os.mkdir(city_path)

            """
            if os.path.exists("1_"+city_path):
                shutil.rmtree("1_" + city_path)
            os.mkdir("1_"+city_path)
            """

            city_guru_href = prepare_city_href(city_guru.href)  # получаем ссылку на город и меняем ее для доступа ко всем ресторанам
            tags_with_data_pagenumber = parsing.get_soup(city_guru_href, good_proxies).find_all(attrs={"data-pagenumber": True})  # получаем ссылки для автоскролла
            pages_for_city = []
            for i in range(0,len(tags_with_data_pagenumber)):
                pages_for_city.append(city_guru_href+"/"+str(i))

            # обход по всем ссылкам внутри города и получение ссылок ресторанов
            restraunts_href_from_city = set()
            for page in pages_for_city:
                rest_countainer = parsing.get_soup(page,good_proxies).find("div", class_="restaurant_container")
                restraunt_guru_hrefs_from_page= rest_countainer.findAll("a")
                for restraunt_guru_href in restraunt_guru_hrefs_from_page:
                    rest_href = restraunt_guru_href.get("href")
                    restraunts_href_from_city.add(rest_href)


            #работа над сссылками ресторанов в городе(парсинг ресторана)
            # пункт РАБОТА НАД ПАРСИНГОМ РЕСТОРАНОВ
            rest_names_list = []
            for rest_href in restraunts_href_from_city:
                json_object = parsing.get_json_restraunt(rest_href, good_proxies)
                if json_object != "no_json":
                    rest_guru_json_object = json.loads(json_object)
                else:
                    f = open("log.txt","a", encoding="UTF-8")
                    f.write(f"{rest_href} bad restraunt - no json\n")
                    f.close()
                    continue
               # rest_guru_json_object = json.loads( parsing.get_json_restraunt("https://restaurantguru.com/Osteria-La-Baracca-Frydek-Mistek", good_proxies)) # пример для разработки
                rest_guru_json_object["features"] = prepare_features(rest_guru_json_object["features"])
                restraunt_object = restraunt_guru.Restraunt_from_guru(rest_guru_json_object, 0)
                #rest_path = city_path + "/" + restraunt_object.name # name сделать проверку на повторы name
                rest_path = city_path + "/" + restraunt_object.latin_name # name сделать проверку на повторы name
                # добавление папки ресторана
                if os.path.exists(rest_path):
                    shutil.rmtree(rest_path)
                os.mkdir(rest_path)
                menu_status = parsing.get_menu(restraunt_object.menu_href, rest_path, good_proxies)
                # если меню нет-> прерываем этот ресторан # удаление папки с рестораном происходит сразу внутри функции скачивания меню
                if menu_status=="no_menu":
                    f = open("log.txt", "a", encoding="UTF-8")
                    f.write(f"{rest_href} bad restraunt - no menu\n")
                    f.close()
                    continue

                # заполнение папки с рестораном ----->>>  создание файла с рестораном
                # реализация проверки повторов
                # собираем количество использований городов
                flag = False
                for names in rest_names_list:
                    if names["name"] == restraunt_object.latin_name:
                        names["used"] += 1
                        restraunt_object.latin_name = restraunt_object.latin_name + ">" + str(names["used"])
                        restraunt_object.network = restraunt_object.latin_name
                        flag = True
                if flag == False:
                    latin_names_dict = {
                        "name": restraunt_object.latin_name,
                        "used": 0
                    }
                    rest_names_list.append(latin_names_dict)


                if restraunt_object.inst_url != "":
                    #insta_parsing.get_album(restraunt_object.inst_url,rest_path)
                    #restraunt_object.last_publication = insta_parsing.get_last_publication(restraunt_object.inst_url)
                    restraunt_object.last_publication = insta_parsing.get_album_and_last_publication_pikacu(restraunt_object.inst_url,rest_path)
                tabler_to_guru_json = restraunt_object.get_json()
                if tabler_to_guru_json != "":
                    print(tabler_to_guru_json)
                    rest_file = open(rest_path+ "/json.txt", "w", encoding="UTF-8")  # 1_ для того чтобы писать города в отдельные страны
                    rest_file.write(json.dumps(tabler_to_guru_json, ensure_ascii=False, indent = 4))
                    rest_file.close()
                    counter_restraunt += 1
                    print(f"good restraunts = {counter_restraunt}")
                    f_rest = open("log.txt", "a", encoding="UTF-8")
                    f_rest.write(f"{rest_href} good restraunt - downloaded\n")
                    f_rest.close()
                    if counter_restraunt == 100:
                        exit(1)
                else:
                    f_rest = open("log.txt", "a", encoding="UTF-8")
                    f_rest.write(f"{rest_href} bad restraunt - no good json\n")
                    f_rest.close()


            # собираем количество использований городов
            flag = False
            for names in latin_names_list:
                if names["name"] == city_guru.latinName:
                    names["used"] += 1
                    city_guru.latinName = city_guru.latinName+"-"+str(names["used"])
                    flag = True
            if flag == False:
                latin_names_dict = {
                    "name": city_guru.latinName,
                    "used": 0
                }
                latin_names_list.append(latin_names_dict)


            city_file = open("1_"+city_path+".txt", "a", encoding="UTF-8")  # 1_ для того чтобы писать города в отдельные страны
            #city_file = open(country+"/"+ letter+"-cities.txt", "a", encoding="UTF-8") ###### рабочий вариант, обновили версией где все сразу записывается

          #  city_file = open(letter + "-cities.txt", "a", encoding="UTF-8")
            #  city_file.write(city_name+"\n")
            city_file.write(json.dumps(city_guru.get_json(), ensure_ascii=False)+"\n")
            counter += 1
            # print(f"{city_name}   ====> {counter}")
            print(f"{json.dumps(city_guru.get_json(), ensure_ascii=False )}   ====> {counter} , { str(counter/city_qty*100)[:6] }% in {country}")
            city_file.close()


pass