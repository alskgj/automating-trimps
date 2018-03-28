"""
    modules.new_buildings
    ~~~~~~~~~~~~~~~~~

    buys buildings
"""


class Building:
    """Wrapper around building"""
    def __init__(self, container):
        self.container = container
        self.name, self.amount = self.parse_text()

    def parse_text(self):
        text = self.container.text.split('\n')
        return text[0], int(text[1])

    def click(self):
        self.container.click()


def run(driver):
    affordable_buildings = driver.find_elements_by_class_name('thingColorCanAfford')
    affordable_buildings = [Building(e) for e in affordable_buildings]

    if not affordable_buildings:
        return

    # atm we just build the building we have the least amount of
    min(affordable_buildings, key=lambda building: building.amount).click()
