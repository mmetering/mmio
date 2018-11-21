import os
import configparser
import logging
from mmetering_server.settings import BASE_DIR
from mmio.controlboard import ControlBoard
from mmetering.summaries import Overview
from mmetering.tasks import send_system_email_task
from django.template import Context
from django.template.loader import render_to_string

config = configparser.RawConfigParser()
config.read(os.path.join(BASE_DIR, 'my.cnf'))

logger = logging.getLogger(__name__)


class DummyRequest:
    GET = None


def supply_threshold_handler(*args, **kwargs):
    io_address = config.getint('mmio', 'address')
    logger.debug('Connecting to control board on address %i' % io_address)

    io_board = ControlBoard(io_address)
    threshold = config.getint('mmio', 'supply-threshold') / 100

    # after each signal, check if at least 70% of energy
    # supply are produced by BHKW and PV
    data = Overview(DummyRequest.GET)

    if data.is_supply_over_threshold(threshold):
        logger.debug("Over " + str(threshold) + "% of energy supply are produced by BHKW and PV")

        try:
            io_board.set_led('green')
        except (IOError, ValueError) as e:
            logger.error("Couldn't reach IO module on address %d." % io_address)
    else:
        logger.debug("Under " + str(threshold) + "% of energy supply are produced by BHKW and PV")

        try:
            io_board.set_led('red')
        except (IOError, ValueError) as e:
            logger.error("Couldn't reach IO module on address %d." % io_address)


def check_input_pins_handler():
    io_address = config.getint('mmio', 'address')
    io_board = ControlBoard(io_address)
    issues = []

    try:
        issues = io_board.check_issues()
    except (IOError, ValueError) as e:
        # Exceptions which can be raised by minimalmodbus.
        logger.error("Couldn't reach IO module on address %d." % io_address)

    if len(issues) is not 0:
        issues = '\n'.join(issues)
        context = Context({'issues': issues})
        message = render_to_string('mmio/email_error_pins_message.txt', context)

        send_system_email_task.delay(message)
