from restraunt_guru import Restraunt_from_guru
import os
import requests
import json

def createNetworks():
     # создание сетей для каждого города
    good_networks = {}
    country = "Czech-Republic"
    letter_cities = os.listdir(country)
    for letter in letter_cities:
        print(letter + "_cities")
        if letter == "B_cities":
            break
        letter_path = country + "/" + letter
        cities = os.listdir(letter_path)
        if len(cities) > 0:
            for c in cities:
                # создаем словарь с именем сети и количеством в городе
                networks = {}

                city_path = letter_path + "/" + c
                rests_in_city = os.listdir(city_path)
                # print(city_path)
                for res in rests_in_city:
                    rest_path = city_path + "/" + res
                    # print(rest_path)
                    if os.path.exists(rest_path + "/json.txt"):
                        rest = Restraunt_from_guru("", "", 1, rest_path)
                    else:
                        print(rest_path + " =-> no_json_file")
                        continue

                    #rest = Restraunt_from_guru("", "", 1, rest_path)
                    if rest.name in networks:
                        networks[rest.name]["qty"] += 1
                    else:
                        networks[rest.name] = {}
                        networks[rest.name]["qty"] = 1
                        networks[rest.name]["category"] = rest.category
                        networks[rest.name]["city"] = c
                pass

                #очистка файла с сетями
                network_file = open(city_path + "/networks.txt", "w",
                                    encoding="UTF-8")

                network_file.close()
                #формирование сети после прохода по городу и отправка запроса на сервер


                for n in networks:
                    if networks[n]["qty"] > 1:
                         #print(n)
                         #good_networks.append(n)
                         good_networks[n] = {}
                         good_networks[n]["category"] = networks[n]["category"]
                         good_networks[n]["city"] = networks[n]["city"].lower()

                         data = {
                             "name" : n,
                             "category": "chain of "+good_networks[n]["category"],
                             "cityId": 'abertamy-karlovy-vary-region-czech-republic',
                             #"city": good_networks[n]["city"],
                         }
                         headers = {
                             'Authorization': 'Bearer 5V2EABW0ODofJAaQqaz5ifkB'
                         }
                         post_organisation_url = "https://tabler.pub/api/v2/organisations"
                         response_creation = requests.post(post_organisation_url,json = data, headers = headers)
                         #print(response_creation.text)
                         d = json.loads(response_creation.text)
                         #good_networks[n]["id"]= d["data"]["organisation"]["id"]
                         data["organisationId"] = d["data"]["organisation"]["id"]
                         #print(good_networks[n]["id"])
                         network_file = open(city_path+"/networks.txt", "a",
                                          encoding="UTF-8")  # 1_ для того чтобы писать города в отдельные страны
                         network_file.write(json.dumps(data, ensure_ascii=False) + "\n")

                         network_file.close()
    pass


createNetworks()