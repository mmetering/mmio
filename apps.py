import os
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.apps import apps
from django.conf import settings
from mmio.signals import meterdata_post_save_handler
import configparser
import logging

config = configparser.RawConfigParser()
config.read(os.path.join(settings.BASE_DIR, 'my.cnf'))

logger = logging.getLogger(__name__)


class MMioConfig(AppConfig):
    name = 'mmio'
    verbose_name = 'MMetering IO Board'

    def ready(self):
        meter_data_model = apps.get_model('mmetering.MeterData')
        post_save.connect(meterdata_post_save_handler, sender=meter_data_model)
