import os
import configparser
import logging
from mmetering_server.settings import BASE_DIR


config = configparser.RawConfigParser()
config.read(os.path.join(BASE_DIR, 'my.cnf'))

logger = logging.getLogger(__name__)


class DummyRequest:
    GET = None


def supply_threshold_handler(*args, **kwargs):
    from mmio.controlboard import ControlBoard
    from mmetering.summaries import Overview

    io_address = config.getint('controlboard', 'address')
    logger.debug('Connecting to control board on address %i' % io_address)

    io_board = ControlBoard(io_address)
    threshold = config.getint('controlboard', 'supply-threshold') / 100

    # after each signal, check if at least 70% of energy
    # supply are produced by BHKW and PV
    data = Overview(DummyRequest.GET)

    if data.is_supply_over_threshold(threshold):
        logger.debug("Over 70% of energy supply are produced by BHKW and PV")
        io_board.set_led('green')
    else:
        logger.debug("Under 70% of energy supply are produced by BHKW and PV")
        io_board.set_led('red')
