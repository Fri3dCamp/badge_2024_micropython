from micropython import const
from fri3d.badge.hardware.pin import HardwarePinInput


class HardwarePinout:
    class PinoutBuzzer:
        def __init__(self):
            self.pin_buzzer = const(32)

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = const(32)
            self.pin_dc = const(33)
            self.pin_cs = const(5)

    class PinoutGameOn:
        class PinoutButtons:
            def __init__(self):
                self.pin_a = HardwarePinInput(13, True)
                self.pin_b = HardwarePinInput(12, True)
                self.pin_start = HardwarePinInput(32, True)
                self.pin_select = HardwarePinInput(36, True)
                self.pin_p0 = HardwarePinInput(27, True)
                self.pin_p1 = HardwarePinInput(14, True)
                self.pin_up = HardwarePinInput(39, True)
                self.pin_left = HardwarePinInput(26, True)
                self.pin_down = HardwarePinInput(15, True)
                self.pin_right = HardwarePinInput(0, False)
                self.pin_p3 = HardwarePinInput(34, True)

        class PinoutSpeaker:
            def __init__(self):
                self.pin = const(25)

        class PinoutSDCard:
            def __init__(self):
                self.pin_cs = const(4)

        def __init__(self):
            self.pinout_buttons = self.PinoutButtons()
            self.pinout_speaker = self.PinoutSpeaker()
            self.pinout_sd_card = self.PinoutSDCard()

    class PinoutI2C:
        def __init__(self):
            self.sda = const(21)
            self.scl = const(22)

    class PinoutLEDS:
        def __init__(self):
            self.pin = const(2)

    class PinoutOnboardButtons:
        def __init__(self):
            self.pin_boot = HardwarePinInput(const(0), False)

    class PinoutSAO:
        def __init__(self, leds):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = const(23)
            self.pin_miso = const(19)
            self.pin_sck = const(18)

    def __init__(self):
        self.pinout_buzzer = self.PinoutBuzzer()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_gameon = self.PinoutGameOn()
        self.pinout_i2c = self.PinoutI2C()
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_onboard_buttons = self.PinoutOnboardButtons()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_spi = self.PinoutSPI()


hardware_pinout = HardwarePinout()
