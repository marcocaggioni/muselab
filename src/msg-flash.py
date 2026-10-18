#!/usr/bin/env python3
"""Flash-until-read message beacon for the Sense HAT.

Behavior:
- If ~/led-message.txt contains text: flash white/blue to attract attention.
- On any joystick press: scroll the message once (yellow), clear the file,
  and go dark until the next message arrives.
- If the file is empty: display stays dark.
"""
import time, os, select
from sense_hat import SenseHat
from evdev import InputDevice, list_devices

sense = SenseHat()
MSG_FILE = os.path.expanduser("~/led-message.txt")

joy = None
for p in list_devices():
    try:
        d = InputDevice(p)
        if "Sense HAT" in d.name:
            joy = d
            break
    except:
        pass

def get_message():
    try:
        return open(MSG_FILE).read().strip()
    except:
        return ""

def clear_message():
    open(MSG_FILE, "w").write("")

ON = (255, 255, 255)
OFF = (0, 0, 40)
sense.clear()
try:
    blink = True
    while True:
        msg = get_message()
        if msg:
            sense.clear(ON if blink else OFF)
            blink = not blink
        else:
            sense.clear()
        start = time.time()
        pressed = False
        while time.time() - start < 0.4:
            if joy:
                r, _, _ = select.select([joy.fd], [], [], 0.05)
                if r:
                    for ev in joy.read():
                        if ev.type == 1 and ev.value == 1:  # key press
                            pressed = True
                            break
                    if pressed:
                        break
            else:
                time.sleep(0.05)
        if pressed:
            msg = get_message()
            if msg:
                sense.clear()
                time.sleep(0.15)
                sense.show_message(msg, text_colour=[255, 255, 0],
                                   scroll_speed=0.07)
                clear_message()
            sense.clear()
finally:
    sense.clear()
