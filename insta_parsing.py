import json
import random
import shutil
import time
import requests
import os
import bs4
#import selenium.common.exceptions
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium_stealth import stealth
import re
#from seleniumwire import webdriver



headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36",
    "X-IG-App-ID": "936619743392459" # 
}


proxy_server = "http://TyKxFA:tdnG0H@200.71.127.109:9164"
proxy_server_for_inst = "http://ec675777:6656af7e7c@45.134.28.7:30010"
proxies = {
    "https": proxy_server_for_inst,
    "http": proxy_server_for_inst,
}

"""
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
"""



def get_proxy():
    f = open("proxy.txt")
    proxies = f.readlines()
    r = random.randint(0,len(proxies)-2)

    proxy = {
        "https": proxies[r].strip(),
        "http": proxies[r].strip(),
    }
    return proxy
"""
def get_album1(inst_restraunt,album_path):
    # Заменить restraunt на настоящий
    album_path = album_path + "/Restraunt/Album"

    # if os.path.exists(album_path):
    #    shutil.rmtree(album_path)

    # делаем новую папку
    #os.mkdir(album_path)
    selenium_ok = False
    wait_time = 1.5
    while selenium_ok == False:
        counts = 0
        try:
            proxy_server = get_proxy()
            options = webdriver.ChromeOptions()
            #options.add_argument(
            #    "user-agent =  Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")
            #options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(seleniumwire_options=proxy_server, options = options)
            #driver = webdriver.Chrome(options=options)
            #driver.maximize_window()
            #driver.get("https://insta-stories-viewer.com/ohota_auto/")
            driver.get("https://instanavigation.com/en/user-profile/"+inst_restraunt[1:])
            #driver.get("https://insanony.com/profile/" + inst_restraunt[1:])
            time.sleep(wait_time)
            #element = driver.find_element(By.CLASS_NAME,"profile-publications__btn")
            element = driver.find_element(By.CSS_SELECTOR, "div.profile-publications__btn")
            #бывает, что не кликает надо подождать тогда подольше!
            element.click()
            # бывает, что не загружает надо подождать тогда подольше!
            time.sleep(wait_time)

            html_text = driver.page_source
            photo_page = bs4.BeautifulSoup(html_text, "html.parser")
            posts_table = photo_page.find("div", id= "posts")
            image_table = posts_table.findAll("img")
            i = 0
            for image in image_table:
                image_href = image.get("data-src")
                attemps = 0
                if image_href:
                    ok = False
                    random_proxy = get_proxy()
                    count_tries = 0
                    #подбираем прокси сервер для скачивания изображений, до тех пор пока оно не будет скачано
                    while not(ok):
                        image_jpeg = ""
                        try:
                            image_jpeg = requests.get(image_href, headers=headers, proxies = random_proxy, timeout=6)
                        except requests.exceptions.ReadTimeout:
                            print(f"  proxies_during_downloading_inst_img ->> BLOCKED = {random_proxy['http']}")
                            attemps += 1

                        if image_jpeg != "" and image_jpeg.status_code == 200:
                            with open(str(i) + ".jpg", 'wb') as f:
                                f.write(image_jpeg.content)
                                ok = True
                                i += 1
                        if attemps == 10:
                            ok = True
                            print("no chance to get photo " + inst_restraunt)
                    if i == 10:
                        break
            last_publication_text = ""
            try:
                last_publication_text = posts_table[0].find("p",class_="text-dark mt-1").text
            except AttributeError:
                print(f"{inst_restraunt} no posts with publication")
                wait_time += 1.0

            if count_tries == 10:
                count_tries +=1
                print(f"  bad instagram {image_href} = {random_proxy['http']}")
                return ""

            return last_publication_text
        except selenium.common.exceptions.ElementClickInterceptedException:
            counts += 1
            if counts == 10:
                selenium_ok = True
            print(f"some error ")  # or  proxies_during_downloading_inst_img ->> BLOCKED = {proxy_server['http']}")
            wait_time += 1.0




def get_album(inst_restraunt,album_path):
    # Заменить restraunt на настоящий
    album_path = album_path + "/Album"

    if os.path.exists(album_path):
        shutil.rmtree(album_path)
    # делаем новую папку
    os.mkdir(album_path)

    selenium_ok = False
    attemps = 0
    wait_time = 1.5
    while selenium_ok == False:
        try:
            proxy_server = get_proxy()
            driver = webdriver.Chrome(seleniumwire_options=proxy_server)

            driver.get("https://insta-stories-viewer.com/"+inst_restraunt[1:])
            time.sleep(wait_time)
            element = driver.find_element(By.PARTIAL_LINK_TEXT, "Publications")
            element.click()
            time.sleep(wait_time)
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
                        selenium_ok = True
                        break
        except AttributeError:
            attemps +=1
            if attemps == 10:
                selenium_ok = True
            print(f"some error ")# or  proxies_during_downloading_inst_img ->> BLOCKED = {proxy_server['http']}")
            wait_time += 1.0
        except selenium.common.exceptions.NoSuchElementException:
            attemps += 1
            if attemps == 10:
                selenium_ok = True
            print(f"some error ")  # or  proxies_during_downloading_inst_img ->> BLOCKED = {proxy_server['http']}")
            wait_time += 1.0
    pass


"""
"""
def get_last_publication(inst_restraunt): # не работает
    # href1 = "https://www.instagram.com/api/v1/users/web_profile_info/?username=ohota_auto"

    href = "https://www.instagram.com/api/v1/users/web_profile_info/?username=" + inst_restraunt[1:]
    respon = requests.get(href, headers=headers, proxies = proxies)
    #x = json.dumps(respon.text, ensure_ascii=False, indent = 6)  #можно использовать для парсинга текста первой публикации/ тут есть и ссылки на посты и картинки. но их вытащить не могу
    pattern = r'"text":"(.*?)"'
    text = ""
    try:
        text = re.findall(pattern, respon.text)[1]
    except Exception:
        print("api doesnt work")
    return text

"""

