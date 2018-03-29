"""
    api
    ==========

    handles access to game ressources

# TODO: Implement science lookup
# TODO: Implement science gathering
"""
import time

import logging
from config import BUILDINGS

from selenium.webdriver import Firefox, ActionChains

from config import GAME_URL, USERNAME, PASSWORD

logger = logging.getLogger(__name__)


class NotAffordableError(Exception):
    """Raised upon trying to build something that is not affordable"""


class Trimps:

    def __init__(self, driver: Firefox):
        self.driver = driver

    def _get_resources(self):
        """Sample from game:
        {'food': {'max': 500, 'owned': 0},
         'fragments': {'max': -1, 'owned': 0},
         'gems': {'max': -1, 'owned': 0},
         'helium': {'max': -1, 'owned': 0},
         'metal': {'max': 500, 'owned': 0},
         'science': {'max': -1, 'owned': 0},
         'trimps': {'employed': 0,
                    'max': 10,
                    'maxMod': 1,
                    'maxSoldiers': 1,
                    'owned': 0,
                    'potency': 0.0085,
                    'realMax': {},
                    'soldiers': 0,
                    'speed': 5,
                    'working': 0},
         'wood': {'max': 500, 'owned': 0}}
         """
        return self.driver.execute_script('return game.resources;')

    @property
    def all_buildings(self):
        buildings = self.driver.find_elements_by_class_name('buildingThing')
        buildings = [Building(e) for e in buildings]
        return buildings

    def build(self, building: str):
        """Tries to build building.
        If building is not affordable an error will be raised"""
        if building not in BUILDINGS:
            logger.error(f'{building} not recognized.')
            raise NotImplementedError

        for element in self.all_buildings:
            if element == building and element.is_affordable():
                self.move_to_and_click_button(element.container)
                return True
            elif element == building and not element.is_affordable():
                raise NotAffordableError

        return False

    @property
    def fighting_unlocked(self):
        """Returns whether we can fight"""
        return self.driver.execute_script('return game.upgrades.Battle.done;')

    @property
    def fighting(self):
        return self.driver.execute_script('return game.global.fighting;')

    def move_to_and_click_button(self, button):
        """from http://selenium-python.readthedocs.io/api.html
        using action chains to prevent tooltips over fight button
        :param button: a clickable selenium thingy
        """
        default_position = self.driver.find_element_by_id('food')
        ActionChains(self.driver).move_to_element(button).click(button).move_to_element(default_position).perform()

    def fight(self):
        self.move_to_and_click_button(self.driver.find_element_by_id('fightBtn'))

    def login(self):
        """LOGIN:
        set username and password, then click login, then confirm if there are conflicting saves:
        document.getElementById("loginUserName").value = 'alskgj'
        document.getElementById("loginPassword").value = '5sv8dIONs9qP'
        playFabLoginWithPlayFab()
        playFabFinishLogin(true)
        """
        self.driver.get(GAME_URL)

        time.sleep(2)
        self.driver.execute_script('cancelTooltip(); toggleSetting("usePlayFab");')
        self.driver.execute_script('document.getElementById("loginUserName").value = "%s";' % USERNAME)
        self.driver.execute_script('document.getElementById("loginPassword").value = "%s";' % PASSWORD)
        self.driver.execute_script('playFabLoginWithPlayFab();')
        time.sleep(2)
        self.driver.execute_script('playFabFinishLogin(true);')

    def gather(self, activity: str):
        """ Sets the players gathering activity

        :param activity: Food, Wood, Metal, Science, Build or Trimps
        :return:
        """
        activity = activity.capitalize()
        activities = ['Food', 'Wood', 'Metal', 'Science', 'Build', 'Trimps']
        if activity not in activities:
            logger.error(f'gathering activity {activity} not in {activities}')
            raise NotImplementedError

        if activity == 'Build':
            self.driver.find_element_by_id('buildingsCollectBtn').click()
        else:
            container = [c for c in self._playergather_containers() if activity in c.text]
            if not container:
                logger.warning(f'Could not switch to activity {activity}. Container not available.')
            else:
                container[0].find_element_by_class_name('workBtn').click()

    def player_build(self):
        """Sets the player to buildings
        """
        self.gather('Build')

    def player_trap(self):
        """Sets the player to trapping trimps
        """
        self.gather('Trimps')

    @property
    def building_queue(self):
        return self.driver.execute_script("return game.global.buildingsQueue")

    def _playergather_containers(self):
        """Gets the playergather containers.
        There are 8 total:
        4 basic ressources (food, wood, metal, science),
        Trimps and 3 unknown"""
        return self.driver.find_elements_by_class_name('playerGather')

    def _trimps_container(self):
        """Returns the ingame trimps container"""
        container = [c for c in self._playergather_containers() if 'Trimps' in c.text]
        if container:
            return container[0]
        else:
            return None

    @property
    def science(self):
        return self._get_resources()['science']['owned']

    @property
    def wood(self):
        return self._get_resources()['wood']['owned']

    @property
    def food(self):
        return self._get_resources()['food']['owned']

    @property
    def metal(self):
        return self._get_resources()['metal']['owned']

    @property
    def wood_capacity(self):
        return self._get_resources()['wood']['max']

    @property
    def food_capacity(self):
        return self._get_resources()['food']['max']

    @property
    def metal_capacity(self):
        return self._get_resources()['metal']['max']

    @property
    def trimps_breeding(self):
        return self._get_resources()['trimps']['owned'] - self._get_resources()['trimps']['employed']

    @property
    def trimps_amount(self):
        return self._get_resources()['trimps']['owned']

    @property
    def trimps_capacity(self):
        # this is not the real max? -- seems to be without multiplicators
        return self._get_resources()['trimps']['max']

    @property
    def trimps_traps(self):
        return self.driver.execute_script("return game.buildings['Trap'].owned;")

    @property
    def trimps_employed(self):
        return self._get_resources()['trimps']['employed']

    @property
    def trimps_looking_for_job(self):
        return self.driver.execute_script('return game.workspaces;')


class Building:
    """Wrapper around building"""
    def __init__(self, container):
        self.container = container
        self.name, self.amount = self.parse_text()

    def parse_text(self):
        text = self.container.text.split('\n')
        if len(text) != 2:
            print(text)
            print(self.container)
        return text[0], int(text[1])

    def click(self):
        self.container.click()

    def is_affordable(self):
        return 'thingColorCanAfford' in self.container.get_attribute('class')

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        else:
            return other.name == self.name
