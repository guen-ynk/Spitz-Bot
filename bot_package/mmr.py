import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome Headless Options
chrome_options = Options()
chrome_options.add_argument("--headless")


def mmr(usname):
    browser = webdriver.Chrome(executable_path=r"driver/chromedriver.exe", options=chrome_options)
    browser.get("https://euw.whatismymmr.com")
    browser.implicitly_wait(30)
    browser.find_element_by_id("input--summoner").send_keys(usname)
    browser.find_element_by_id("button--search").click()
    time.sleep(15)

    element = browser.find_element_by_id("stats--ranked")
    location = element.location
    size = element.size

    browser.save_screenshot("temp/shot.png")

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open('temp/shot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('temp/image.png')
    browser.close()
