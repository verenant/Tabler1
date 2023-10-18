


import bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import requests
import random
from pdf2image import convert_from_path
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
        self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
        self.Coordinates = get_coordinates(self.soup)
        self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)
        self.menu = get_menu(self.soup, self.additional_url)

    def printRest(self):
        print(f"{self.name} , {self.phone} , {self.avg_check}" )


#Описание
def get_description(soup):
    #description = soup.find(class_='expandable-text__t').find("p").text
    description = soup.find(class_='expandable-text__t').text
    if description:
        return description
    else:
        return "no_description"
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
    else:
        return "no_avg_check"


# Режим работы
def get_timetable(soup):
    get_timetable_from_soup = soup.find("h2",text = re.compile("Время работы"))
    if get_timetable_from_soup:

        timetable = get_timetable_from_soup.find_parent().find_parent().find("ul").text
        return timetable
    else:
        return "no_timetable"

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
    if not(get_main_image is None):
        #если у get_main_image перед /uploads есть base_url(restoclub.ru), то его чистим
        if ".ru/" in get_main_image:
            get_main_image = get_main_image[get_main_image.find("/")+2:]
            get_main_image = get_main_image[get_main_image.find("/"):]

        main_image_url = main_url+get_main_image
        main_image_jpeg = requests.get(main_image_url, headers = headers)
        #response = requests.get(url)
        if main_image_jpeg.status_code == 200:
            jpeg_name = addUrl[addUrl.rfind("/")+1:]+"+"
            with open(jpeg_name + "main_image.jpg", 'wb') as f:
                f.write(main_image_jpeg.content)
        #download_wget(main_image_url)  # https://www.restoclub.ru/uploads/place_thumbnail_big/d/9/6/e/d96e3f0f868f21b03f2a50ecbb621b41.jpg
        return jpeg_name + "main_image.jpg"  #main_image_url
    else:
        return "no_main_image"

def get_album(soup,main_url,headers,addUrl):
    div_slide_images = soup.findAll("div", class_="slide")
    if not (div_slide_images is None):
        i = -1
        for div in div_slide_images:
            image = div.find("a").get("data-src")
            if image == '':
                image = div.find("img").get("src")



            if not (image is None):
                # очистка от restoclub.ru
                if ".ru/" in image:
                    image = image[image.find("/") + 2:]
                    image = image[image.find("/"):]

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

        return "complete"
    else:
        return "no_album"
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

def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)


def get_menu(soup,addUrl):
    menu_link_list = soup.findAll("a", class_ ="file-link")
    if menu_link_list:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',

        ]
        print(menu_link_list)
        for link in menu_link_list:
            agent = random.choice(user_agent_list)
           # print(agent)
            headers = {
                "User-Agent": agent
            }
            #socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
           # socket.socket = socks.socksocket
           # checkIP()
            url = "https://www.restoclub.ru" + link.get("href")
            req = requests.get(url, headers = headers)
            src = req.text
            menu_soup = BeautifulSoup(src, "html.parser")
            pdf_link = "https://www.restoclub.ru" + menu_soup.find("a", class_="load-menu-link").get("href")
            pdf = open("pdf" + "test" + ".pdf", "wb")
            responce_menu = requests.get(pdf_link)
            print(responce_menu)
            pdf.write(responce_menu.content)
            pdf.close()
            #укажите свой путь к poppler`y чтобы работало
            images = convert_from_path("pdftest.pdf", 500, poppler_path=r"J:\poppler-23.08.0\Library\bin")
            for i in range(len(images)):
                # Save pages as images in the pdf
                images[i].save(addUrl[addUrl.rfind("/") + 1:] + "+" +link.find("span",class_ ="file-link__name").text + str(i) + '.jpg', 'JPEG')
            time.sleep(3)
        return "complete"
    else:
        return "no_menu"
