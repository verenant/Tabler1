import time
import json

class Restraunt_from_guru:
    name = ""
    id = ""
    latin_name = ""
    additional_url = ""
    lon = 0.0
    lat = 0.0
    description = ""
    short_description = ""
    phone = ""
    address = ""
    avg_check = ""
    timetable = ""
    features = []
    kitchen = []
    category = ""
    #subcategory = ""
    main_image_url = ""
    city = ""
    menu = ""
    category_str = ""
    guru_url = ""
    inst_url = ""
    sub_category = ""
    network =""
    qty_in_city = ""
    organisation_id = ""
    last_publication = ""
    place_url = ""

    def __init__(self, object,city, typeOfConstructor,rest_path):
        if typeOfConstructor == 0:  # для парсинга
            if ("address" in object) and ( "streetAddress" in object["address"]):
                #address = object["address"]['streetAddress'].split(" ")
                address = object["address"]['streetAddress']
            else:
                address = ["no_info"]
            self.main_url = object["href"]

            stTime = time.localtime()
            print(f"time: {stTime.tm_hour}-{stTime.tm_min} -> Working_on {object['href']}")

            self.latin_name = object["add_href"]
            self.name = object["name"]
            self.check = object["avg_check"]
            self.features = object["features"]
            """
            if ("review" in object) and ("description" in object["review"]):
                self.description = object["review"]["description"]
                first_point = object["review"]["description"].find(".")
                self.short_description = object["review"]["description"][:first_point+1]
            else:
                self.description = "no_info"
                self.short_description = "no_info"
            """
            if "new_description" in object:
                self.description = object["new_description"]
                first_point = object["new_description"].find(".")
                self.short_description = object["new_description"][:first_point + 1]
            else:
                self.description = "no_info"
                self.short_description = "no_info"

            self.menu_href = object["menu"]

            if not("telephone" in object):
                object["telephone"] = "no_info"
            self.phone = object["telephone"]
            #self.address = object["address"]["addressLocality"] + ">" + object["address"]['streetAddress']
            self.street = address
            """
            if len(address) >= 2:
                self.place = address[1]
            else:
                self.place = "no_info"
            """
            # self.avg_check = get_avg_check(self.soup)
            if not("openingHours" in object):
                object["openingHours"] = "no_info"
            self.timetable = object["openingHours"]
            # self.features = get_features(self.soup)
            if not("servesCuisine" in object):
                object["servesCuisine"] = "no_info"
            self.kitchen = object["servesCuisine"]
            self.category = object["type"]
            if not("url" in object):
                object["url"] = "no_info"
            self.place_url = object["url"]
            # self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
            self.lat = object["geo"]["latitude"]
            self.lon = object["geo"]["longitude"]
            self.inst_url = object["instagramm"]
            self.sub_category = object["sub_category"].strip()
            self.city = city.get_json()
        #   self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)
        #   self.menu = get_menu(self.soup, self.additional_url)
        """
        if typeOfConstructor == 1: #для json  #  0 для парсинга
            addUrl = additional_url[additional_url.rfind("/") + 1:]
            j = get_json(addUrl)
            self.__dict__ = json.loads(j)
        """
        #конструктор для загрузчика
        if typeOfConstructor == 1:
            #json_file = "Czech-Republic/A_cities/adamov-south-moravian-region-czech-republic/Asia-Bistro-Skalni-Sklep-Adamov/json.txt"
            json_file = rest_path+"/json.txt"
            f = open(json_file, encoding="UTF-8")
            t = f.read()
            j = json.loads(t)
            f.close()
            self.filename = rest_path
            self.name = j["name"]
            self.latin_name = j["latinName"]
            self.city = j["city"]
            self.avg_check = j["check"]
            self.lon = j["lon"]
            self.lat = j["lat"]
            self.phone = j["phone"]
            self.address = j["street"]
            self.category = j["category"]
            self.kitchen = j["kitchen"]
            self.description = j["description"]
            self.short_description = j["short_description"]
            self.timetable = j["timetable"]
            self.inst_url = j["inst_url"]
            self.place_url = j["place_url"]
            self.last_publication = j["last_publication"]
            self.sub_category = j["sub_category"]
            if "network" in j:
                self.network = j["network"]



            pass


    def get_json(self):

        json_dict = {
            "latinName" : self.latin_name,
            "name" : self.name,
            "check" : self.check,
            "features" : self.features,
            "description" : self.description,
            "short_description" : self.short_description,
            "phone": self.phone,
            "timetable" : self.timetable,
            "kitchen" : self.kitchen,
            "category" : self.sub_category,
            "place_url" : self.place_url,
            # self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
            "lat" : self.lat,
            "lon" : self.lon,
            "inst_url" : self.inst_url,
            "last_publication": self.last_publication,
            "sub_category" : self.sub_category,
            "street" : self.street,
            "city":self.city,
        }
        if self.network != "":
            json_dict["network"] = self.network
        #if self.place != "no_info":
        #    json_dict["place"] = self.place
        return json_dict


