import ipaddress
import random
import time

import bs4
import requests
import ipaddress
#============================================================================

#============================================================================


proxies_from_network = [
]


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}

main_page= "https://restaurantguru.com/"



def get_new_proxies():
    random_milliseconds = random.randint(1000, 2000)
    time.sleep(random_milliseconds / 1000.0)
    proxies = []
    res = requests.get("https://free-proxy-list.net/", headers = headers)
    table = bs4.BeautifulSoup(res.text, "html.parser")

    ips = table.find("tbody").find_all("tr")
    for ip in ips:
        ip_addr = ip.find("td")

        port = ip_addr.findNext("td")
        if port.text != "80":
            newIpAddress = ip_addr.text + ":" + port.text

            proxies.append(newIpAddress)
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


def get_soup(url):
    ok = True
    indexProxy = 0
    file_with_proxies = open("proxy.txt", "r")
    proxies_from_network = file_with_proxies.readlines()
    for i in range(len(proxies_from_network)):
        proxies_from_network[i] = proxies_from_network[i][:-1]
    file_with_proxies.close()
    while(ok):
        random_milliseconds = random.randint(100, 1500)
        time.sleep(random_milliseconds / 1000.0)



        res = ""
        if "" in proxies_from_network:
            proxies_from_network.remove("")
      #  i = random_milliseconds % random.randint(len(proxies_from_network),2*len(proxies_from_network))
        if indexProxy < len(proxies_from_network):
            proxies = {
                "https": proxies_from_network[indexProxy],
                "http": proxies_from_network[indexProxy],
            }
            try:
                res = requests.get(url, headers=headers, proxies = proxies, timeout=6)

            except Exception:
                pass
                print(f"bad Ip -- {proxies_from_network[indexProxy]}")

        else:
            res = requests.get(url, headers=headers)
            # если все прокси удалены, то берем их опять из файла
            if len(proxies_from_network) == 0:
                file_with_proxies = open("proxy.txt", "r")
                proxies_from_network = file_with_proxies.readlines()
                for i in range(len(proxies_from_network)):
                    proxies_from_network[i] = proxies_from_network[i][:-1]
                if "" in proxies_from_network:
                    proxies_from_network.remove("")
                file_with_proxies.close()
                time.sleep(1*60)


        if res != "":
            if res.status_code == 200:
                if bs4.BeautifulSoup(res.text,"html.parser").find("span",class_="pier_img") == None: # если не словили капчу

                  #  for k in range(5):
                   #     proxies_from_network[k] = proxies["http"] # proxies_from_network[i]
                       #### #ok = False
                    return bs4.BeautifulSoup(res.text, "html.parser")
                else:
                    if len(proxies_from_network)>0:
                        proxies_from_network.pop(indexProxy)
                    #time.sleep(60*5)
        #indexProxy+=1
       # if i == len(proxies_from_network):
       #    proxies_from_network = get_new_proxies()




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

def get_city_letters(country):
    countryUrl = "https://restaurantguru.com/cities-" + country + "-c"
    soup = get_soup(countryUrl)
    lettersHTML = soup.findAll("div", class_ = "cities_block" )
    letters = []
    for letterHTML in lettersHTML:
        letterHTMLText = letterHTML.text
        letters.append(letterHTMLText.strip()[0])
    return letters

def get_country_city_href(country,letter):
    cityHrefs = []
    countryUrl = "https://restaurantguru.com/cities-" + country + "-c/" + letter + "-t"
    soup = get_soup(countryUrl)
    cities_div_li_containers = soup.find("div", class_ = "cities scrolled-container").findAll("li")
    for li in cities_div_li_containers:
            cityHrefs.append(li.find("a").get("href"))
    return cityHrefs
    pass


def get_full_city_name(href):

    soup = get_soup(href)

    cityName = soup.find("div", class_= "content crumbs")
    cityName= cityName.find("a", attrs = { "href" : href}).text
    cityName = cityName.replace(" ","-")
    cityName = cityName.replace(",", "")
   # cityName = cityName.replace(">", "-")

    return cityName
def get_countries():

    f = open("countries.txt","r",encoding="UTF-8")
    countries = f.readlines()
    for i in range(len(countries)):
        countries[i] = countries[i][:-1]
    return countries


#=================================================
stTime = time.localtime()
print(f"{stTime.tm_hour}-{stTime.tm_min}")

#proxies_from_network = get_new_proxies() # получение бесплатных прокси
#get_good_proxies(main_page,proxies_from_network) #составление файла с хорошими прокси
#countries = get_countries(main_page)
countries = get_countries()
counter = 0
for countryIndex in range(1,len(countries)): # не через in чтобы пропустить Алеутские острова
    #letters = get_city_letters(countries[4])
    letters = get_city_letters(countries[countryIndex])
    for letter in letters:
        #cityHrefs = get_country_city_href(countries[4],letters[1])
        cityHrefs = get_country_city_href(countries[countryIndex], letter)
        for cityHref in cityHrefs:
            #city_name = get_full_city_name(cityHrefs[2])

            city_name = get_full_city_name(cityHref)
            counter+=1
            print(f"{city_name}   ====> {counter}")



pass