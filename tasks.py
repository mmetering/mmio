import logging
from celery.schedules import crontab
from celery.task import periodic_task
from celery.signals import after_setup_task_logger
from datetime import datetime, timedelta
from time import sleep
from mmio.handlers import supply_threshold_handler, check_input_pins_handler


def setup_logging(**kwargs):
    """
      Handler names is a list of handlers from your settings.py you want to
      attach to this
    """

    handler_names = ['mail_admins', 'file', 'console']

    import logging.config
    from django.conf import settings
    logging.config.dictConfig(settings.LOGGING)

    logger = kwargs.get('logger')

    handlers = [x for x in logging.root.handlers if x.name in handler_names]
    for handler in handlers:
        logger.addHandler(handler)
        logger.setLevel(handler.level)
        logger.propagate = False


after_setup_task_logger.connect(setup_logging)


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name='check_supply_task',
    ignore_result=True
)
def check_supply_task():
    logger = check_supply_task.get_logger()
    logger.setLevel(logging.DEBUG)

    supply_threshold_handler()


@periodic_task(
    run_every=timedelta(seconds=60),
    name='check_input_pins_task',
    ignore_result=True
)
def check_input_pins_task():
    logger = check_supply_task.get_logger()
    logger.setLevel(logging.DEBUG)

    check_input_pins_handler()
