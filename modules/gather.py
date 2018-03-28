"""
    modules.gather
    ~~~~~~~~~~~~~~~~~

    manages player gathering of resources

    Priority:
    Buildings > Trimps (trapping) > min ressource
    # todo when do I need to science?
"""

import logging

from api import Trimps

logger = logging.getLogger(__name__)


def run(trimps: Trimps):
    # If there are more than two buildings in the queue we help building
    if len(trimps.building_queue) >= 2:
        logger.info("Player set to building")
        trimps.player_build()
        return

    # If no trimps are breeding and we have traps we trap them
    if trimps.trimps_breeding < 2 and trimps.trimps_traps:
        logger.info("Player set to trapping")
        trimps.player_trap()

    # default option: gather the resource with the lowest amount stored
    resources = {
        'Food': trimps.food,
        'Wood': trimps.wood,
        'Metal': trimps.metal
    }
    logger.info("Player set to collecting resources")
    trimps.gather(min(resources, key=lambda key: resources[key]))






