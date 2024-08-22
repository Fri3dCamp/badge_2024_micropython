from .pinout import hardware_pinout


class HardwareImu:
    def __init__(self):
        self.address = 0x6B
        self.accelero = True
        self.gyro = True


hardware_imu = HardwareImu()