def get_inst_proxy():
    f = open("foreign_proxies.txt")
    proxies = f.readlines()
    r = random.randint(0,len(proxies)-1)

    proxy = {
        "https": proxies[r].strip(),
        "http": proxies[r].strip(),
    }
    return proxy

def get_album_and_last_publication_pikacu(inst_restraunt,album_path):
    album_path = album_path + "/Album"

    if os.path.exists(album_path):
        shutil.rmtree(album_path)
    # делаем новую папку
    os.mkdir(album_path)

    global_attemps = 0
    global_ok = True
    last_publication = ""
    while(global_ok):
        try:# загрузка зеркала инстаграмма с фотографиями
            good_proxy = get_inst_proxy()
            site = requests.get("https://www.picuki.com/profile/" + inst_restraunt[1:], headers = headers, proxies= good_proxy,timeout = 5)
            photo_page = bs4.BeautifulSoup(site.text, "html.parser")
            #posts = photo_page.findAll("div", class_="box-photo")
            posts = photo_page.findAll("div", class_="box-photo")

            i = 0
            k = 0
            for post in posts:
                if post.find("div") != None and post.find("div").get("id") != None:
                    k+=1
                if post.get("data-s")=="media":

                    resp = ""
                    img = post.find("img",class_="post-image").get("src")
                    ok = True
                    while(ok):

                        try:# загрузка фотографий
                            resp = requests.get(img,headers = headers, proxies = good_proxy, timeout = 5)
                        except requests.exceptions.ReadTimeout:
                            print(f"  proxies_during_downloading_inst_img ->> BLOCKED = {good_proxy['http']}")
                        if resp != "" and resp.status_code == 200:
                            if i < 3 and (posts[i].find("div", class_="photo-description") != None) and (
                                    posts[i].find("div", class_="photo-description").text.strip() != "") \
                                    and last_publication == "":
                                last_publication = str(i-k) + "_" + posts[i].find("div",
                                                                                class_="photo-description").text.strip()
                            with open(album_path + "/" + str(i) + ".jpg", 'wb') as f:
                                f.write(resp.content)
                                ok = False
                                global_attemps = 0
                                i += 1
                if i == 10:
                    global_ok = False
                    ok = False
                    break
            if last_publication == None:
                last_publication = ""
            return last_publication
        except AttributeError:
            print(f"{inst_restraunt} didn't allow to download photos, attemp = {global_attemps}")
            global_attemps +=1
            if global_attemps == 5:
                print(f"{inst_restraunt} didn't allow to download photos")
                global_ok = False
        except requests.exceptions.ReadTimeout:
            print(f"{inst_restraunt} didn't allow to download photos, attemp = {global_attemps}")
            global_attemps +=1
            if global_attemps == 5:
                print(f"{inst_restraunt} didn't allow to download photos")
                global_ok = False
        except BaseException:
            print(f"{inst_restraunt} Some error downloading instagram")
            global_attemps += 1
            if global_attemps == 5:
                print(f"{inst_restraunt} didn't allow to download photos")
                global_ok = False
            return False

#t = get_album_and_last_publication_pikacu("@unudleas","Czech-Republic")
#print(t)
#pass
#get_last_publication("@southmoravia")








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

