import lis2hh12

# this is an extenstion to lis2hh12 driver from https://github.com/tuupola/micropython-lis2hh12
# to enable the interrupt pin, so that badge-2022 display is on

# if you want to implement extra functionality (tapped, shaken) look at
# https://github.com/tinypico/tinypico-micropython/tree/master/lis3dh%20library

class LIS2HH12_int(lis2hh12.LIS2HH12):
    def enable_act_int(self):
        self._register_char(lis2hh12._CTRL6, 0x0A)
