import requests
import jsons

MAIN_URL = "https://tabler.ru/api/v1/places?offset=0&limit=25&response_type=short&query=дымзавод"

def getJsonForTablerObject(url):
    response = requests.get(url)
    return response.json()


class TablerObject():
    JSON = getJsonForTablerObject(MAIN_URL)
    def __init__(self):
        self.__dict__ = jsons.load(self.JSON)


#tablerObj = TablerObject()
pass