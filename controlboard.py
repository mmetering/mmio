from mmio.ex9055dm import EX9055DM
from mmio.models import NotificationPin


class ControlBoard(EX9055DM):
    def __init__(self, address):
        EX9055DM.__init__(self, address)

        self.pins = {}
        for name, pin in NotificationPin.objects.all().values_list('name', 'pin'):
            self.pins[pin] = name

    def check_pins(self):
        pin_states = {}
        for pin, name in self.pins.items():
            input_status = self.read_input(pin)
            pin_states[pin] = input_status

        return pin_states

    def set_led(self, color):
        if color is 'green':
            self.write_output(1, 0)
            self.write_output(0, 1)
        elif color is 'red':
            self.write_output(0, 0)
            self.write_output(1, 1)
