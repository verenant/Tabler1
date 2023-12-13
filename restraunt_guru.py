
class Restraunt_from_guru():
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

    def __init__(self, object, typeOfConstructor):
        if typeOfConstructor == 0:  # для парсинга
            address = object["address"]['streetAddress'].split(" ")

            first_point = object["review"]["description"].find(".")
            self.short_description = object["review"]["description"][:first_point]
            self.main_url = object["href"]
            self.additional_url = object["add_href"]
            self.name = object["name"]
            self.check = object["avg_check"]
            self.features = object["features"]
            self.description = object["review"]["description"]
            self.menu_href = object["menu"]
            self.phone = object["telephone"]
            #self.address = object["address"]["addressLocality"] + ">" + object["address"]['streetAddress']
            self.street = address[0]
            self.place = address[1]
            # self.avg_check = get_avg_check(self.soup)
            if not("openingHours" in object):
                object["openingHours"] = "no_info"
            self.timetable = object["openingHours"]
            # self.features = get_features(self.soup)
            self.kitchen = object["servesCuisine"]
            self.category = object["type"]
            self.place_url = object["url"]
            # self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
            self.lat = object["geo"]["latitude"]
            self.lon = object["geo"]["longitude"]
            self.inst_url = object["instagramm"]
            self.sub_category = object["sub_category"]
        #   self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)
        #   self.menu = get_menu(self.soup, self.additional_url)
        """
        if typeOfConstructor == 1: #для json  #  0 для парсинга
            addUrl = additional_url[additional_url.rfind("/") + 1:]
            j = get_json(addUrl)
            self.__dict__ = json.loads(j)
        """

