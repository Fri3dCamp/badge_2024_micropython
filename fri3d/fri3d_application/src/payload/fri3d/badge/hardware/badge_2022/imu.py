from .pinout import hardware_pinout


class HardwareImu:
    def __init__(self):
        self.address = 0x18
        self.accelero = True
        self.gyro = False



hardware_imu = HardwareImu()
