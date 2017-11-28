from django.test import TestCase
from django.test.utils import override_settings
from mmio.tasks import check_supply_task, check_input_pins_task


@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                   CELERY_ALWAYS_EAGER=True,
                   BROKER_BACKEND='memory')
class TasksTest(TestCase):
    def test_supply_task(self):
        check_supply = check_supply_task.delay()
        self.assertTrue(check_supply.successful())

    def test_input_pins_task(self):
        check_input_pins = check_input_pins_task.delay()
        self.assertTrue(check_input_pins.successful())
