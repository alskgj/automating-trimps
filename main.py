from time import sleep
from selenium import webdriver
import logging
from config import GAME_URL, GECKOPATH
from modules import upgrades, buildings, jobs, maps, gather, new_buildings
import tools
from api import Trimps

logging.basicConfig(level=logging.INFO)
driver = webdriver.Firefox(executable_path=GECKOPATH)

trimps = Trimps(driver)
trimps.login()


"""

# load modules and run them
# modules = [upgrades, buildings, jobs, maps]
modules = [gather, new_buildings]

for i in range(10):
    for mod in modules:
        sleep(2)
        mod.run(driver)
    sleep(5)
"""

input()