import requests
import json
import os
f = open("insta_href.txt","r")
dir_path = "instagramm"
hrefs = f.readlines()
f.close()
proxy_server = "http://TyKxFA:tdnG0H@200.71.127.109:9164"
proxies_CANADA_v4 = {
    "https": proxy_server,
    "http": proxy_server,
}

proxy_server_for_photo = "http://umrPYt:dKe8Ze@85.195.81.170:11485"
proxy_server_for_photo = "http://93.115.28.181:443"
proxies_DE_v6 = {
    "https": proxy_server,
    "http": proxy_server,
}
f = open("cookies_inst.txt","r")
cookies = json.loads(f.read())
f.close()
headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}
i = 0



ip = requests.get('https://api.ipify.org',proxies = proxies_CANADA_v4).content.decode('utf8')
print('My public IP address is: {}'.format(ip))

for href_image in hrefs:
    print(href_image)
    image_jpeg = requests.get(href_image, proxies=proxies_CANADA_v4)
    # response = requests.get(url)

    if image_jpeg.status_code == 200:
        with open(dir_path + "/" + str(i) + ".jpg", 'wb') as f:
            f.write(image_jpeg.content)
    i += 1
    if i == 10:
        break