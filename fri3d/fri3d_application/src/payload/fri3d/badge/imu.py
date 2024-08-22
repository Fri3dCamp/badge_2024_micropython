from p0tat0.badge import badge_type, FRI3D_BADGE_2022, FRI3D_BADGE_2024

from fri3d.badge.hardware import hardware_imu
from .i2c import i2c


class Imu:
    @property
    def accel(self):
        return (None, None, None)
    
    @property
    def gyro(self):
        return (None, None, None)

    @property
    def accel_gyro(self):
        return self.accel(), self.gyro()


if badge_type == FRI3D_BADGE_2022:

    from lis2hh12_int import LIS2HH12_int

    class LisImu(Imu):
        def __init__(self, lis2hh12_int):
            self.lis = lis2hh12_int
            
            # enable the interrupt pin, this controls the display backlight
            self.lis.enable_act_int()

        @property
        def accel(self):
            return self.lis.acceleration()

    lis2hh12_int = LIS2HH12_int(i2c=i2c, address=hardware_imu.address)
    imu = LisImu(lis2hh12_int)

elif badge_type == FRI3D_BADGE_2024:

    from wsen_isds import Wsen_Isds

    class WsenIsdsImu(Imu):
        def __init__(self, wsen_isds):
            self.wsen_isds = wsen_isds
            
        @property
        def accel(self):
            return self.wsen_isds.read_accelerations()

        @property
        def gyro(self):
            return self.wsen_isds.read_angular_velocities()

    wsen_isds = Wsen_Isds(i2c=i2c, address=hardware_imu.address)
    imu = Imu(wsen_isds)


else:
    raise(OSError("Unknown badge type"))
