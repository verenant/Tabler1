from instagrapi import Client
import requests
import os
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"
}
proxy_server = "http://TyKxFA:tdnG0H@200.71.127.109:9164"
proxies = {
    "https": proxy_server,
    "http": proxy_server,
}
dir_path = "/instagram"
USERNAME = "repetitor_maksim"
Password = "ff6018ff"
cl = Client()
cl.set_proxy(proxy_server)
cl.login(USERNAME, Password)

#print(cl.account_info())
rest_id = cl.user_id_from_username("lafarmarestaurant")
l = cl.user_medias(rest_id,10)
i=0


proxy_server_for_photo = "http://umrPYt:dKe8Ze@85.195.81.170:11485"
proxies = {
    "https": proxy_server,
    "http": proxy_server,
}

for x in l:
    #p = int(x.pk)
    href_image = str(x.thumbnail_url)
    print(href_image)
    cl.photo_download_by_url_origin(href_image)

    image_jpeg = requests.get(href_image, headers=headers, proxies= proxies )
    # response = requests.get(url)

    if image_jpeg.status_code == 200:
        with open(dir_path + "/" + str(i) + ".jpg", 'wb') as f:
            f.write(image_jpeg.content)
    i += 1
    if i==10:
        break
