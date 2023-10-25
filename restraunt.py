import PIL.Image
import bs4
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import re
import requests
import os
import glob
import random
from pdf2image import convert_from_path
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import wget
from PIL import Image
import json
import urllib.request
Image.MAX_IMAGE_PIXELS = None


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

    def __init__(self,main_url,additional_url, headers, typeOfConstructor ):
        if typeOfConstructor == 0: # для парсинга
            self.main_url = main_url
            self.headers = headers
            self.additional_url = additional_url
            self.soup = get_soup(self.main_url + self.additional_url,headers)
            self.name = get_name(self.soup)
            self.description = get_description(self.soup)
            #self.driver = create_driver(self.main_url + self.additional_url)
            self.phone = get_phone(self.soup, self.main_url + self.additional_url)
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
        if typeOfConstructor == 1: #для json
            addUrl = additional_url[additional_url.rfind("/") + 1:]
            j = get_json(addUrl)
            self.__dict__ = json.loads(j)

    def printRest(self):
        print(f"{self.name} , {self.phone} , {self.avg_check}" )

def get_json(filename):
    with open("jsons/"+filename, encoding="utf8") as f:
        return f.read()
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
#сделать нет телефона
def create_driver(url):
    # options = webdriver.ChromeOptions()
    # options.add_argument(
    #     "user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36")
    # # options.add_argument("--disable-blink-feaures=AutomationControlled")
    # headers = {
    #
    #                     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #                     'Accept-Encoding': "gzip, deflate, br",
    #                     "Accept-Language": "ru,en;q=0.9",
    #                     "Cache-Control": "max-age=0",
    #                     "Referer":url,
    #                     "Sec-Ch-Ua":' "Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    #                     "Sec-Fetch-User": "?1",
    #                     "Sec-Fetch-Site":"same-origin",
    #                     "Upgrade-Insecure-Requests":"1",
    #                     "Cookie":'__ddg1_=bVfoar7vIFWeBimtByJh; PHPSESSID=3bv61h771pd42d35m0ojm33ip0; device_view=full; g_state={"i_p":1697482304790,"i_l":2}'
    #
    #                 }
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(url)


    return driver


def get_phone(soup, url):
    phone = soup.find(class_='place-phone__text')
    if not(phone is None) :

        #phone = soup.find(class_='place-phone').find("a").get("content")
        phone = phone.text
        phone = phone[:-1]
        driver = webdriver.Chrome()
        driver.get(url)
        hidden_phone = driver.find_element(By.CLASS_NAME,"place-phone__number")
        driver.execute_script("")
        hidden_phone.click()
        if (phone is None) or hidden_phone:

            try:

                hidden_phone.click()
                time.sleep(5)
            except selenium.common.exceptions.SessionNotCreatedException:
              #  f = open("temp.txt", "a")
               # f.write(dir_path + "\n" + "   sessionError")
                return










            return "no_phone"
        else:
            return phone
    else:
        return "no_phone"

# Адрес
def get_address(soup):
    #address = soup.find(attrs={"data-popup": "map"}).text
    address = soup.find(attrs={"data-popup": "map"})
    if address:
        address = address.text
        return address
    else:
        return "no_address"

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
    category = soup.find("div", class_= "place-title__type")
    if category:
        category = category.text
        return category
    else:
        return "no_category"

# images = #ссылки
def get_image(soup,main_url,headers,addUrl):
    get_main_image = soup.find("div", class_="gallery__main").find("img")
    if not(get_main_image is None):
        get_main_image = get_main_image.get("src")
        #get_main_image = soup.find("div", class_="gallery__main").find("img").get("src")
        dir_path = "Main_photo/" + addUrl[addUrl.rfind("/") + 1:]
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        if not(get_main_image is None):
            #если у get_main_image перед /uploads есть base_url(restoclub.ru), то его чистим
            if ".ru/" in get_main_image:
                get_main_image = get_main_image[get_main_image.find("/")+2:]
                get_main_image = get_main_image[get_main_image.find("/"):]

            main_image_url = main_url+get_main_image
            main_image_jpeg = requests.get(main_image_url, headers = headers)
            #response = requests.get(url)
            jpeg_name = addUrl[addUrl.rfind("/") + 1:] + "+"
            if main_image_jpeg.status_code == 200:

                with open(dir_path + "/" +  "main_image.jpg", 'wb') as f:
                    f.write(main_image_jpeg.content)
            #download_wget(main_image_url)  # https://www.restoclub.ru/uploads/place_thumbnail_big/d/9/6/e/d96e3f0f868f21b03f2a50ecbb621b41.jpg
            return jpeg_name + "main_image.jpg"  #main_image_url
        else:
            return "no_main_image"

def get_album(soup,main_url,headers,addUrl):
    div_slide_images = soup.findAll("div", class_="slide")
    dir_path = "Album/" + addUrl[addUrl.rfind("/") + 1:]
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
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
                    with open(dir_path + "/" +str(i)+".jpg", 'wb') as f:
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
    #data_longitude = soup.find("div", class_="place-map maps-on").get("data-longitude")
    #data_latitude = soup.find("div", class_="place-map maps-on").get("data-latitude")
    data_longitude = coords1.get("data-longitude")
    data_latitude = coords1.get("data-latitude")
    return data_latitude,data_longitude

def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)


