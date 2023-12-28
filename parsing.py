import os
import time
import json
import bs4
import requests
import random
import re
import shutil

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"
}

proxies_from_network = [
]

class Used_Proxy():
    name = ""
    isBlocked = False
    isPaused = False
    qtyOfUsage = 0
    blockedAt = -1

    def __init__(self,name,isBlocked,qtyOfUsage):
        self.name = name
        self.isBlocked = isBlocked
        self.qtyOfUsage = qtyOfUsage

    def incUsage(self):
        self.qtyOfUsage+=1

    def createJson(self):
        json_dict = {
            "name":self.name,
            "isBlocked":self.isBlocked,
            "isPaused":self.isPaused,
            "qtyOfUsage":self.qtyOfUsage,
            "blockedAt":self.blockedAt,
        }

        return json.dumps(json_dict)

    def is_full_blocked(self):
        if (self.isPaused == True) and (self.isPaused == True):
            return True
        else:
            return False


def get_new_proxies():
    random_milliseconds = random.randint(1000, 2000)
    time.sleep(random_milliseconds / 1000.0)
    proxies = []
    try:
        res = requests.get("https://free-proxy-list.net/", headers = headers)
    except requests.exceptions.ProxyError:
        print("Выключите прокси сервер в настройках OS")
    table = bs4.BeautifulSoup(res.text, "html.parser")

    ips = table.find("tbody").find_all("tr")
    for ip in ips:
        ip_addr = ip.find("td")

        port = ip_addr.findNext("td")
        if port.text != "80":
            newIpAddress = ip_addr.text + ":" + port.text

            proxies.append(newIpAddress)

    file_for_proxies = open("bad_proxy.txt","w",encoding="UTF-8")
    for proxy in proxies:
        file_for_proxies.write(proxy+"\n")

    file_for_proxies.close()
    return proxies



def get_good_proxies():
    # получаем хорошие прокси
    file_with_proxies = open("proxy.txt", "r")
    proxies_from_network = file_with_proxies.readlines()
    for i in range(len(proxies_from_network)):
        # proxies_from_network[i] = proxies_from_network[i][:-1]
        proxies_from_network[i] = Used_Proxy(proxies_from_network[i][:-1], False, 0)
    file_with_proxies.close()
    return proxies_from_network


def pause_program():
    random_milliseconds = random.randint(100, 1500)
    time.sleep(random_milliseconds / 1000.0)

