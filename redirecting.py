from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return
def getLinks(userUrl, driver):
    driver.get("http://space.bilibili.com"+userUrl)
    waitForLoad(driver)
    html = driver.page_source
    bsObj = BeautifulSoup(html)
    return bsObj.findAll("a",{"class":"item"})
    
driver = webdriver.PhantomJS(executable_path='phantomjs-2.0.0-windows/bin/phantomjs')
links = getLinks("/1653140", driver)
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle, driver)

