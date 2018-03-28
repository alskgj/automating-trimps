"""
    modules.gather
    ~~~~~~~~~~~~~~~~~

    manages player gathering of resources

    Priority:
    Buildings > Trimps (trapping) > min ressource
    TODO do something better - gathering buildings might be good if building_queue is long
"""

import logging
import re

logger = logging.getLogger(__name__)


class PlayerGatherContainer:
    """Wrapper class for 'playerGather' class elements.
    """

    def __init__(self, container):
        self.container = container

        self.name = self.parse_text()[0]
        self.amount, self.capacity = self.parse_text()[1]
        print(f'Resource {self.name}: {self.amount}/{self.capacity}')

    def click(self):
        logger.info(f'Switching to {self.name}')
        self.container.find_element_by_class_name('workBtn').click()

    def parse_text(self):
        """ Parses a container.text

        container.text: 'Food\n170 / 500\n5 Mins 30 Secs\nGathering\n+1/sec'
        :return: ['Food', (170, 500)]
        """
        text = self.container.text
        if '???' in text or 'Trimps' in text:
            resource = 'Trimps'
            progress = text.split('\n')[2]
        else:
            resource, progress, *_ = text.split('\n')
        progress = re.findall('\d+', progress)

        # Science has  no maximum capacity
        if 'Science' in text:
            progress = int(progress[0]), None
        else:
            progress = int(progress[0]), int(progress[1])
        return [resource, progress]


def run(driver):

    # we help building stuff
    if len(building_queue(driver)) >= 2:
        logger.info("Switching to buildings")
        driver.find_element_by_id('buildingsCollectBtn').click()
        return

    # default option: gather the resource with the lowest amount stored
    # we remove all containers that are not displayed yet - we need to unlock them first
    containers = driver.find_elements_by_class_name('playerGather')
    containers = [PlayerGatherContainer(c) for c in containers if c.text]

    basic, trimps = [c for c in containers if c.name != 'Trimps'], [c for c in containers if c.name == 'Trimps']

    if trimps:
        trimps = trimps[0]
        if trimps.amount < trimps.capacity:
            trimps.click()
            # Todo what if we have no traps?
            return

    # we always gather the resources with the lowest amount stored - obviously this is horrible
    min(basic, key=lambda container: container.amount).click()


def building_queue(driver):
    # TODO error handling
    return driver.execute_script("return game.global.buildingsQueue")





