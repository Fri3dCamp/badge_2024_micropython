import time

class Wsen_Isds:
    _ISDS_STATUS_REG = 0x1E  # Status data register

    _REG_G_X_OUT_L = 0x22
    _REG_G_Y_OUT_L = 0x24
    _REG_G_Z_OUT_L = 0x26

    _REG_A_X_OUT_L = 0x28
    _REG_A_Y_OUT_L = 0x2A
    _REG_A_Z_OUT_L = 0x2C
    
    _REG_A_TAP_CFG = 0x58

    _options = {
        'acc_range': {
            # range in REG_CTRL1_XL bits(0x10) bits [3:2]
            'reg': 0x10, 'mask': 0b11110011, 'shift_left': 2,
            'val_to_bits': {"2g": 0b00, "4g": 0b10, "8g": 0b11, "16g": 0b01}
        },
        'acc_data_rate': {
            # range in REG_CTRL1_XL bits(0x10) bits [7:4]
            'reg': 0x10, 'mask': 0b00001111, 'shift_left': 4,
            'val_to_bits': {
                "0": 0b0000, "1.6Hz": 0b1011, "12.5Hz": 0b0001,
                "26Hz": 0b0010, "52Hz": 0b0011, "104Hz": 0b0100,
                "208Hz": 0b0101, "416Hz": 0b0110, "833Hz": 0b0111,
                "1.66kHz": 0b1000, "3.33kHz": 0b1001, "6.66kHz": 0b1010}
        },
        'gyro_range': {
            # range in REG_CTRL2_G bits(0x11) bits [3:0]
            'reg': 0x11, 'mask': 0b11110000, 'shift_left': 0,
            'val_to_bits': {
                "125dps": 0b0010, "250dps": 0b0000, 
                "500dps": 0b0100, "1000dps": 0b1000, "2000dps": 0b1100}
        },
        'gyro_data_rate': {
            # range in REG_CTRL2_G bits(0x11) bits [7:4]
            'reg': 0x11, 'mask': 0b00001111, 'shift_left': 4,
            'val_to_bits': {
                "0": 0b0000, "12.5Hz": 0b0001, "26Hz": 0b0010,
                "52Hz": 0b0011, "104Hz": 0b0100, "208Hz": 0b0101,
                "416Hz": 0b0110, "833Hz": 0b0111, "1.66kHz": 0b1000,
                "3.33kHz": 0b1001, "6.66kHz": 0b1010}
        },
        'tap_double_enable': {
            # tap_double_enable in REG_WAKE_UP_THS(0x5B) bits [7]
            'reg': 0x5B, 'mask': 0b01111111, 'shift_left': 7,
            'val_to_bits': {True: 0b01, False: 0b00}
        },
        'tap_threshold': {
            # tap_threshold in TAP_THS_6D(0x59) bits [4:0]
            # Set tap threshold (5 bits, 1bit = 1 * full_scale / 32)
            'reg': 0x59, 'mask': 0b11100000, 'shift_left': 0,
            'val_to_bits': {0: 0b00, 1: 0b01, 2: 0b10, 3: 0b11, 4: 0b100, 5: 0b101,
                            6: 0b110, 7: 0b111, 8: 0b1000, 9: 0b1001}
        },
        'tap_quiet_time': {
            # tap_quiet_time in INT_DUR2(0x5A) bits [3:2]
            # Set quiet time(1 bit = 1 * 4 / ODR)
            'reg': 0x5A, 'mask': 0b11110011, 'shift_left': 2,
            'val_to_bits': {0: 0b00, 1: 0b01, 2: 0b10, 3: 0b11}
        },
        'tap_duration_time': {
            # tap_duration_time in INT_DUR2(0x5A) bits [7:4]
            # Set duration time(1 bit = 1 * 32 / ODR)
            'reg': 0x5A, 'mask': 0b00001111, 'shift_left': 2,
            'val_to_bits': {0: 0b00, 1: 0b01, 2: 0b10, 3: 0b11, 4: 0b100, 5: 0b101,
                            6: 0b110, 7: 0b111, 8: 0b1000, 9: 0b1001}
        },
        'tap_shock_time': {
            # tap_shock_time in INT_DUR2(0x5A) bits [1:0]
            # Set shock time(1 bit = 1 * 32 / ODR)
            'reg': 0x5A, 'mask': 0b11111100, 'shift_left': 0,
            'val_to_bits': {0: 0b00, 1: 0b01, 2: 0b10, 3: 0b11}
        },
        'tap_single_to_int0': {
            # tap_single_to_int0 in MD1_CFG(0x5E) bits [6]
            'reg': 0x5E, 'mask': 0b10111111, 'shift_left': 6,
            'val_to_bits': {0: 0b00, 1: 0b01}
        },
        'tap_double_to_int0': {
            # tap_double_to_int0 in MD1_CFG(0x5E) bits [3]
            'reg': 0x5E, 'mask': 0b11110111, 'shift_left': 3,
            'val_to_bits': {0: 0b00, 1: 0b01}
        },
        'int1_on_int0': {
            # CTRL4_(0x13) bits [5] True enables all interrupt signals available on INT0 pad.
            'reg': 0x13, 'mask': 0b11011111, 'shift_left': 5,
            'val_to_bits': {0: 0b00, 1: 0b01}
        },
        'ctrl_do_soft_reset': {
            # CTRL3_C(0x12) bits [0]
            'reg': 0x12, 'mask': 0b11111110, 'shift_left': 0,
            'val_to_bits': {True: 0b01, False: 0b00}
        },
        'ctrl_do_reboot': {
            # CTRL3_C(0x12) bits [0]
            'reg': 0x12, 'mask': 0b01111111, 'shift_left': 7,
            'val_to_bits': {True: 0b01, False: 0b00}
        },
    }

    def __init__(self, i2c, address=0x6B, acc_range="2g", acc_data_rate="1.6Hz", gyro_range="125dps", gyro_data_rate="12.5Hz"):
        """
        Initializes the accelerometer with the specified I2C and address.
        """
        self.i2c = i2c
        self.address = address

        self.acc_offset_x = 0
        self.acc_offset_y = 0
        self.acc_offset_z = 0        
        self.acc_range = 0
        self.acc_sensitivity = 0

        self.gyro_offset_x = 0
        self.gyro_offset_y = 0
        self.gyro_offset_z = 0
        self.gyro_range = 0
        self.gyro_sensitivity = 0

        self.ACC_NUM_SAMPLES_CALIBRATION = 5
        self.ACC_CALIBRATION_DELAY_MS = 10

        self.GYRO_NUM_SAMPLES_CALIBRATION = 5
        self.GYRO_CALIBRATION_DELAY_MS = 10

        self.set_acc_range(acc_range)
        self.set_acc_data_rate(acc_data_rate)

        self.set_gyro_range(gyro_range)
        self.set_gyro_data_rate(gyro_data_rate)

    def _write_option(self, option, value):
        """
        """
        opt = Wsen_Isds._options[option]
        try:
            bits = opt["val_to_bits"][value]
            print(option)
            print(bits)
            # Read current configuration, mask out existing bits, and write back new value
            config_value = self.i2c.readfrom_mem(self.address, opt["reg"], 1)[0]
            config_value &= opt["mask"]
            config_value |= (bits << opt["shift_left"])
            self.i2c.writeto_mem(self.address, opt["reg"], bytes([config_value]))
        except KeyError as err:
            print(f"Invalid option: {option}, or invalid option value: {value}.", err)

    def set_acc_range(self, acc_range):
        """
        Sets the measurement range of the accelerometer.
        Possible range values: "±2g", "±4g", "±8g", "±16g".
        """
        self._write_option('acc_range', acc_range)
        self.acc_range = acc_range
        print("Accelerometer range set to", self.acc_range)
        self._acc_calc_sensitivity()

    def set_acc_data_rate(self, acc_rate):
        """
        Sets the data rate (output frequency) of the accelerometer.
        """
        self._write_option('acc_data_rate', acc_rate)
        print("Accelerometer data rate set to", acc_rate)

    def set_gyro_range(self, gyro_range):
        """
        Sets the measurement range of the gyroscope.
        Possible range values: "±125 dps", "±250 dps", "±500 dps", "±1000 dps", "±2000 dps".
        """
        self._write_option('gyro_range', gyro_range)
        self.gyro_range = gyro_range
        print("Gyroscope range set to", self.gyro_range)
        self._gyro_calc_sensitivity()

    def set_gyro_data_rate(self, gyro_rate):
        """
        Sets the data rate (output frequency) of the gyroscope.
        Possible rate values: "0" for off, or "12.5Hz", "26Hz", "52Hz", "104Hz", "208Hz", "416Hz", "833Hz", "1.66kHz", "3.33kHz", and "6.66kHz"
        """
        self._write_option('gyro_data_rate', gyro_rate)
        print("Gyroscope data rate set to", gyro_rate)

    def _gyro_calc_sensitivity(self):
        """
        Sets the Gyroscope sensitivity value based on the selected full-scale range.
        """
        # Map range values to corresponding sensitivity values
        sensitivity_mapping = {
            "125dps": 4.375,
            "250dps": 8.75,
            "500dps": 17.5,
            "1000dps": 35,
            "2000dps": 70
        }

        # Check if the provided range is valid
        if self.gyro_range in sensitivity_mapping:
            # Set the sensitivity value
            self.gyro_sensitivity = sensitivity_mapping[self.gyro_range]
            print("Sensitivity set to", self.gyro_sensitivity, "mdps/digit")
        else:
            print("Invalid range value:", self.gyro_range)


    def soft_reset(self):
        """
        Performs a soft reset of the gyroscope/accelerometer.
        """
        self._write_option('ctrl_do_soft_reset', True)
        print("Soft reset performed.")

    def reboot(self):
        """
        Performs a reboot of the gyroscope/accelerometer.
        """
        self._write_option('ctrl_do_reboot', True)
        print("Reboot performed.")

    def set_interrupt(self, interrupts_enable=False, inact_en=False, slope_fds=False,
                      tap_x_en=True, tap_y_en=True, tap_z_en=True):
        """
        Enables or disables interrupt for tap gestures.
        """
        config_value = 0b00000000  # Initialize config value

        # Set corresponding bits based on arguments
        if interrupts_enable:
            config_value |= (1 << 7)
        if inact_en:
            inact_en = 0x01
            config_value |= (inact_en << 5)
        if slope_fds:
            config_value |= (1 << 4)
        if tap_x_en:
            config_value |= (1 << 3)
        if tap_y_en:
            config_value |= (1 << 2)
        if tap_z_en:
            config_value |= (1 << 1)

        print("Interrupt for tap gestures configured.")

        # Write the new configuration value to TAP_CFG register
        self.i2c.writeto_mem(self.address, Wsen_Isds._REG_TAP_CFG, bytes([config_value]))

        # based on https://github.com/WurthElektronik/Sensors-SDK_STM32/blob/main/examples/WSEN_ISDS_TAP/WSEN_ISDS_TAP_EXAMPLE.c#L82

        self._write_option('tap_double_enable', False)
        self._write_option('tap_threshold', 9)
        # Set quiet time, corresponds to 1 * 4 / 400 = 10 ms
        self._write_option('tap_quiet_time', 1)
        # Set duration time, corresponds to 5 * 32 / 400 = 400ms
        self._write_option('tap_duration_time', 5)
        # Set shock time, corresponds to 2 * 8 / 400 = 40 ms
        self._write_option('tap_shock_time', 2)
        # Write the MD1_CFG register to route the events to interrupt 0
        self._write_option('tap_single_to_int0', 1)
        self._write_option('tap_double_to_int0', 1)
        # enable all IRQs on INT0 pad
        self._write_option('int1_on_int0', 1)

    def acc_calibrate(self):
        """
        Performs accelerometer calibration.
        """
        print("Calibrating accelerometer...")
        for _ in range(self.ACC_NUM_SAMPLES_CALIBRATION):
            x, y, z = self._read_raw_accelerations()
            self.acc_offset_x += x
            self.acc_offset_y += y
            self.acc_offset_z += z
            time.sleep_ms(self.CALIBRATION_DELAY_MS)  # Delay between samples

        # Calculate average offsets
        self.acc_offset_x //= self.ACC_NUM_SAMPLES_CALIBRATION
        self.acc_offset_y //= self.ACC_NUM_SAMPLES_CALIBRATION
        self.acc_offset_z //= self.ACC_NUM_SAMPLES_CALIBRATION

        print(f"Accelerometer calibration completed ({self.acc_offset_x},{self.acc_offset_y},{self.acc_offset_z}).")

    def _acc_calc_sensitivity(self):
        """
        Sets the sensitivity value based on the selected full-scale range.
        """
        sensitivity_mapping = {
            "2g": 0.061,
            "4g": 0.122,
            "8g": 0.244,
            "16g": 0.488
        }
        if self.acc_range in sensitivity_mapping:
            self.acc_sensitivity = sensitivity_mapping[self.range]
            print("Sensitivity set to", self.acc_sensitivity, "mg/digit")
        else:
            print("Invalid range value:", self.acc_range)

    def read_accelerations(self):
        """
        Reads and returns the acceleration from the 3 axis, all in one read, so the values correspond.
        """
        # Get the raw value
        raw_a_x, raw_a_y, raw_a_z = self._read_raw_accelerations()

        # Apply offset and sensitivity
        a_x = (raw_a_x - self.acc_offset_x) * self.acc_sensitivity
        a_y = (raw_a_y - self.acc_offset_y) * self.acc_sensitivity
        a_z = (raw_a_z - self.acc_offset_z) * self.acc_sensitivity

        return a_x, a_y, a_z

    def _read_raw_accelerations(self):
        """
        Reads and returns the raw acceleration from the 3 axis, all in one read, so the values correspond.
        """
        if not self._acc_data_ready():
            raise Exception("sensor data not ready")

        # Read the accelerometer data starting from x axis lower output register, 6 (3x2) bytes
        raw = self.i2c.readfrom_mem(self.address, Wsen_Isds._REG_G_X_OUT_L, 6)

        raw_a_x = self._convert_from_raw(raw[0], raw[1])
        raw_a_y = self._convert_from_raw(raw[2], raw[3])
        raw_a_z = self._convert_from_raw(raw[4], raw[5])

        return raw_a_x, raw_a_y, raw_a_z


    def gyro_calibrate(self):
        """
        Performs gyroscope calibration.
        """
        print("Calibrating gyroscope...")
        for _ in range(self.GYRO_NUM_SAMPLES_CALIBRATION):
            x, y, z = self._read_raw_angular_velocities()
            self.offset_x += x
            self.offset_y += y
            self.offset_z += z
            time.sleep_ms(self.GYRO_CALIBRATION_DELAY_MS)  # Delay between samples

        # Calculate average offsets
        self.offset_x //= self.GYRO_NUM_SAMPLES_CALIBRATION
        self.offset_y //= self.GYRO_NUM_SAMPLES_CALIBRATION
        self.offset_z //= self.GYRO_NUM_SAMPLES_CALIBRATION

        print(f"Gyroscope calibration completed ({self.offset_x},{self.offset_y},{self.offset_z}).")

    def read_angular_velocities(self):
        """
        Reads and returns the angular velocity from the 3 axis, all in one read, so the values correspond.
        """
        # Get the raw value
        raw_g_x, raw_g_y, raw_g_z = self._read_raw_angular_velocities()

        # Apply offset and sensitivity
        g_x = (raw_g_x - self.gyro_offset_x) * self.gyro_sensitivity
        g_y = (raw_g_y - self.gyro_offset_y) * self.gyro_sensitivity
        g_z = (raw_g_z - self.gyro_offset_z) * self.gyro_sensitivity

        return g_x, g_y, g_z

    def _read_raw_angular_velocities(self):
        """
        Reads and returns the raw angular velocity from the 3 axis, all in one read, so the values correspond.
        """
        if not self._gyro_data_ready():
            raise Exception("sensor data not ready")

        # Read the gyroscope data starting from x axis lower output register, 6 (3x2) bytes
        raw = self.i2c.readfrom_mem(self.address, Wsen_Isds.REG_G_X_OUT_L, 6)

        raw_g_x = self._convert_from_raw(raw[0], raw[1])
        raw_g_y = self._convert_from_raw(raw[2], raw[3])
        raw_g_z = self._convert_from_raw(raw[4], raw[5])

        return raw_g_x, raw_g_y, raw_g_z


    def read_angular_velocities_accelerations(self):
        """
        Reads and returns the angular velocity and accelerations from the 3 axis, all in one read, so the values correspond.
        """
        # Get the raw value
        raw_g_x, raw_g_y, raw_g_z, raw_a_x, raw_a_y, raw_a_z = self._read_raw_gyro_acc()

        # Apply offset and sensitivity
        g_x = (raw_g_x - self.gyro_offset_x) * self.gyro_sensitivity
        g_y = (raw_g_y - self.gyro_offset_y) * self.gyro_sensitivity
        g_z = (raw_g_z - self.gyro_offset_z) * self.gyro_sensitivity
        
        a_x = (raw_a_x - self.acc_offset_x) * self.acc_sensitivity
        a_y = (raw_a_y - self.acc_offset_y) * self.acc_sensitivity
        a_z = (raw_a_z - self.acc_offset_z) * self.acc_sensitivity

        return g_x, g_y, g_z, a_x, a_y, a_z

    def _read_raw_gyro_acc(self):
        """
        Reads and returns the raw angular velocity from the 3 axis, all in one read, so the values correspond.
        """
        acc_data_ready, gyro_data_ready = self._acc_gyro_data_ready()
        if not acc_data_ready or not gyro_data_ready:
            raise Exception("sensor data not ready")

        # Read the gyroscope data starting from x axis lower output register, 6 (3x2) bytes
        raw = self.i2c.readfrom_mem(self.address, Wsen_Isds.REG_G_X_OUT_L, 12)

        raw_g_x = self._convert_from_raw(raw[0], raw[1])
        raw_g_y = self._convert_from_raw(raw[2], raw[3])
        raw_g_z = self._convert_from_raw(raw[4], raw[5])

        raw_a_x = self._convert_from_raw(raw[6], raw[7])
        raw_a_y = self._convert_from_raw(raw[8], raw[9])
        raw_a_z = self._convert_from_raw(raw[10], raw[11])

        return raw_g_x, raw_g_y, raw_g_z, raw_a_x, raw_a_y, raw_a_z

    def _convert_from_raw(b_l, b_h):
        # Combine low and high bytes to form 16-bit value (two's complement)
        c = (b_h << 8) | b_l
        if c & (1 << 15):  # Check if value is negative
            c -= 1 << 16  # Convert to negative value
        return c
    
    def _acc_data_ready(self):
        return self._get_status_reg[0]

    def _gyro_data_ready(self):
        return self._get_status_reg[1]
    
    def _acc_gyro_data_ready(self):
        status_reg = self._get_status_reg()
        return status_reg[0], status_reg[1]

    def _get_status_reg(self):
        """
        /**
        * @brief ISDS_STATUS_REG
        *
        * Address 0x1E
        * Type  R
        * Default value: 0x00
        */
        typedef struct
        {
            uint8_t accDataReady : 1;               /**< 1: New acceleration data available; 0: No new data available. */
            uint8_t gyroDataReady : 1;              /**< 1: New gyroscope data available; 0: No new data available. */
            uint8_t tempDataReady: 1;               /**< 1: New temperature data available; 0: No new data available. */
            uint8_t notUsed01 : 5;                  /**< These bits must be set to 0 for proper operation of the device. */
        } ISDS_status_t;        
        
        """
        raw = self.i2c.readfrom_mem(self.address, Wsen_Isds._ISDS_STATUS_REG, 4)
        
        acc_data_ready = True if raw[0] == 1 else False
        gyro_data_ready = True if raw[1] == 1 else False
        temp_data_ready = True if raw[2] == 1 else False

        return acc_data_ready, gyro_data_ready, temp_data_ready