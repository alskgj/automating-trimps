"""
    fight
    =====

    start fights left and right.

"""
import logging

from api import Trimps

logger = logging.getLogger(__name__)


def run(trimps: Trimps):

    # sanity check
    if not trimps.fighting_unlocked or trimps.fighting:
        return
    # only start fighting if there are lots of fighters
    if trimps.trimps_amount == trimps.trimps_capacity:
        logger.info('Fight!')
        trimps.fight()
