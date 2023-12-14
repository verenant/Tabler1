
class Restraunt_from_guru:
    name = ""
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
    category_str = ""
    qty_in_city = 0
    network = ""
    guru_url = ""
    inst_url = ""
    sub_category = ""
    network =""
    qty_in_city = ""

    def __init__(self, object, typeOfConstructor):
        if typeOfConstructor == 0:  # для парсинга
            address = object["address"]['streetAddress'].split(" ")
            self.main_url = object["href"]

            print(f"Working_on {object['href']}")

            self.additional_url = object["add_href"]
            self.name = object["name"]
            self.check = object["avg_check"]
            self.features = object["features"]

            if ("review" in object) and ("description" in object["review"]):
                self.description = object["review"]["description"]
                first_point = object["review"]["description"].find(".")
                self.short_description = object["review"]["description"][:first_point]
            else:
                self.description = "no_info"
                self.short_description = "no_info"
            self.menu_href = object["menu"]

            if not("telephone" in object):
                object["telephone"] = "no_info"
            self.phone = object["telephone"]
            #self.address = object["address"]["addressLocality"] + ">" + object["address"]['streetAddress']
            self.street = address[0]
            if len(address) == 2:
                self.place = address[1]
            else:
                self.place = "no_info"
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
        #   self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)
        #   self.menu = get_menu(self.soup, self.additional_url)
        """
        if typeOfConstructor == 1: #для json  #  0 для парсинга
            addUrl = additional_url[additional_url.rfind("/") + 1:]
            j = get_json(addUrl)
            self.__dict__ = json.loads(j)
        """


    def get_json(self):
        json_dict = {
            "latinName" : self.additional_url,
            "name" : self.name,
            "check" : self.check,
            "features" : self.features,
            "description" : self.description,
            "short_description" : self.description,
            "phone" : self.phone,
            "timetable" : self.timetable,
            "kitchen" : self.kitchen,
            "category" : self.category,
            "place_url" : self.place_url,
            # self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
            "lat" : self.lat,
            "lon" : self.lon,
            "inst_url" : self.inst_url,
            "sub_category" : self.sub_category,
            "street" : self.street,
        }

        if self.place != "no_info":
            json_dict["place"] = self.place
        return json_dict
