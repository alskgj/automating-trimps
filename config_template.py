from os.path import join, dirname
import sys

GAME_URL = "https://trimps.github.io/"
USERNAME = "YOUR_USERNAME_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"

PRESTIGE = ['Dagadder', 'Supershield', 'Bootboost', 'Megamace', 'Axeidic', 'Greatersword', 'Hellishmet', 'Polierarm',
            'Bestplate', 'Smoldershoulder', 'Pantastic']

# from https://github.com/zininzinin/AutoTrimps/blob/gh-pages/modules/upgrades.js
UPGRADES = ['Miners', 'Scientists', 'Coordination', 'Speedminer', 'Speedlumber', 'Speedfarming', 'Speedscience',
            'Megaminer', 'Megalumber', 'Megafarming', 'Megascience', 'Efficiency', 'TrainTacular', 'Trainers',
            'Explorers', 'Blockmaster', 'Battle', 'Bloodlust', 'Bounty', 'Egg', 'Anger', 'Formations', 'Dominance',
            'Barrier', 'UberHut', 'UberHouse', 'UberMansion', 'UberHotel', 'UberResort', 'Trapstorm', 'Gigastation',
            'Shieldblock', 'Potency', 'Magmamancers', 'Gymystic'] + PRESTIGE


BUILDINGS_HOUSING = ['Hut', 'House', 'Mansion', 'Hotel', 'Resort', 'Gateway', 'Collector', 'Warpstation']
BUILDINGS_STORAGE = ['Barn', 'Shed', 'Forge']
BUILDINGS_OTHER = ['Tribute']
BUILDINGS = BUILDINGS_HOUSING + BUILDINGS_STORAGE + BUILDINGS_OTHER

JOBS_RATIOS = {
    'Scientist': 0.1,
    'Farmer': 0.25,
    'Lumberjack': 0.25,
    'Miner': 0.4
}

JOBS = ['Scientist', 'Farmer', 'Lumberjack', 'Miner']

if sys.platform == 'win32':
    GECKOPATH = join(dirname(__file__), 'geckodriver.exe')
else:
    GECKOPATH = join(dirname(__file__), 'geckodriver')
