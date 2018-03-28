"""
    api
    ==========

    handles access to game ressources

# TODO: Implement science lookup
# TODO: Implement science gathering
"""
import time
import re
import logging

from selenium.webdriver import Firefox

from config import GAME_URL, USERNAME, PASSWORD

logger = logging.getLogger(__name__)


class Trimps:

    def __init__(self, driver: Firefox):
        self.driver = driver

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

    def _parse_trimps(self):
        """Parses the trimps container"""
        trimps = self._trimps_container()
        if not trimps:
            return {'amount': 0, 'capacity': 0, 'breeding': 0, 'traps': 0}

        breeding = re.findall('(\d+) breeding', trimps.text) or [0]
        amount = re.findall('(\d+) / \d+', trimps.text) or [0]
        capacity = re.findall('\d+ / (\d+)', trimps.text) or [0]
        traps = re.findall('Traps \((\d+)\)', trimps.text) or [0]
        employed = re.findall('(\d+)/\d+ employed', trimps.text) or [0]
        employed_capacity = re.findall('\d+/(\d+) employed', trimps.text) or [0]

        return {
            'amount': int(amount[0]),
            'capacity': int(capacity[0]),
            'breeding': int(breeding[0]),
            'traps': int(traps[0]),
            'employed': int(employed[0]),
            'employed_capacity': int(employed_capacity[0])
                }

    def _parse_basic_resources(self):
        """Parses the Food, Wood and Metal container
        Returns {Food: (12, 100), Wood: (100, 100), Metal: (None, None)}
        if we have 12/100 Food, 100/100 Wood, and haven't unlocked metal yet."""
        containers = self._playergather_containers()
        result = dict()
        for resource in ['Food', 'Wood', 'Metal']:
            container = [c for c in containers if resource in c.text]
            if not container:
                result[resource] = None, None
                continue
            container = container[0]
            current = int(re.findall('(\d+) / \d+', container.text)[0])
            max = int(re.findall('\d+ / (\d+)', container.text)[0])
            result[resource] = current, max
        return result

    @property
    def science(self):
        containers = self._playergather_containers()
        containers = [c for c in containers if 'Science' in c.text]
        if not containers:
            return None
        container = containers[0]
        return int(re.findall('(\d+)', container.text)[0])

    @property
    def wood(self):
        return self._parse_basic_resources()['Wood'][0]

    @property
    def food(self):
        return self._parse_basic_resources()['Food'][0]

    @property
    def metal(self):
        return self._parse_basic_resources()['Metal'][0]

    @property
    def wood_capacity(self):
        return self._parse_basic_resources()['Wood'][1]

    @property
    def food_capacity(self):
        return self._parse_basic_resources()['Food'][1]

    @property
    def metal_capacity(self):
        return self._parse_basic_resources()['Metal'][1]

    @property
    def trimps_breeding(self):
        return self._parse_trimps()['breeding']

    @property
    def trimps_amount(self):
        return self._parse_trimps()['amount']

    @property
    def trimps_capacity(self):
        return self._parse_trimps()['capacity']

    @property
    def trimps_traps(self):
        return self._parse_trimps()['traps']

    @property
    def trimps_employed(self):
        return self._parse_trimps()['employed']

    @property
    def trimps_employed_capacity(self):
        return self._parse_trimps()['employed_capacity']
