from mmio.ex9055dm import EX9055DM
from django.conf import settings
from mmio.models import NotificationPin


class ControlBoard(EX9055DM):
    def __init__(self, address):
        if settings.PRODUCTION:
            EX9055DM.__init__(self, address)

            self.issues = {}
            for k, v in NotificationPin.objects.all().values_list('name', 'pin'):
                self.issues[k] = v

    def check_issues(self):
        if settings.PRODUCTION:
            found_issues = []
            for k, v in self.issues.items():
                input_status = self.read_input(v)
                if input_status:
                    if input_status is 1:
                        found_issues.append(k)
                else:
                    raise ValueError('Could not read from the device')

            return found_issues
        else:
            return []

    def set_led(self, color):
        if settings.PRODUCTION:
            if color is 'green':
                self.write_output(1, 0)
                self.write_output(0, 1)
            elif color is 'red':
                self.write_output(0, 0)
                self.write_output(1, 1)