def get_menu(soup,addUrl,driver):
    menu_link_list = soup.findAll("a", class_ ="file-link")
    dir_path = "Menu/" + addUrl[addUrl.rfind("/") + 1:]
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    if menu_link_list:
        user_agent_list = [
          #  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',

        ]
        #print(menu_link_list)
        for link in menu_link_list:
            if not os.path.isdir(dir_path + link.find("span",class_ ="file-link__name").text):
                try:
                    os.mkdir(dir_path + "/" +  link.find("span",class_ ="file-link__name").text)
                except :
                    print("someError:" + dir_path + "/" +  link.find("span",class_ ="file-link__name").text )

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
           # pdf_link = "https://www.restoclub.ru" + menu_soup.find("a", class_="load-menu-link").get("href")
            if not(menu_soup.find("a", class_="load-menu-link") is None):
                    pdf_link = "https://www.restoclub.ru" + menu_soup.find("a", class_="load-menu-link").get("href")
                    pdf = open("pdf" + "test" + ".pdf", "wb")


                    # s = requests.Session()
                    # s.headers.update({'referer': my_referer})
                    # s.get(url)


                    headers.update({

                        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Encoding': "gzip, deflate, br",
                        "Accept-Language": "ru,en;q=0.9",
                        "Cache-Control": "max-age=0",
                        "Referer":url,
                        "Sec-Ch-Ua":' "Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Site":"same-origin",
                        "Upgrade-Insecure-Requests":"1",
                        "Cookie":'__ddg1_=bVfoar7vIFWeBimtByJh; PHPSESSID=3bv61h771pd42d35m0ojm33ip0; device_view=full; g_state={"i_p":1697482304790,"i_l":2}'

                    })

                    binary_yandex_driver_file = "yandexdriver.exe"  # path to YandexDriver

                    responce_menu = requests.get(pdf_link,headers)

                    pdf.write(responce_menu.content)
                    pdf.close()
                    print(f" {addUrl} ,{responce_menu.status_code} ")
                    images = False
                    if responce_menu.status_code != 200:
                        # если спарсить не дали, то пробуем selenium
                        try:
                            options = webdriver.ChromeOptions
                            options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36")
                            options.add_argument("--disable-blink-feaures=AutomationControlled")

                            #driver = webdriver.Chrome(options=options)
                            stealth(driver,
                                    language=["en-US","en"],
                                    vendor = "Google Inc.",
                                    platform="Win32",
                                    webgl_vendor="Intel Inc",
                                    renderer="Intel Iris OpenGl Engine",
                                    fix_hair_line=True,
                                    )

                        except selenium.common.exceptions.SessionNotCreatedException:
                            f = open("temp.txt", "a")
                            f.write(dir_path + "\n" + "   sessionError")
                            return
                        driver.get(url)
                        time.sleep(5)
                        download_menu = driver.find_element(By.CSS_SELECTOR, "a.load-menu-link")
                        if download_menu:
                            download_menu.click()
                        else:
                            #div class="image-wrap" img src
                         #   responce_menu
                            # Меню есть, но некоторые в виде картинок, а не которые как пдф
                            # здесь обработка части с картинками
                            image_menu = BeautifulSoup(responce_menu.text,"html.parser").find("div", class_= "image-wrap").find("img").get("src")
                            cleanURL(image_menu)
                            with open(dir_path + "/" + image_menu + ".jpg", 'wb') as f:
                                f.write(image_menu.content)



                            pass
                        time.sleep(5)
                        list_of_files = glob.glob('C:/Users/Admin/Downloads/*')
                        latest_file = max(list_of_files, key=os.path.getctime)
                        try:
                            images = convert_from_path(latest_file,500, poppler_path=r"G:\poppler-23.08.0\Library\bin")
                        except PIL.Image.DecompressionBombError:

                            f = open("temp.txt", "a")
                            f.write(download_menu +" " + dir_path + "   image" + "\n")
                            return


                        os.remove(latest_file)

                    #укажите свой путь к poppler`y чтобы работало
                    if images == False:
                        images = convert_from_path("pdftest.pdf", 500, poppler_path=r"G:\poppler-23.08.0\Library\bin")
                    for i in range(len(images)):
                            # Save pages as images in the pdf
                        try:
                            images[i].save(dir_path + "/" + link.find("span",class_ ="file-link__name").text + "/" + str(i) + '.jpg', 'JPEG')
                        except:
                            file = open("temp.txt", "a")
                            file.write(f"Слишком большое пдф изображение на странице:{addUrl}, не разбито на страницы \n")
                    time.sleep(3)
            # меню в виде изображений
            elif not (menu_soup.find("div", class_="image-menu-wrap") is None):
                div_menu = menu_soup.find("div", class_="image-menu-wrap")
                menu = div_menu.find("img").get("src")
                if ".ru/" in menu:
                    menu = menu[menu.find("/") + 2:]
                    menu = menu[menu.find("/"):]

                menu_image_url = "https://www.restoclub.ru" + menu
                menu_image_jpeg = requests.get(menu_image_url, headers=headers)
                # response = requests.get(url)
                if menu_image_jpeg.status_code == 200:
                    jpeg_name = addUrl[addUrl.rfind("/") + 1:]

                    with open(dir_path + "/" + link.find("span",class_ ="file-link__name").text + "/" + "0" +".jpg", 'wb') as f:
                        f.write(menu_image_jpeg.content)

                # меню в виде изображений SVG


                pass
        return "complete"
    else:
        return "no_menu"


def cleanURL(url):
    if ".ru/" in url:
        url = url[url.find("/") + 2:]
        tidyUrl = url[url.find("/"):]
    return tidyUrl