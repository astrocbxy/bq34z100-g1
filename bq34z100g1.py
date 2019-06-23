"""
Created on Tue Sep 26 18:39:18 2017

@author: chris
"""

from smbus import SMBus


class bq34z100g1(object):

    def __init__(self, address=0x55, bus=1):
        self._address = address
        self._bus = SMBus(bus)

    @staticmethod
    def log(msg):
        print(msg)

    @staticmethod
    def ftol(byte: int):
        liste = []
        liste.append(1) if byte & 1 > 0 else liste.append(0)
        liste.append(1) if byte & 2 > 0 else liste.append(0)
        liste.append(1) if byte & 4 > 0 else liste.append(0)
        liste.append(1) if byte & 8 > 0 else liste.append(0)
        liste.append(1) if byte & 16 > 0 else liste.append(0)
        liste.append(1) if byte & 32 > 0 else liste.append(0)
        liste.append(1) if byte & 64 > 0 else liste.append(0)
        liste.append(1) if byte & 128 > 0 else liste.append(0)
        return liste

    def openConfig(self):
        self._bus.write_word_data(self._address, 0x00, 0x0414)
        self._bus.write_word_data(self._address, 0x00, 0x3672)
        self._bus.write_byte_data(self._address, 0x61, 0x00)

    def setConfig(self):
        self.openConfig()
        self._bus.write_byte_data(self._address, 0x3e, 0x30)
        self._bus.write_byte_data(self._address, 0x3f, 0x00)
        # self._bus.write_byte_data(self._address, 0x4a, 0x00)
        # self._bus.write_byte_data(self._address, 0x4b, 0x00)

    def _writeValue(self, cmd, text):
        try:
            self._bus.write_word_data(self._address, cmd, text)
        except:
            bq34z100g1.log("Couldn't write to i2c bus")

    def _readValue(self, register: int, length: int = 2) -> int:
        try:
            if length == 2:
                return self._bus.read_word_data(self._address, register)
            if length == 1:
                return self._bus.read_byte_data(self._address, register)
            else:
                print("is not supported by now") # do again two times?
                return -1
        except:
            bq34z100g1.log("Could not read i2c bus")
            return -1

    def _readSignedValue(self, register: int, length: int = 2) -> int:
        value = self._readValue(register, length)
        if length == 2:
            if value <= 32767:
                return value
            else:
                return value - 65535
        if length == 1:
            if value <= 128:
                return value
            else:
                return value - 256

    def get_temperature(self):  # 0x0c
        """returns Temperature in °C"""
        return round((self._readValue(0x0C) * 0.1) - 273.15, 2)

    def get_internal_temperature(self):  # 0x2a
        """return internal Temperature in °C"""
        return round((self._readValue(0x2A) * 0.1) - 273.15, 2)

    def get_voltage(self):  # 0x08,0x09
        """return Voltage in mV"""
        return self._readValue(0x08)

    def get_current(self):  # 0x10,0x11
        """returns Current in mA"""
        return self._readSignedValue(0x10)

    def get_power(self):  # 0x26,0x27
        """returns current Power Usage"""
        return self._readSignedValue(0x26)

    def get_capacity(self):  # 0x04,0x05
        """returns Capacity in mAh"""
        return self._readValue(0x04)

    def get_full_capacity(self):  # 0x06,0x07
        """returns Capacity when full in mAh"""
        return self._readValue(0x06)

    def get_design_capacity(self):  # 0x0c,0x0d
        """returns Design Capacity in mAh"""
        return self._readValue(0x3C)

    def get_cycle_count(self):  # 0x2c
        """returns the amount of Cycles the Battery has run"""
        return self._readValue(0x2C, 1)

    def get_state_of_charge(self):  # 0x02
        """return State of Charge in %"""
        return self._readValue(0x02, 1)

    def get_flagsa(self):  #0x0e, 0x0f
        return str(str(self.ftol(int(self._readValue(0x0e, 1)))) + "\n" + str(self.ftol(int(self._readValue(0x0f, 1)))))

    def get_flagsb(self):  #0x12, 0x13
        return str(str(self.ftol(int(self._readValue(0x12, 1)))) + "\n" + str(self.ftol(int(self._readValue(0x13, 1)))))

    def get_ctrl_statusa(self):
        return self.ftol(int(self._readValue(0x00, 1)))

    def get_ctrl_statusb(self):
        return self.ftol(int(self._readValue(0x01, 1)))

    def get_max_error(self):
        return self._readValue(0x03, 1)

    def get_avg_time_to_empty(self):
        return self._readValue(0x18)

    def get_avg_time_to_full(self):  # 0x1a,0x1b
        return self._readValue(0x1A)

    def get_state_of_health(self):  # 0x2e,0x2f
        return self._readValue(0x2E)

    def get_qmax_time(self):
        return self._readValue(0x74)

    def get_learned_status(self):
        return self.ftol(int(self._readValue(0x63,1)))
