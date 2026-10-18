#!/usr/bin/env python3
"""Scroll a temperature/humidity reading once on the Sense HAT.
Usage: show-temp.py "21.7C 48.7%"
"""
from sense_hat import SenseHat
import sys

sense = SenseHat()
msg = sys.argv[1] if len(sys.argv) > 1 else "--"
sense.show_message(msg, text_colour=[0, 255, 255], scroll_speed=0.08)
sense.clear()
