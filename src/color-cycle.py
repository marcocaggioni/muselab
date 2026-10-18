#!/usr/bin/env python3
"""Cycle the Sense HAT LED matrix through full-screen red, green, blue,
one second each. Used together with rgb-meter.py to watch each camera
channel spike in turn."""
import time
from sense_hat import SenseHat

sense = SenseHat()
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
try:
    i = 0
    while True:
        sense.clear(colors[i % 3])
        i += 1
        time.sleep(1)
finally:
    sense.clear()
