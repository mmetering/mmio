import os
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.apps import apps
from django.conf import settings
import configparser
import logging

config = configparser.RawConfigParser()
config.read(os.path.join(settings.BASE_DIR, 'my.cnf'))

logger = logging.getLogger(__name__)


class MMioConfig(AppConfig):
    name = 'mmio'
    verbose_name = 'MMetering IO Board'
