from config import UPGRADES
import logging

logger = logging.getLogger(__name__)


def run(driver):
    for upgrade in UPGRADES:

        upgrade_info = driver.execute_script('return game.upgrades["%s"]' % upgrade)
        affordable = driver.execute_script('return canAffordTwoLevel(game.upgrades["%s"])' % upgrade)
        if upgrade_info['allowed'] > upgrade_info['done'] and affordable:
            driver.execute_script('buyUpgrade("%s", true, true);' % upgrade)
            logging.info('[upgrade] upgraded %s to level %s' % (upgrade, upgrade_info['allowed']))
