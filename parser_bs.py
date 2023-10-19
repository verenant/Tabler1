import shutil

import bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import requests
import wget
import json
import jsons
from PIL import Image
import urllib.request

from restraunt import Restraunt
import glob
import os

try:
    shutil.rmtree("Album")
except:
    print("no dir Album")
try:
    shutil.rmtree("Jsons")
except:
    print("no dir Jsons")
try:
    shutil.rmtree("Main_photo")
except:
    print("no dir Main_photo")
try:
    shutil.rmtree("Menu")
except:
    print("no dir Menu")


#запускать с конца
i=2
while i != 10:
    main_page_1 = "https://www.restoclub.ru/msk/search/"+str(i)+"?expertChoice=false&types%5B%5D=3&types%5B%5D=30&types%5B%5D=23&types%5B%5D=38&types%5B%5D=16&types%5B%5D=46&types%5B%5D=2&types%5B%5D=33&types%5B%5D=7&types%5B%5D=14&types%5B%5D=4&types%5B%5D=24&types%5B%5D=15&types%5B%5D=39&types%5B%5D=1&types%5B%5D=17&types%5B%5D=37&types%5B%5D=22&types%5B%5D=13&types%5B%5D=25"
    main_url = "https://www.restoclub.ru"
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}
    """
    # версия со скачанной страницей
    
    with open("rassvet.html", encoding="UTF-8") as f:
        src = f.read()
    #soup = BeautifulSoup(src, "lxml")
    """

    # версия без скачанной страницей (с подгружаемой на лету)
    def get_soup(url):
        res = requests.get(url,headers = headers)
        return bs4.BeautifulSoup(res.text,"html.parser")

    def download_wget(url=''):
        wget.download(url=url)

    #получение коротких ссылок (URL) всех ресторанов на странице
    soup_main = get_soup(main_page_1)
    ul_links = soup_main.find( "ul" , class_="page-search__list")
    li = ul_links.findAll("li")
    additional_links = []
    if not os.path.isdir("Jsons"):
        os.mkdir("Jsons")
    if not os.path.isdir("Main_photo"):
        os.mkdir("Main_photo")
    if not os.path.isdir("Menu"):
        os.mkdir("Menu")
    if not os.path.isdir("Album"):
        os.mkdir("Album")


    with open("add_links.txt", "w") as f:
        for rest in li:
                get_div= rest.find("div")
                if not(get_div is None):
                    get_data_href = get_div.get("data-href")
                    if not(get_data_href is None):
                        f.write(get_data_href+"\n")
                        additional_links.append(get_data_href)


        """
     #Временная заглушка для проверки работы с ссылками, чтобы не закидывать сервер запросами
     """
    """"
    with open("add_links.txt") as fileLinks:
        additional_links = fileLinks.readlines()
    """


    # обход всех ресторанов с текущей страницы и создание обьекта Restraunt и его json
    # (с ограничением в несколько файлов link[:-1] для работы с ссылками файлов, которые берутся из файла add_links.txt)
    j=0
    for link in additional_links:
        rest = Restraunt(main_url,"/msk/place/fabrika-andy",headers)
       # rest = Restraunt(main_url,"/msk/place/steak-it-easy-3",headers)
        #rest = Restraunt(main_url,link, headers)
        j +=1
        rest_name = link[link.rfind("/") + 1:]
        with open("Jsons/" + rest_name +".json","w",encoding='UTF-8') as rest_JSON_file:
            w = jsons.dump(rest)

            w.pop('soup')
            w.pop('headers')
            json.dump(w, rest_JSON_file,indent = 4, ensure_ascii=False)
           # rest_JSON_file.write(w)
            rest.printRest()
    i += 1
    if i>2:
        break
    pass


