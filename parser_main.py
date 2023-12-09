import ipaddress
import json
import random
import time

import bs4
import requests
import ipaddress
#============================================================================

#============================================================================


proxies_from_network = [
]

city = {
    "name" : "",
    "latin_name": "",
    "lat": "",
    "lon": ""
}
cities = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}

main_page= "https://restaurantguru.com/"

class City():
    def __init__(self, url,good_proxies):
        city = get_full_city_name_and_coords(url,good_proxies)
        city["name"] = city["name"][:city["name"].find(",")]
        self.name = city["name"]
        self.latinName = city["latin_name"]
        self.lat = city["lat"]
        self.lon = city["lon"]

    def get_json(self):
        json_dict ={
            "name":self.name,
            "latinName": self.latinName,
            "lat": self.lat,
            "lon": self.lon,
        }
        return json_dict


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
    #for x in proxies:
     #   print(x)

    return proxies

def get_good_proxies(url,proxies_from_network):
    with open("proxy.txt","w", encoding="UTF-8") as f:
        ok = True
        i = 0
        k = 0
        f.write("46.161.45.235:9104\n")
        f.write("200.71.127.109:9164\n")
        while (ok ):
            random_milliseconds = random.randint(100, 1500)
            time.sleep(random_milliseconds / 1000.0)
            res = ""
            #  i = random_milliseconds % random.randint(len(proxies_from_network),2*len(proxies_from_network))
            if i < len(proxies_from_network) :
                proxies = {
                    "https": proxies_from_network[i],
                    "http": proxies_from_network[i],
                }
                try:
                    res = requests.get(url, headers=headers, proxies=proxies, timeout=2)

                except Exception:
                    pass
                    # print(f"bad Ip -- {proxies_from_network[i]}")
          #  else:
          #      res = requests.get(url, headers=headers)

            if res != "":
                if res.status_code == 200:
                    if i != len(proxies_from_network):
                        f.write(proxies["http"]+"\n")  # proxies_from_network
                        k+=1
            i += 1
            if i == len(proxies_from_network) and k>0:
                ok = False

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
       # random_milliseconds = random.randint(100, 1500)
       # time.sleep(random_milliseconds / 1000.0)
        pause_program()

        # случайные индексы для выбора IP прокси
        indexBadProxy = random.randint(0, len(bad_proxies_from_network)-1)

        rightEnd = len(proxies_from_network)      #защита от ("empty range for randrange() (%d, %d, %d)" % (istart, istop, width)) # не используется
        if rightEnd<=0:
            rightEnd=1

      #  indexProxy = random.randint(0, rightEnd) # случайные прокси

        # indexProxy берем первый незаблокированный и не на паузе
        for i in range(len(proxies_from_network)):
            if (proxies_from_network[i].isBlocked == False) and (proxies_from_network[i].isPaused == False):
                indexProxy = i
                break

        # очистка после взятия из файлов
        """
        if "" in proxies_from_network:
            proxies_from_network.remove("")
        if "" in bad_proxies_from_network:
            bad_proxies_from_network.remove("")
        """

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
               # random_milliseconds = random.randint(100, 1500)
               # time.sleep(random_milliseconds / 1000.0)

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
                #proxies_from_network.pop(indexProxy)

            try:
                #random_milliseconds = random.randint(100, 1500)
                #time.sleep(random_milliseconds / 1000.0)

                pause_program()

                requests.get(url, headers=headers, proxies = bad_proxies, timeout=4)

            except Exception:
                pass
                #print(f"bad Ip from bad IPS -- {bad_proxies_from_network[indexBadProxy]}")
                ###############proxies_from_network.pop(indexProxy)

        else:
            #random_milliseconds = random.randint(100, 1500)
            #time.sleep(random_milliseconds / 1000.0)
            pause_program()
            res = requests.get(url, headers=headers)
            try:
                #random_milliseconds = random.randint(100, 1500)
                #time.sleep(random_milliseconds / 1000.0
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
                    #======== новые строчки

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
                    # ========конец новые

                    # !!!   PROBLEM  !!!Если все заблокированы то indexProxy остается равным 0!!!!!! Решение внизу, еще не тестировано
                   # if indexProxy == len(proxies_from_network) :
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
                   # if len(proxies_from_network)>0: #еще есть хорошие прокси на пробу

                       # if indexProxy < len(proxies_from_network): # иначе происходит попытка удаления своего ip
                         #   print(f"indexProxy = {indexProxy}, len(proxies_from_network) = {len(proxies_from_network)}, proxies_from_network= {proxies_from_network[indexProxy]}")
                         #  proxies_from_network.pop(indexProxy)
                            # ========= новые строчки
                       #     print(
                               # f"indexProxy = {indexProxy}, len(proxies_from_network) = {len(proxies_from_network)}, proxies_from_network= {proxies_from_network[indexProxy].name}")
                            #proxies_from_network.pop(indexProxy)
                           # indexProxy = 0 # начинаем обход прокси с начала
                            # ========конец новые строчки
                    """# перезаполнение списка с прокси , убрал так как прокси теперь не удаляем        
                    else:
                        file_with_proxies = open("proxy.txt", "r") #все прокси удалены и берем новые
                        proxies_from_network = file_with_proxies.readlines()
                        for i in range(len(proxies_from_network)):
                            proxies_from_network[i] = proxies_from_network[i][:-1]
                        if "" in proxies_from_network:
                            proxies_from_network.remove("")
                        file_with_proxies.close()
                        bad_proxies_from_network = get_new_proxies()
                    """
                    time.sleep(1 * 10)  # ускорить бы процесс!




