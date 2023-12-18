import json
import random
import shutil
import time
from instagrapi import Client
import requests
from requests.auth import HTTPProxyAuth
import os
import PIL.Image
import bs4
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import re
from seleniumwire import webdriver



headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36",
    "X-IG-App-ID": "936619743392459" # 
}

proxy_server = "http://TyKxFA:tdnG0H@200.71.127.109:9164"
proxy_server_for_inst = "http://ec675777:6656af7e7c@45.134.28.7:30010"
proxies = {
    "https": proxy_server_for_inst,
    "http": proxy_server_for_inst,
}


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
    try:
        options = webdriver.ChromeOptions
        options.add_argument(
            "user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36")
        options.add_argument("--disable-blink-feaures=AutomationControlled")

        # driver = webdriver.Chrome(options=options)
        stealth(driver,
                language=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc",
                renderer="Intel Iris OpenGl Engine",
                fix_hair_line=True,
                )

    except selenium.common.exceptions.SessionNotCreatedException:
        #f = open("temp.txt", "a")
        # f.write(dir_path + "\n" + "   sessionError")
        pass
        #return
    url = "https://insta-stories-viewer.com/ohota_auto/"
    driver.get(url)
    time.sleep(5)




def get_proxy():
    f = open("proxy.txt")
    proxies = f.readlines()
    r = random.randint(0,len(proxies)-2)

    proxy = {
        "https": proxies[r].strip(),
        "http": proxies[r].strip(),
    }
    return proxy

def get_album1(inst_restraunt,album_path):
    # Заменить restraunt на настоящий
    album_path = album_path + "/Restraunt/Album"

    # if os.path.exists(album_path):
    #    shutil.rmtree(album_path)

    # делаем новую папку
    os.mkdir(album_path)

    proxy_server = get_proxy()

    driver = webdriver.Chrome(seleniumwire_options=proxy_server)


    # Возможно нужно будет добавить подбор прокси сервер для открытия ссылки на инстаграмм
    #driver = webdriver.Chrome()
    driver.maximize_window()
    #driver.get("https://insta-stories-viewer.com/ohota_auto/")
    driver.get("https://instanavigation.com/en/user-profile/"+inst_restraunt[1:])
    #time.sleep(1.0)
    #element = driver.find_element(By.CLASS_NAME,"profile-publications__btn")
    element = driver.find_element(By.CSS_SELECTOR, "div.profile-publications__btn")
    #бывает, что не кликает надо подождать тогда подольше!
    element.click()
    # бывает, что не загружает надо подождать тогда подольше!
    time.sleep(5.0)

    html_text = driver.page_source
    photo_page = bs4.BeautifulSoup(html_text, "html.parser")
    posts_table = photo_page.find("div", id= "posts")
    posts = posts_table.findAll("div")
    i = 0
    for image in posts:
        image_href = image.find("img").get("data-src")
        if image_href:
            ok = False
            random_proxy = get_proxy()
            #подбираем прокси сервер для скачивания изображений, до тех пор пока оно не будет скачано
            while not(ok):
                try:
                    image_jpeg = requests.get(image_href, headers=headers, proxies = random_proxy, timeout=6)
                except requests.exceptions.ReadTimeout:
                    print(f"  proxies_during_downloading_inst_img ->> BLOCKED = {random_proxy['http']}")
                if image_jpeg.status_code == 200:
                    with open(album_path+"/"+str(i) + ".jpg", 'wb') as f:
                        f.write(image_jpeg.content)
                        ok = True
                        i += 1
            if i == 10:
                break
    last_publication_text = posts[0].find("p",class_="text-dark mt-1").text
    return last_publication_text


def get_album(inst_restraunt,album_path):
    # Заменить restraunt на настоящий
    album_path = album_path + "/Album"

    if os.path.exists(album_path):
        shutil.rmtree(album_path)
    # делаем новую папку
    os.mkdir(album_path)

    selenium_ok = False
    proxy_server = get_proxy()
    driver = webdriver.Chrome(seleniumwire_options=proxy_server)
    # Возможно нужно будет добавить подбор прокси сервер для открытия ссылки на инстаграмм

    driver.get("https://insta-stories-viewer.com/"+inst_restraunt[1:])
    time.sleep(1.5)
    element = driver.find_element(By.PARTIAL_LINK_TEXT, "Publications")
    element.click()
    time.sleep(1.5)
    html_text = driver.page_source
    photo_page = bs4.BeautifulSoup(html_text, "html.parser")
    posts = photo_page.find("ul", class_= "profile__tabs-media profile__posts")
    images_table = posts.findAll("img")
    i = 0
    for image in images_table:
        image_href = image.get("data-src")
        if image_href:
            ok = False
            random_proxy = get_proxy()
            #подбираем прокси сервер для скачивания изображений, до тех пор пока оно не будет скачано
            while not(ok):
                image_jpeg = ""
                try:
                    image_jpeg = requests.get(image_href, headers=headers, proxies = random_proxy, timeout=6)
                except requests.exceptions.ReadTimeout:
                    print(f"  proxies_during_downloading_inst_img ->> BLOCKED = {random_proxy['http']}")
                #image_jpeg = requests.get(image_href, headers=headers, proxies = random_proxy, timeout=6)
                if image_jpeg != "" and  image_jpeg.status_code == 200:
                    with open(album_path+"/"+str(i) + ".jpg", 'wb') as f:
                        f.write(image_jpeg.content)
                        ok = True
                        i += 1
            if i == 10:
                break
    pass



def get_last_publication(inst_restraunt):
    # href1 = "https://www.instagram.com/api/v1/users/web_profile_info/?username=ohota_auto"

    href = "https://www.instagram.com/api/v1/users/web_profile_info/?username=" + inst_restraunt[1:]
    respon = requests.get(href, headers=headers, proxies = proxies)
    x = json.dumps(respon.text, ensure_ascii=False, indent = 6)  #можно использовать для парсинга текста первой публикации/ тут есть и ссылки на посты и картинки. но их вытащить не могу
    pattern = r'"text":"(.*?)"'

    text = re.search(pattern, respon.text).group(1)


    return text

#get_album("@skiarealplesivec","Czech-Republic/A_cities/Abertamy-Karlovy-Vary-Region-Czech-Republic/Restraunt")
#get_last_publication("@skiarealplesivec")








"""
from instagrapi import Client


proxy_server = "http://umrPYt:dKe8Ze@85.195.81.170:11485"
proxy_server_for_inst = "http://ec675777:6656af7e7c@45.134.28.7:30010"
proxies = {
    "https": proxy_server,
    "http": proxy_server,
}
ACCOUNT_USERNAME = "repetitor_maksin"
ACCOUNT_PASSWORD = "ff6018ff"
cl = Client(proxy=proxy_server_for_inst)
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username("ohota_auto")

user_media = cl.user_medias(user_id, 1)

#cl.photo_download_by_url_origin(medias[0].thumbnail_url)
if user_media:
    # Получаем текст (подпись) последнего поста
    last_post = user_media[0]
    text_of_last_post = last_post.caption.text if last_post.caption else 'No caption'

    # Вывод текста последнего поста
    print(text_of_last_post)
else:
    print("This user has no media available.")
"""

pass
