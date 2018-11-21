from mmio.ex9055dm import EX9055DM
from mmio.models import NotificationPin


class ControlBoard(EX9055DM):
    def __init__(self, address):
        EX9055DM.__init__(self, address)

        self.issues = {}
        for name, pin in NotificationPin.objects.all().values_list('name', 'pin'):
            self.issues[name] = pin

    def check_issues(self):
        found_issues = []
        for name, pin in self.issues.items():
            input_status = self.read_input(pin)
            if input_status == 1:
                found_issues.append(name)

        return found_issues

    def set_led(self, color):
        if color is 'green':
            self.write_output(1, 0)
            self.write_output(0, 1)
        elif color is 'red':
            self.write_output(0, 0)
            self.write_output(1, 1)
