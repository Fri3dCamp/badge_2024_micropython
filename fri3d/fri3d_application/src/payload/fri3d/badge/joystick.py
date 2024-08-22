from fri3d.badge.hardware import hardware_capabilities
from fri3d.utils.joystick_axis import JoystickAxis


class Joystick:
    def __init__(self):
        self.x = None
        self.y = None

        if hardware_capabilities.joystick:
            from fri3d.badge.hardware import hardware_joystick

            self.x = JoystickAxis(hardware_joystick.pinout.pin_joystick_x, dead_val=400)
            self.x.init()

            self.y = JoystickAxis(hardware_joystick.pinout.pin_joystick_y, dead_val=400)
            self.y.init()


joystick = Joystick()