def get_soup(url, proxies_from_network):
    ok = True

    bad_proxies_from_network_file = open("bad_proxy.txt","r")
    #получаем плохие прокси
    bad_proxies_from_network = bad_proxies_from_network_file.readlines()
    for i in range(len(bad_proxies_from_network)):
        bad_proxies_from_network[i] = bad_proxies_from_network[i][:-1]
    bad_proxies_from_network_file.close()
    indexProxy = 0
    while(ok):

        pause_program()

        # случайные индексы для выбора IP прокси
        indexBadProxy = random.randint(0, len(bad_proxies_from_network)-1)


        # indexProxy берем первый незаблокированный и не на паузе
        for i in range(len(proxies_from_network)):
            if (proxies_from_network[i].isBlocked == False) and (proxies_from_network[i].isPaused == False):
                indexProxy = i
                break
        bad_proxies = {
            "https": bad_proxies_from_network[indexBadProxy],
            "http": bad_proxies_from_network[indexBadProxy],
        }
        res = ""
        if indexProxy < len(proxies_from_network):
            proxies = {
                "https": proxies_from_network[indexProxy].name,
                "http": proxies_from_network[indexProxy].name,
            }

            #запросы к серверу сначала хорошим IP, потом плохим IP
            try:
                pause_program()
                # запрос хорошим прокси и увеличение количества использованных им раз
                # проверка прокси на отсутствие паузы
                if proxies_from_network[indexProxy].isPaused == True:
                   indexProxy+=1

                res = requests.get(url, headers=headers, proxies = proxies, timeout=6)
                proxies_from_network[indexProxy].incUsage()
                #если было запросов много это ставим его на паузу
                if proxies_from_network[indexProxy].qtyOfUsage == 4:
                    proxies_from_network[indexProxy].isPaused = True

            except Exception:
                print(f"bad Ip from good proxies -- {proxies_from_network[indexProxy].name}")

            try:
                pause_program()
                requests.get(url, headers=headers, proxies = bad_proxies, timeout=4)

            except Exception:
                pass

        else:
            pause_program()
            res = requests.get(url, headers=headers)
            try:
                pause_program()
                requests.get(url, headers=headers, proxies=bad_proxies, timeout=4)
            except Exception:
                pass
                #  print(f"bad Ip from bad IPS --  {bad_proxies_from_network[indexBadProxy]}")


        #если получили ответ от сервера ( он принял прокси)
        if res != "" and res.status_code == 200:
                if bs4.BeautifulSoup(res.text,"lxml").find("span",class_="pier_img") == None: # если не словили капчу
                    proxies_from_network[indexProxy].isBlocked = False
                    # ставим прокси на паузу, пока он не заблокировался
                    if proxies_from_network[indexProxy].isPaused == True:
                        indexProxy+=1

                    return bs4.BeautifulSoup(res.text, "html.parser") # получили адекватный ответ от сервера
                else:


                    #блокировка прокси и переход на следующий
                    proxies_from_network[indexProxy].isBlocked = True
                    proxies_from_network[indexProxy].blockedAt = proxies_from_network[indexProxy].qtyOfUsage

                    print(
                        f"indexProxy = {indexProxy}, len(proxies_from_network) = {len(proxies_from_network)}, proxies_from_network_BLOCKED = {proxies_from_network[indexProxy].name}")

                    #запись заблокированного прокси в файл
                    stTime = time.localtime()
                    block_time = (f"{stTime.tm_hour}-{stTime.tm_min}")

                    blocked_proxy_file = open("blocked_proxies.txt","a",encoding="UTF-8")
                    blocked_proxy_json = proxies_from_network[indexProxy].createJson()
                    blocked_proxy_file.write(block_time+"\t")
                    blocked_proxy_file.write(blocked_proxy_json)
                    blocked_proxy_file.write("\n")
                    blocked_proxy_file.close()
                    indexProxy += 1

                            #обновляем список прокси и снимаем блокировки и паузы. Нам нужны все

                    #снятие паузы

                    allPaused =True
                    for proxy in proxies_from_network:
                        if proxy.isPaused == False:
                            break
                    if allPaused == True:
                        for proxy in proxies_from_network:
                            proxy.isPaused = False


                    #проверка заблокированности всех IP
                    allBlocked = True
                    for proxy in proxies_from_network:
                        if proxy.isBlocked == False:
                            allBlocked=False
                    if allBlocked == True:
                        # Если все заблокированны, то
                        # очистка блокировок
                        for i in range(len(proxies_from_network)):
                            if proxies_from_network[i].isBlocked== True:
                                indexProxy = 0
                                proxies_from_network[i].isPaused = False
                                proxies_from_network[i].isBlocked = False
                            pass
                    pass
                    time.sleep(1 * 2.1)  # ускорить бы процесс!



def get_countries(url):
    soup_main = get_soup(url)
    countries = soup_main.find("div", class_='promo_links content')
   # spanCountries = countries.findAll("div", class_="w25")
    spanCountries = countries.findAll("span")
    countries = []

    f = open("countries.txt","w",encoding="UTF-8")
    for spanCountry in spanCountries:
        country = spanCountry.text
        country = country.replace(" ", "-")
        countries.append(country)


    countries[0] = "Aland-Islands"
    for country in countries:
        f.write(country+"\n")
    f.close()
    return countries

def get_city_letters(country, good_proxies):
    countryUrl = "https://restaurantguru.com/cities-" + country + "-c"
    soup = get_soup(countryUrl,good_proxies)
    lettersHTML = soup.findAll("div", class_ = "cities_block" )
    letters = []
    city_qty = soup.find("div", class_="restaurants_count")
    for letterHTML in lettersHTML:
        letterHTMLText = letterHTML.text
        letters.append(letterHTMLText.strip()[0])
    return letters,city_qty

def get_country_city_href(country,letter,good_proxies):
    cityHrefs = []
    countryUrl = "https://restaurantguru.com/cities-" + country + "-c/" + letter + "-t"
    soup = get_soup(countryUrl,good_proxies)
    cities_div_li_containers = soup.find("div", class_ = "cities scrolled-container").findAll("li")
    for li in cities_div_li_containers:
            cityHrefs.append(li.find("a").get("href"))
    return cityHrefs
    pass


