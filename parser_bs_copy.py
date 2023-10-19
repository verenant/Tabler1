import bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import requests
import wget
from PIL import Image
import urllib.request
from restraunt import Restraunt
main_page_1 = "https://www.restoclub.ru/msk/search/1?expertChoice=false&types%5B%5D=3&types%5B%5D=30&types%5B%5D=23&types%5B%5D=38&types%5B%5D=16&types%5B%5D=46&types%5B%5D=2&types%5B%5D=33&types%5B%5D=7&types%5B%5D=14&types%5B%5D=4&types%5B%5D=24&types%5B%5D=15&types%5B%5D=39&types%5B%5D=1&types%5B%5D=17&types%5B%5D=37&types%5B%5D=22&types%5B%5D=13&types%5B%5D=25"
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

i=0

with open("add_links.txt", "w") as f:
    for rest in li:

            get_div= rest.find("div")
            if not(get_div is None):

                get_data_href = get_div.get("data-href")
                if not(get_data_href is None):
                    i+=1
                    f.write(get_data_href+"\n")
                    additional_links.append(get_data_href)
                if i>10:
                    break


for link in additional_links:
   # rest = Restraunt(main_url_msk,"place/dymzavod-rassvet",headers)
   rest = Restraunt(main_url,link, headers)
   rest.printRest()
   pass

#Albums
