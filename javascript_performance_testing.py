from config import GECKOPATH

from selenium import webdriver

url = 'https://trimps.github.io/'

driver = webdriver.Firefox(executable_path=GECKOPATH)
driver.get(url)

def fetch_resources():
    return driver.execute_script('return game.resources;')

def dummyfunction():
    return 1

n = 10000
for i in range(n):
    dummyfunction()
    fetch_resources()