def get_coords_from_script(string_with_coords):
    raw_coords_start_index = string_with_coords.find('"sw')
    raw_coords = string_with_coords[raw_coords_start_index:]
    raw_coords = raw_coords.replace('"sw":',"")
    raw_coords = raw_coords.replace(";", "", 1)
    raw_coords = raw_coords.strip()
    raw_coords = raw_coords.replace("}", "", 1)
    #raw_coords = raw_coords.replace("\n","")
    #

    raw_coords = eval(raw_coords)
    return raw_coords["latitude"],raw_coords["longitude"]


def get_full_city_name_and_coords(href,country,good_proxies):
    #получение имени города
    lat=""
    lon=""
    soup = get_soup(href,good_proxies)
    scripts = soup.findAll("script")
    for script_texts in scripts:
        if "longitude" in script_texts.text:
            lat, lon = get_coords_from_script(script_texts.text)
    cityName = soup.find("div", class_= "content crumbs")
    cityName= cityName.find("a", attrs = { "href" : href}).text + ", "+country
    #cityNameForMaps = cityName
    cityNameForMaps = cityName.replace("-"," ")
    cityName = cityName.replace(" ","-")
    cityName = cityName.replace(",", "")
    href = soup.find("link",rel="canonical").get("href")
    # cityName = cityName.replace(">", "-")
    city = {
        "name":cityNameForMaps,
        "latin_name":cityName,
        "lat" : lat,
        "lon":lon,
        "href":href,
    }
    return city
   # return cityNameForMaps+">"+cityName

def get_countries():
    f = open("countries.txt","r",encoding="UTF-8")
    countries = f.readlines()
    for i in range(len(countries)):
        countries[i] = countries[i][:-1]
    return countries


def get_json_restraunt(href,good_proxies):
    soup = get_soup(href,good_proxies)

    if soup.find("script", type = "application/ld+json"):
        guru_restraunt_json = soup.find("script", type = "application/ld+json").text
    else:
        #print(f"{href} -> no json -> bad restraunt")
        return "no_json"
    description_for_dict = ""
    if soup.find("div",class_="description"):
        description = soup.find("div",class_="description").text.strip()
        description_for_dict = '  "new_description":"'+description +'",'
    # добавлять в строку данные после "{"
    # print(guru_restraunt_json)
    guru_restraunt_json = guru_restraunt_json.replace("@type","type")
    try:
        url_instagramm_for_dict = '  "instagramm":"'+ soup.find("a", class_= "insta_btn").text + '",'
    except AttributeError:
        url_instagramm_for_dict = '  "instagramm":"''",'
    href_for_dict = '  "href":  "' + href + '",\n'
    add_href_for_dict = '  "add_href":  "' +  href[href.rfind("/")+1:] + '",\n'

    features_str = ""

    if soup.find("div", class_="features_block"):
        features = soup.find("div", class_="features_block").findAll("span")
        features_str = '"features":'+'"['
        features_list = []

        for feature in features:
            feature = feature.text
            features_list.append(feature)
            features_str= features_str+"'"+feature+"',"
        features_str = features_str[:-1]+']",\n'
    else:
        features_str = '"features":"no_info",\n'

    try:
        avg_price = soup.find("div", class_="short_info with_avg_price").text
        avg_price = ' "avg_check":" ' + str(prepare_avg_check(avg_price)) + '",\n'
    except AttributeError:
        avg_price = ' "avg_check":"no_info",\n'
    try:
        sub_category = soup.find("div", class_="r_prime").find("span").text
        sub_category = ' "sub_category":" ' +sub_category+ '",\n'
    except AttributeError:
        sub_category = ' "sub_category":"no_info",\n'
        f = open("log.txt", "a", encoding="UTF-8")
        f.write(f"{href} bad restraunt - no category\n")
        f.close()

    if sub_category != "":
        guru_restraunt_json=guru_restraunt_json.replace("{","{"+description_for_dict+href_for_dict+add_href_for_dict+avg_price+features_str+sub_category+url_instagramm_for_dict,1)
        #print(guru_restraunt_json)
        return guru_restraunt_json
    else:
        return ""


