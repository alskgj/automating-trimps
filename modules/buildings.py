"""
    modules.buildings
    ~~~~~~~~~~~~~~~~~

    buys buildings, priorises storage, then housing
"""

import logging
from config import BUILDINGS_HOUSING, BUILDINGS_STORAGE, BUILDINGS_OTHER

logger = logging.getLogger(__name__)


def buildingqueue(driver):
    return driver.execute_script("return game.global.buildingsQueue")


def build(driver, building):

    # check if building is already beeing built
    queue = buildingqueue(driver)
    if len([b for b in queue if b.startswith(building)]):
        logger.debug('returning since building is already in queue')
        return

    # locked building...
    if driver.execute_script("return game.buildings['%s'].locked" % building):
        logger.debug('returning since building is locked')
        return

    level = driver.execute_script("return game.buildings['%s'].owned" % building)
    # test if we can afford it
    if driver.execute_script("return canAffordBuilding('%s')" % building):
        result = driver.execute_script("return buyBuilding('%s')" % building)
        if result:
            logger.info("[building] bought %s, level %s" % (building, level+1))


def build_gyms(driver):
    gymistic_level = driver.execute_script("return game.upgrades['Gymystic'].done")
    gym_level = driver.execute_script("return game.buildings['Gym'].owned")
    if gym_level < 20 or gymistic_level >= 1:
        build(driver, 'Gym')


def run(driver):
    if len(buildingqueue(driver)) >= 5:
        driver.execute_script("setGather('buildings');")
        return
    else:
        driver.execute_script("setGather('metal')")

    for building in BUILDINGS_STORAGE:
        build(driver, building)

    for building in BUILDINGS_HOUSING:
        build(driver, building)

    for building in BUILDINGS_OTHER:
        build(driver, building)

    # special case for gyms
    build_gyms(driver)
