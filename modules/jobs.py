"""
    modules.jobs
    ~~~~~~~~~~~~

    sending those trimps do to some heavy lifting
"""
import logging
from config import JOBS_RATIOS, JOBS

logger = logging.getLogger(__name__)


def buy_jobs(driver, job, amount):
    # return if job is not yet unlocked
    if driver.execute_script('return game.jobs["%s"].locked' % job):
        return

    # disable firing and set right amount
    driver.execute_script('return game.global.firing = false')
    if amount == 'Max':
        driver.execute_script('return game.global.buyAmt = "Max"')
    else:
        driver.execute_script('return game.global.buyAmt = %s' % amount)

    if driver.execute_script('return canAffordJob("%s")' % job):
        driver.execute_script('buyJob("%s")' % job)
        logger.info("[jobs] recruited %s %s" % (amount, job))

    # reset buy amount
    driver.execute_script('return game.global.buyAmt = %s' % 1)


def simple_jobs(driver):
    """Buys Farmer, Miners, Lumberjacks and Scientists"""
    free = driver.execute_script('return Math.ceil(game.resources.trimps.realMax()/2) - game.resources.trimps.employed')
    if free == 0:
        return

    total = free
    for job in JOBS:
        current_job_number = driver.execute_script('return game.jobs["%s"].owned' % job)
        total += current_job_number

    for job in JOBS:
        diff = int(total * JOBS_RATIOS[job]) - driver.execute_script('return game.jobs["%s"].owned' % job)
        if diff <= 0:
            # nothing to see here
            continue

        buy = min(diff, free)
        buy_jobs(driver, job, buy)


def run(driver):
    free = driver.execute_script('return Math.ceil(game.resources.trimps.realMax()/2) - game.resources.trimps.employed')
    if free == 0:
        return

    buy_jobs(driver, 'Trainer', 'Max')

    simple_jobs(driver)
