import bs4
import requests
import jsons


query = ""

MAIN_URL = "https://tabler.ru/api/v1/places?offset=0&limit=25&response_type=short&query=" + query



def getJsonForTablerObject(url):
    response = requests.get(url)
    if '"status":"RecordNotFound"' in response.text:
        #Запись не найдена -> можно создавать ресторан
        pass
    else:
        #Запись найдена -> получить json
        return response.json()



class TablerObject():
    JSON = getJsonForTablerObject(MAIN_URL)
    if isinstance(JSON,dict):
        def __init__(self):
            self.__dict__ = jsons.load(self.JSON)


#tablerObj = TablerObject()
pass