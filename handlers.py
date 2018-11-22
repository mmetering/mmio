import os
import configparser
import logging
from mmetering_server.settings import BASE_DIR
from mmio.controlboard import ControlBoard
from mmetering.summaries import Overview
from mmetering.tasks import send_system_email_task
from django.template import Context
from django.template.loader import render_to_string
from mmio.models import NotificationPin

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
            logger.exception("Couldn't reach IO module on address %d." % io_address)
    else:
        logger.debug("Under " + str(threshold) + "% of energy supply are produced by BHKW and PV")

        try:
            io_board.set_led('red')
        except (IOError, ValueError) as e:
            logger.exception("Couldn't reach IO module on address %d." % io_address)


def check_input_pins_handler():
    io_address = config.getint('mmio', 'address')
    io_board = ControlBoard(io_address)
    pin_states = {}

    try:
        pin_states = io_board.check_pins()
    except (IOError, ValueError) as e:
        # Exceptions which can be raised by minimalmodbus.
        logger.exception("Couldn't reach IO module on address %d." % io_address)

    if len(pin_states) > 0:
        issues = []
        resolved_errors = []

        for pin, state in pin_states.items():
            notification_pin = NotificationPin.objects.get(pin=pin)

            if state == 1 and notification_pin.state == 'W':
                # New error. Set pin state and send mail.
                notification_pin.state = 'E'
                issues.append(notification_pin.name)
            elif state == 0 and notification_pin.state == 'E':
                # Error resolved. Set new pin state.
                notification_pin.state = 'W'
                resolved_errors.append(notification_pin.name)

            notification_pin.save()

        if len(issues) > 0:
            issues = '\n'.join(issues)
            context = Context({'issues': issues})
            message = render_to_string('mmio/email_error_pins_message.txt', context)

            send_system_email_task.delay(message)

        if len(resolved_errors) > 0:
            resolved_errors = '\n'.join(resolved_errors)
            context = Context({'resolved_errors': resolved_errors})
            message = render_to_string('mmio/email_resolved_error_pins_message.txt', context)

            send_system_email_task.delay(message)
