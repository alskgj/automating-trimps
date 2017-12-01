from time import sleep
from selenium import webdriver
import logging
from config import GAME_URL
from modules import upgrades, buildings, jobs, maps
import tools

logging.basicConfig(level=logging.INFO)

driver = webdriver.Firefox()

# start game and login
driver.get(GAME_URL)
tools.login(driver)

# load modules and run them
modules = [upgrades, buildings, jobs, maps]

while True:
    for mod in modules:
        sleep(2)
        mod.run(driver)
    sleep(5)

