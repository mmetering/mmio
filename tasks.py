from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime, timedelta
from mmio.handlers import supply_threshold_handler

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name='check_supply_task',
    ignore_result=True
)
def check_supply_task():
    supply_threshold_handler()


@periodic_task(
    run_every=timedelta(seconds=60),
    name='check_input_pins_task',
    ignore_result=True
)
def check_input_pins_task():
    pass
