
class Restraunt_from_guru():
    name = ""
    latin_name = ""
    additional_url = ""
    lon = 0.0
    lat = 0.0
    description = ""
    phone = ""
    address = ""
    avg_check = ""
    timetable = ""
    features = []
    kitchen = []
    category = ""
    subcategory = ""
    main_image_url = ""
    city = ""
    category_str = ""
    qty_in_city = 0
    network = ""
    guru_url = ""
    inst_url = ""

    def __init__(self, object, typeOfConstructor):
        if typeOfConstructor == 0:  # для парсинга
            self.main_url = object["href"]
            self.additional_url = object["add_href"]
            self.name = object["name"]
            self.description = object["review"]["description"]
            self.phone = object["telephone"]
            self.address = object["address"]["addressLocality"] + ">" + object["address"]['streetAddress']
            # self.avg_check = get_avg_check(self.soup)
            self.timetable = object["openingHours"]
            # self.features = get_features(self.soup)
            self.kitchen = object["servesCuisine"]
            self.category = object["type"]
            self.place_url = object["url"]
            # self.main_image_url = get_image(self.soup,self.main_url,self.headers,self.additional_url)
            self.lat = object["geo"]["latitude"]
            self.lon = object["geo"]["longitude"]
            self.inst_url = object["instagramm"]
        #   self.album = get_album(self.soup, self.main_url, self.headers, self.additional_url)
        #   self.menu = get_menu(self.soup, self.additional_url)
        """
        if typeOfConstructor == 1: #для json  #  0 для парсинга
            addUrl = additional_url[additional_url.rfind("/") + 1:]
            j = get_json(addUrl)
            self.__dict__ = json.loads(j)
        """

