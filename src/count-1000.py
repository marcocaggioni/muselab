#!/usr/bin/env python3
"""Scroll the numbers 1 to 1000 on the Sense HAT, one per second."""
import time
from sense_hat import SenseHat

sense = SenseHat()
try:
    for n in range(1, 1001):
        start = time.time()
        sense.show_message(str(n), text_colour=[0, 255, 0], scroll_speed=0.08)
        elapsed = time.time() - start
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
    sense.show_message("DONE!", text_colour=[255, 255, 0], scroll_speed=0.08)
finally:
    time.sleep(2)
    sense.clear()
