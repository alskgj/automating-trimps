"""
    modules.new_buildings
    ~~~~~~~~~~~~~~~~~

    buys buildings
    # todo currently we are only ever building 1 building per turn - this is not optimal
"""

from api import Trimps, NotAffordableError
from config import BUILDINGS_STORAGE, BUILDINGS_HOUSING, BUILDINGS_OTHER


def run(trimps: Trimps):

    if len(trimps.building_queue) > 5:
        return

    # at the very start of the game we might have to manually build traps
    if trimps.trimps_amount < 5:
        try:
            trimps.build('Trap')
        except NotAffordableError:
            pass
        return

    # storage > housing > other
    for building in BUILDINGS_STORAGE+BUILDINGS_HOUSING+BUILDINGS_OTHER:
        try:
            trimps.build(building)
        except NotAffordableError:
            pass
        else:
            # return after building 1 building successfully
            return


