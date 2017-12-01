"""
    modules.jobs
    ~~~~~~~~~~~~

    sending those trimps do to some heavy lifting
"""
import logging

logger = logging.getLogger(__name__)


def prestiges_unlockable(driver):
    # every five levels there will be prestige waiting
    current_zone = driver.execute_script('return game.global.world;')
    mapunlocks = driver.execute_script('return game.mapUnlocks;')
    prestiges = {unlock: mapunlocks[unlock] for unlock in mapunlocks if 'prestige' in mapunlocks[unlock]}

    # if slow is not done ignore arbalest and gambeson
    slow_done = driver.execute_script('return game.global.slowDone')
    if not slow_done:
        prestiges = {p: prestiges[p] for p in prestiges if 'specialFilter' not in prestiges[p]}
    print(prestiges)
    return len([prestiges[p]['last'] for p in prestiges if prestiges[p]['last'] <= current_zone-5])


def switch_to_maps(driver):

    if not driver.execute_script('game.global.switchToMaps'):
        driver.execute_script('mapsClicked();')


def create_map(driver, level):
    driver.execute_script('mapLevelInput.value = %s' % level)

    for i in range(9, 0, -1):
        driver.execute_script('sizeAdvMapsRange.value = %s' % i)
        driver.execute_script('difficultyAdvMapsRange.value = %s' % i)
        driver.execute_script('lootAdvMapsRange.value = %s' % i)
        driver.execute_script('updateMapNumbers()')

        # we can afford map
        if driver.execute_script('return updateMapCost(true) < game.resources.fragments.owned'):
            print('we can afford map, sliders on %s/9, costing %s' %
                  (i, driver.execute_script('return updateMapCost(true)')))
            break

    logging.info('buying a map, level %s' % level)
    result = driver.execute_script('return buyMap()')
    if result == -2:
        logging.warning('Too many maps, recycling now...')
        driver.execute_script('recycleBelow(true)')


def get_prestige_map(driver):
    "Get's a map of current level or creates one if none found"
    maps_owned = driver.execute_script('return game.global.mapsOwnedArray;')
    current_zone = driver.execute_script('return game.global.world;')

    for game_map in maps_owned:
        if game_map['level'] == current_zone:
            return game_map['id']

    # no map found -> creating one
    create_map(driver, current_zone)

    return None


def run(driver):
    # maps not yet unlocked...
    if not driver.execute_script('return game.global.mapsUnlocked;'):
        return

    # always select mountain
    driver.execute_script("biomeAdvMapsSelect.value='Mountain'")

    if prestiges_unlockable(driver) < 2:
        print('here')
        return

    print('...')
    print(driver.execute_script("return !game.global.mapsActive && !game.global.preMapsActive && !game.global.switchToMaps"))
    # we are on worldmap and want to farm
    if driver.execute_script("return !game.global.mapsActive && !game.global.preMapsActive && !game.global.switchToMaps"):
        print(driver.execute_script('return mapsClicked()'))
        print('here2')
        # we will let trimps die, so just waiting for now
        return

    # we are in a map right now
    elif driver.execute_script("return game.global.mapsActive"):
        return

    # we are in mapchamber
    elif driver.execute_script("return game.global.preMapsActive"):
        mapid = get_prestige_map(driver)
        if mapid:
            driver.execute_script('selectMap("%s")' % mapid)
            driver.execute_script('runMap()')
            logging.info('Running map %s for prestige!' % mapid)

    # i fucked up?
    else:
        logging.error("state of mapchamber: %s, maps: %s - not in mapchamber/maps/worldmap???" % (
            driver.execute_script("return game.global.preMapsActive"),
            driver.execute_script("return game.global.mapsActive")
        ))

    #game.global.currentMapId

    # game.global.mapsActive is true when running a map
    # game.global.preMapsActive is true in mapchamber
    # --> we are on worldmap if neither is true

    # todo if more than 2 prestiges available, find out if we are on worldmap,
    # todo if yes, switch to mapchamber, select or create map,
    # todo set settings to repeat until items
