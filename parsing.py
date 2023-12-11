import os
import time
import json
import bs4
import requests
import random


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
                if proxies_from_network[indexProxy].qtyOfUsage == 9:
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
                    time.sleep(1 * 7)  # ускорить бы процесс!



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
    guru_restraunt_json = soup.find("script", type = "application/ld+json").text
    # добавлять в строку данные после "{"
    print(guru_restraunt_json)
    guru_restraunt_json = guru_restraunt_json.replace("@type","type")
    url_instagramm_for_dict = '  "instagramm":"'+ soup.find("a", class_= "insta_btn").text + '",'
    href_for_dict = '  "href":  "' + href + '",\n'
    add_href_for_dict = '  "add_href":  "' +  href[href.rfind("/")+1:] + '",\n'
    guru_restraunt_json=guru_restraunt_json.replace("{","{\n"+href_for_dict+add_href_for_dict+url_instagramm_for_dict,1)
    print(guru_restraunt_json)
    return guru_restraunt_json


def get_restraunt_hrefs_from_city_page(city_href):
    soup = get_soup(city_href,proxies_from_network)

    pass
