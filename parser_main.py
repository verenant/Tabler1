from selenium import webdriver
import time

#option = webdriver.ChromeOptions()
from selenium.webdriver.common.by import By

binary_yandex_driver_file = "yandexdriver.exe" # path to YandexDriver
driver = webdriver.Chrome()
super_url = "https://www.restoclub.ru"
baseurl_1 = "https://www.restoclub.ru/msk/search/1?expertChoice=false&types%5B%5D=3&types%5B%5D=30&types%5B%5D=23&types%5B%5D=38&types%5B%5D=16&types%5B%5D=46&types%5B%5D=2&types%5B%5D=33&types%5B%5D=7&types%5B%5D=14&types%5B%5D=4&types%5B%5D=24&types%5B%5D=15&types%5B%5D=39&types%5B%5D=1&types%5B%5D=17&types%5B%5D=37&types%5B%5D=22&types%5B%5D=13&types%5B%5D=25"
driver.get(baseurl_1)
time.sleep(3)

element = driver.find_element(By.CSS_SELECTOR, "div.search-place-card")
data_href = element.get_attribute("data-href")
#переходим на в ресторан по полученной ссылке
driver.get(super_url+data_href)
div_element = driver.find_element(By.CLASS_NAME, 'expandable-text__t')
# Находим внутри div нужный элемент p
p_element = div_element.find_element(By.TAG_NAME,'p')
# Получаем текст из элемента p
description = p_element.text

hidden_phone = driver.find_element(By.CLASS_NAME, "place-phone").find_element(By.TAG_NAME,"a")
phone = hidden_phone.get_attribute("content")

# adress=
# timetable =
# avg_check =
# kitchen =
# images =
pass
driver.quit()