#!/usr/bin/env python
from AutoPilot.MultiWii import MultiWii

import pytest
import sys
import fake_rpi
import time

sys.modules['RPi'] = fake_rpi.RPi

try:
    from RPi.GPIO import GPIO
except:
    import RPi as RPi
    GPIO = RPi.GPIO

stack = []

@pytest.mark.parametrize('serial_port', [('/dev/ttyACM0')])     
class TestMultiWii():
    def test_arm(self, serial_port):
        board = MultiWii(serial_port=serial_port)
        assert board.SET_PID == 202
        