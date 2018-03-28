from time import sleep
from selenium import webdriver
import logging
from config import GECKOPATH
from modules import upgrades, jobs, maps, gather, buildings, fight
from api import Trimps

logging.basicConfig(level=logging.INFO)
driver = webdriver.Firefox(executable_path=GECKOPATH)

trimps = Trimps(driver)
trimps.login()

# load modules and run them
# modules = [upgrades, buildings, jobs, maps]
modules = [gather, buildings, fight]

for i in range(10):
    for mod in modules:
        sleep(2)
        mod.run(trimps)
    sleep(5)

input()
