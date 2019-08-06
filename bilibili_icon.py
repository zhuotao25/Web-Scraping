from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import datetime
import random
import re
import os

random.seed(datetime.datetime.now())


def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 12:
            print("Timing out after 15 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return


def getLinks(userUrl, driver):
    driver.get("http://space.bilibili.com/" + userUrl + "/fans/follow")
    waitForLoad(driver)
    html = driver.page_source
    bsObj = BeautifulSoup(html, "html.parser")
    saveImg(bsObj)
    return bsObj.findAll("a", href=re.compile("^(//space)((?!:).)*$"))


def saveImg(bsObj):
    imgs = bsObj.findAll("img", id="h-avatar")
    if len(imgs) > 0:
        for i in range(0, len(imgs)):
            img = imgs[i]
            print(img)
            imageLocation = img["src"]
            print(imageLocation)
            name = bsObj.find("span", id="h-name")
            path = "icon/" + name.text + "." + imageLocation.rsplit('.', 1)[-1]
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.isfile(path):
                urlretrieve("http:" + imageLocation, path)
                print("saved: " + path)


session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-windows/bin/phantomjs')
links = getLinks("38934450", driver)
while len(links) > 0:
    link = links[random.randint(0, len(links) - 1)]
    newArticle = link.attrs["href"]
    s = newArticle.rsplit('/')
    print("next id:" + s[-2])
    links.extend(getLinks(s[-2], driver))
