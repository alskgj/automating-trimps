"""
    api
    ==========

    handles access to game ressources

"""
import time
import re

from selenium.webdriver import Firefox

from config import GAME_URL, USERNAME, PASSWORD


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