def prepare_avg_check(check):
    check = check.replace(",", "")
    # price_range = "price range per person czk 230 - czk 570"
    # Использование регулярного выражения для поиска всех чисел в строке
    numbers = re.findall(r'\b\d+\b', check)
    # Преобразование найденных числовых строк в целые числа
    numbers = [int(number) for number in numbers]
    #print(numbers)  # Выведет: [230, 570]
    if len(numbers) == 1:
        return numbers[0]
    else:
        return (numbers[0]+numbers[1])//2

def download_img(href,dir_path,good_proxies,i):
    ok = True
    count_tries = 0
    while ok:
        index_proxy = 0
        good_proxy = -1
        image_jpeg = ""
        while good_proxy==-1:
            for proxy in good_proxies:
                if (proxy.isPaused == False) and (proxy.isBlocked == False):
                    good_proxy = {
                        "https": proxy.name,
                        "http": proxy.name,
                    }
                    break
                index_proxy += 1

            if (good_proxy==-1): # Если все прокси заблокированы, то их надо разблокировать
                for i in range(0,len(good_proxies)):
                    good_proxies[i].isPaused = False
                    good_proxies[i].isBlocked = False

        try:
            image_jpeg = requests.get(href, headers=headers, proxies=good_proxy, timeout=6)
            if image_jpeg.status_code == 404:
                raise BaseException
        except requests.exceptions.ReadTimeout:
            #get_good_proxies()
            #image_jpeg = requests.get(href, headers=headers, proxies=good_proxy, timeout=3)
            print(f"  proxies_during_downloading_menu ->> BLOCKED = {proxy.name}")

            if index_proxy<len(good_proxies) and good_proxies[index_proxy].name == proxy.name:
                good_proxies[index_proxy].isBlocked = True
            count_tries += 1
            if count_tries == 5: # количество попыток скачивания с хорошим ip
                ok = False
                print(f"{href} has bad menu")
                return False
        except requests.exceptions.ProxyError:
            print(f"  proxies_during_downloading_menu ->> BLOCKED = {proxy.name}")
            if good_proxies[index_proxy].name == proxy.name:
                good_proxies[index_proxy].isBlocked = True
            count_tries += 1
            if count_tries == 5:  # количество попыток скачивания с хорошим ip
                ok = False
                print(f"{href} has bad menu")
                return False
        except requests.exceptions.ConnectTimeout:
            print(f"  proxies_during_downloading_menu ->> BLOCKED = {proxy.name}")
            if good_proxies[index_proxy].name == proxy.name:
                good_proxies[index_proxy].isBlocked = True
            count_tries += 1
            if count_tries == 5:  # количество попыток скачивания с хорошим ip
                ok = False
                print(f"{href} has secured menu")
                return False
        except BaseException:
            print(f"{href} Some error downloading menu")
            ok = False
            return False

        if image_jpeg != "" and image_jpeg.status_code == 200:
            with open(dir_path + "/menu/" + str(i) + ".jpg", 'wb') as f:
                f.write(image_jpeg.content)
                ok = False
            pass
        else:
            #ошибка при скачивании, делаем перезапуск пока не получим изображение после паузы
            time.sleep(1)

    return True

def get_menu(href_menu,dir_path,good_proxies):
    #удаление старой папки, если есть.
    menu_path = dir_path+"/menu"
    if os.path.exists(menu_path):
        shutil.rmtree(menu_path)
    #делаем новую папку
    os.mkdir(menu_path)
    try:
        if get_soup(href_menu,good_proxies).find("div",class_="left_column"):
            list_img = get_soup(href_menu,good_proxies).find("div",class_="left_column").findAll("img", recursive = False)
        else:
            list_img = get_soup(href_menu, good_proxies).find("div", class_="content clear").findAll("img", recursive=False)
    except AttributeError:
        shutil.rmtree(dir_path)
        print("  " + href_menu + " has no menu at all")
        return "no_menu"

    if isinstance(list_img,list) and len(list_img)>0:
        i = 0
        for img in list_img:
            href_img = img.get("data-src")
            if isinstance(href_img,str) and img.has_attr('class') and not("not_loaded" in img.get("class")):
                status_img = download_img(href_img,dir_path,good_proxies,i)
                if status_img == True:
                    i+=1
    else:
        shutil.rmtree(dir_path)
        return "no_menu"
    return True



#good_proxies = get_good_proxies()
#t = get_menu("https://restaurantguru.com/Bastanka-Frydek-Mistek/menu","Jsons" ,good_proxies)
#pass



