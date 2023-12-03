
import bs4
import requests


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"}

main_page= "https://restaurantguru.com/"


def get_soup(url):
    res = requests.get(url, headers=headers)
    return bs4.BeautifulSoup(res.text, "html.parser")


def get_countries(url):
    soup_main = get_soup(url)
    countries = soup_main.find("div", class_='promo_links content')
    spanCountries = countries.findAll("span")
    countries = []
    for spanCountry in spanCountries:
        country = spanCountry.text
        country = country.replace(" ", "-")
        countries.append(country)

    countries[0] = "Aland-Islands"
    return countries

def get_city_letters(country):
    countryUrl = "https://restaurantguru.com/cities-" + country + "-c"
    soup =  get_soup(countryUrl)
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
    cityName = soup.find("div", class_= "content_crumbs").find("a", class_= href).text
    cityName = cityName.replace(" ","-")
    cityName = cityName.replace(",", "")
    cityName = cityName.replace(">", "-")

    return cityName

countries = get_countries(main_page)
letters = get_city_letters(countries[4])
cityHrefs = get_country_city_href(countries[4],letters[1])
city_name = get_full_city_name(cityHrefs[2])


pass