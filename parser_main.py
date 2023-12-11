import ipaddress
import json
import os
import random
import time

import bs4
import requests
import parsing
import city
import restraunt_guru


def prepare_city_href(href):
    new_href_slash_index = href.rfind("/")+1
    city_end = href[new_href_slash_index:]
    new_href = href.replace(city_end, "restaurant-"+city_end+"-t1")
    return new_href



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
proxies_from_network = parsing.get_new_proxies() # получение бесплатных прокси
######get_good_proxies(main_page,proxies_from_network) #составление файла с хорошими прокси
#countries = get_countries(main_page)
countries = parsing.get_countries()
counter = 0

latin_names_list = []

#заполнение ресторана, потом переместить в пункт РАБОТА НАД ПАРСИНГОМ РЕСТОРАНОВ
rest_guru_json_object = json.loads(parsing.get_json_restraunt("https://restaurantguru.com/La-Farma-Prague",good_proxies))
restraunt_object = restraunt_guru.Restraunt_from_guru(rest_guru_json_object,0)



for countryIndex in range(1,2): # не через in чтобы пропустить Алеутские острова # поменять на len(countries) при запуске на все страны
    #letters = get_city_letters(countries[4])
    #letters = get_city_letters
    country = "Czech-Republic" #countries[countryIndex] # при полном парсинге городов
    if os.path.isdir(country) == False:
        os.mkdir(country)
    letters, city_qty = parsing.get_city_letters(country,good_proxies)
    city_qty = int(city_qty.text.replace("/ ","").strip())
    for letter in letters:
        #cityHrefs = get_country_city_href(country, "B", good_proxies)  # вариант для  парсинга буквы
        cityHrefs = parsing.get_country_city_href(country,letter,good_proxies) #вариант для  парсинга страны
        #cityHrefs = get_country_city_href(countries[countryIndex], letter) #вариант для полного парсинга
        for cityHref in cityHrefs:
            #city_name = get_full_city_name(cityHrefs[2])
            #city_name = get_full_city_name_and_coords(cityHref,good_proxies) # старый вариант рабочий

            #============Работа над ресторанами в текущем городе ============

            city_guru = city.City(cityHref,country,good_proxies) # новый вариант через структуру тоже рабочий
            city_guru_href = prepare_city_href(city_guru.href) # получаем ссылку на город и меняем ее для доступа ко всем ресторанам
            tags_with_data_pagenumber = parsing.get_soup(city_guru_href,good_proxies).find_all(attrs={"data-pagenumber": True}) # получаем ссылки для автоскролла
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
            for rest_href in restraunts_href_from_city:
                rest_guru_object = json.loads(parsing.get_json_restraunt(rest_href,good_proxies))
                pass






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

            city_file = open(country+"/"+ letter+"-cities.txt", "a", encoding="UTF-8")

          #  city_file = open(letter + "-cities.txt", "a", encoding="UTF-8")
            #  city_file.write(city_name+"\n")
            city_file.write(json.dumps(city_guru.get_json() , ensure_ascii=False)+"\n")
            counter+=1
            # print(f"{city_name}   ====> {counter}")
            print(f"{json.dumps(city_guru.get_json() , ensure_ascii=False )}   ====> {counter} , { str(counter/city_qty*100)[:6] }% in {country}")
            city_file.close()



pass