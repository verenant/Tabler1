import json
import parsing
from anyascii import anyascii

class City():
    def __init__(self, url,country,good_proxies):
        city = parsing.get_full_city_name_and_coords(url,country,good_proxies)
        # city["name"] = city["name"][:city["name"].find(",")]
        self.name = city["name"]
        self.latin_name = anyascii(city["latin_name"]).lower()
        self.lat = city["lat"]
        self.lon = city["lon"]
        self.href = city["href"]
        self.country = country

    def get_json(self):
        json_dict ={
            "name":self.name,
            "latin_name": self.latin_name,
            "lat": self.lat,
            "lon": self.lon,
        }
        return json_dict