def get_countries(url):
    soup_main = get_soup(url)
    countries = soup_main.find("div", class_='promo_links content')
   # spanCountries = countries.findAll("div", class_="w25")
    spanCountries = countries.findAll("span")
    countries = []
    """ 
    for i in range(4):
        for country in spanCountries[i]:
           country.find
    finalCountries = []
    for i in range(4):
        finalCountries = finalCountries + countries[i]
    """
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


def get_full_city_name_and_coords(href,good_proxies):
    #получение имени города
    lat=""
    lon=""
    soup = get_soup(href,good_proxies)
    scripts = soup.findAll("script")
    for script_texts in scripts:
        if "lon" in script_texts.text:
            lat, lon = get_coords_from_script(script_texts.text)
    cityName = soup.find("div", class_= "content crumbs")
    cityName= cityName.find("a", attrs = { "href" : href}).text
    cityNameForMaps = cityName
    cityName = cityName.replace(" ","-")
    cityName = cityName.replace(",", "")
    # cityName = cityName.replace(">", "-")
    city = {
        "name":cityNameForMaps,
        "latin_name":cityName,
        "lat" : lat,
        "lon":lon,
    }
    return city
   # return cityNameForMaps+">"+cityName

def get_countries():
    f = open("countries.txt","r",encoding="UTF-8")
    countries = f.readlines()
    for i in range(len(countries)):
        countries[i] = countries[i][:-1]
    return countries


#=================================================
stTime = time.localtime()
print(f"{stTime.tm_hour}-{stTime.tm_min}")
good_proxies = get_good_proxies()
proxies_from_network = get_new_proxies() # получение бесплатных прокси
######get_good_proxies(main_page,proxies_from_network) #составление файла с хорошими прокси
#countries = get_countries(main_page)
countries = get_countries()
counter = 0


latin_names_list = []

for countryIndex in range(1,len(countries)): # не через in чтобы пропустить Алеутские острова
    #letters = get_city_letters(countries[4])
    #letters = get_city_letters
    country = "Australia" #countries[countryIndex] # при полном парсинге городов
    letters, city_qty = get_city_letters(country,good_proxies)
    city_qty = int(city_qty.text.replace("/ ","").strip())
    for letter in letters:
        cityHrefs = get_country_city_href(country,letter,good_proxies)
      #  cityHrefs = get_country_city_href(countries[countryIndex], letter)
        for cityHref in cityHrefs:
            #city_name = get_full_city_name(cityHrefs[2])

            #city_name = get_full_city_name_and_coords(cityHref,good_proxies) # старый вариант рабочий
            city = City(cityHref,good_proxies) # новый вариант через структуру тоже рабочий

            # собираем количество использований городов
            flag = False
            for names in latin_names_list:
                if names["name"] == city.latinName:
                    names["used"] += 1
                    city.latinName = city.latinName+"-"+names["used"]
                    flag = True
            if flag == False:
                latin_names_dict = {
                    "name": city.latinName,
                    "used": 0
                }
                latin_names_list.append(latin_names_dict)

            city_file = open(letter+"-cities.txt", "a", encoding="UTF-8")
            #  city_file.write(city_name+"\n")
            city_file.write(json.dumps(city.get_json())+"\n")
            counter+=1
            # print(f"{city_name}   ====> {counter}")
            print(f"{json.dumps(city.get_json())}   ====> {counter} , { str(counter/city_qty*100)[:6] }% in {country}")
            city_file.close()



pass