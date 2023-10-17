


import bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import requests
import wget
from PIL import Image
import urllib.request


# версия без скачанной страницей (с подгружаемой на лету)
def get_soup(url,headers):
    res = requests.get(url, headers = headers)
    return bs4.BeautifulSoup(res.text,"html.parser")

class Restraunt():
    name = ""
    additional_url = ""
    description = ""
    phone = ""
    address = ""
    avg_check = ""
    timetable = ""
    features =[]
    kitchen = []
    category = ""
    main_image_url = ""
    Coordinates = []
    soup = bs4.BeautifulSoup()

    def __init__(self,main_url,additional_url, headers):
        self.main_url = main_url
        self.headers = headers
        self.additional_url = additional_url
        self.soup = get_soup(self.main_url + self.additional_url,headers)
        self.name = get_name(self.soup)
        self.description = get_description(self.soup)
        self.phone = get_phone(self.soup)
        self.address = get_address(self.soup)
        self.avg_check = get_avg_check(self.soup)
        self.timetable = get_timetable(self.soup)
        self.features = get_features(self.soup)
        self.kitchen = get_kitchen(self.soup)
        self.category = get_category(self.soup)
      #  self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
        self.Coordinates = get_coordinates(self.soup)
      #  self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)

    def printRest(self):
        print(f"{self.name} , {self.phone} , {self.avg_check}" )


#Описание
def get_description(soup):
    #description = soup.find(class_='expandable-text__t').find("p").text
    description = soup.find(class_='expandable-text__t').text
    return description
#Имя
def get_name(soup):
    name = soup.find("div", class_="place-title__header").text
    return name


# Телефон
def get_phone(soup):
    phone = soup.find(class_='place-phone').find("a").get("content")
    return phone

# Адрес
def get_address(soup):
    address = soup.find(attrs={"data-popup": "map"}).text
    return address

# Средний чек (бывает, что не указан)
def get_avg_check(soup):
    if (soup.find("h2",text = re.compile("Средний чек"))):
        find_h_div_by_text = soup.find("h2",text = re.compile("Средний чек")).find_parent().find_parent()
        avg_check = find_h_div_by_text.find("div").find("span").text.strip()
        return avg_check


# Режим работы
def get_timetable(soup):
    get_timetable_from_soup = soup.find("h2",text = re.compile("Время работы")).find_parent().find_parent()
    timetable = get_timetable_from_soup.find("ul").text
    return timetable

# Особенности
def get_features(soup):
    features_list = soup.findAll("li", class_="place-description__feature")
    features = []
    for feature in features_list:
        features.append(feature.text)
    return features

#кухня # kitchen =
def get_kitchen(soup):
   # get_kitchens = soup.find("div",class_ = "info__header", text = re.compile("Кухня")).find_parent().find_parent()
    kitchen_list = soup.findAll("a", class_="cuisine link _untrack")
    kitchens = []
    for kitchen in kitchen_list:
        kitchens.append(kitchen.text)
    kitchens = set(kitchens)
    return kitchens

#категория
def get_category(soup):
    category = soup.find("div", class_= "place-title__type").text
    return category


# images = #ссылки
def get_image(soup,main_url,headers,addUrl):
    get_main_image = soup.find("div", class_="gallery__main").find("img").get("src")

    main_image_url = main_url+get_main_image
    main_image_jpeg = requests.get(main_image_url, headers = headers)
    #response = requests.get(url)
    if main_image_jpeg.status_code == 200:
        jpeg_name = addUrl[addUrl.rfind("/")+1:]+"+"
        with open(jpeg_name + "main_image.jpg", 'wb') as f:
            f.write(main_image_jpeg.content)
    #download_wget(main_image_url)  # https://www.restoclub.ru/uploads/place_thumbnail_big/d/9/6/e/d96e3f0f868f21b03f2a50ecbb621b41.jpg
    return jpeg_name + "main_image.jpg"  #main_image_url

def get_album(soup,main_url,headers,addUrl):
    div_slide_images = soup.findAll("div", class_="slide")
    i = -1
    for div in div_slide_images:
        image = div.find("a").get("data-src")
        if not (image is None):
            main_image_url = main_url + image
            main_image_jpeg = requests.get(main_image_url, headers=headers)
            # response = requests.get(url)

            if main_image_jpeg.status_code == 200:
                jpeg_name = addUrl[addUrl.rfind("/") + 1:] + "+"
                i += 1
                if i==0:
                    continue
                with open(jpeg_name + str(i)+".jpg", 'wb') as f:
                    f.write(main_image_jpeg.content)
        if i == 10:
            break
        # download_wget(main_image_url)  # https://www.restoclub.ru/uploads/place_thumbnail_big/d/9/6/e/d96e3f0f868f21b03f2a50ecbb621b41.jpg
      # main_image_url

    #координаты
def get_coordinates(soup):
    coords1 = soup.find("footer", id="great-footer").findChild("div").findChild("div")
    coords = coords1.find("div", class_="place-map maps-on")
  #  data_longitude = soup.find("div", class_="place-map maps-on").get("data-longitude")
   # data_latitude = soup.find("div", class_="place-map maps-on").get("data-latitude")
    data_longitude = coords1.get("data-longitude")
    data_latitude = coords1.get("data-latitude")
    return data_latitude,data_longitude



