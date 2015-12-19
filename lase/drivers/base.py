#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

from ..signal import Sampling
from ..core import Device, command, write_buffer
#from ..core import Dac


class Base(Device):
    """ This class is used as a base class for `Oscillo` and `Spectrum`

    args:
        n (int): number of points in the waveform (ex: n = 8192).
        client : instance of KClient class, used to connect to the board.
    """

    def __init__(self, dac_wfm_size, client, map_size=4096):
        super(Base, self).__init__(client)
        self.open(dac_wfm_size)

        self.client = client

        self.n = dac_wfm_size
        # Number of points in the waveform 'ex : n = 8192'
        self.max_current = 50  # mA
        self.sampling = Sampling(dac_wfm_size, 125e6)

        self.opened = True
        self.dac = np.zeros((2, self.sampling.n))

    @command
    def open(self, dac_wfm_size):
        pass

    def update(self):
        pass  # Used in BaseSimu

    def close(self):
        self.reset()

    @command
    def reset(self):
        pass

    @command
    def start_laser(self):
        """ Start laser emission """
        pass

    @command
    def stop_laser(self):
        """ Stop laser emission """
        pass

    @command
    def get_laser_current(self):
        current = self.client.recv_int(4)

        if math.isnan(current):
            print("Can't read laser current")
            self.is_failed = True

        return current

    @command
    def get_laser_power(self):
        power = self.client.recv_int(4)

        if math.isnan(power):
            print("Can't read laser power")
            self.is_failed = True

        return power

    @command
    def get_monitoring(self):
        return self.client.recv_tuple()

    @command
    def set_laser_current(self, current):
        """ Set the current bias of the laser diode

        Args:
            - current: The bias in mA
        """
        pass

    @write_buffer
    def set_dac_buffer(self, data):
        pass

    def set_dac(self, warning=False, reset=False):
        if warning:
            if np.max(np.abs(self.dac)) >= 1:
                print('WARNING : dac out of bounds')
        dac_data_1 = np.mod(np.floor(8192 * self.dac[0, :]) + 8192,16384) + 8192
        dac_data_2 = np.mod(np.floor(8192 * self.dac[1, :]) + 8192,16384) + 8192
        self.set_dac_buffer(dac_data_1 + 65536 * dac_data_2)

        if reset:
            self.reset_acquisition()

    @command
    def get_bitstream_id(self):
        pass

    @command
    def set_led(self, value):
        pass

    @command
    def reset_acquisition(self):
        pass