# 07 — Cross-Pi sensing

**Question:** Can one Pi's sensor drive another Pi's display — two machines
acting as a single instrument?

**Answer:** 21.7 °C and 48.7 % humidity, read on Pi #1, scrolled in cyan on
Pi #2's Sense HAT a moment later.

## The idea

The lab had grown into two Pis with complementary hardware: Pi #1
(`pi4officiacase`) carried the TEMPerX232 USB temperature/humidity sensor;
Pi #2 (`pi4leddisplay`) carried the Sense HAT display. The test: *"get the
temperature and humidity from the Raspberry Pi that has the sensor and
display it both on the [Sense] HAT and [here]."*

No new wiring. No new hardware. Just a question about whether the two
machines could cooperate.

## What was built

Two one-liners, really:

**Read** (Pi #1, via the `temper-py` venv — the sensor speaks a plain-text
protocol over `/dev/ttyUSB0` at 9600 baud):
```python
import temper
r = temper.USBRead('ttyUSB0').read()
# {'firmware': 'TEMPerX232_V2.5', 'internal temperature': 21.73,
#  'internal humidity': 48.7}
```

**Display** (Pi #2, cyan scroll on the HAT via `src/show-temp.py`):
```python
sense.show_message("21.7C 48.7%", text_colour=[0, 255, 255])
```

The value traveled Pi #1 → agent → Pi #2, and appeared in chat at the same
time. The message beacon was briefly paused for the test, then resumed —
the unread chore reminder was still waiting in its file, untouched.

## What was observed

- **The network is the backplane.** Once every machine is reachable, "which
  Pi has the sensor" and "which Pi has the display" are just routing
  details. The two-Pi setup behaved like one instrument with a sensor on
  one end and a display on the other.
- **21.7 °C / 48.7 %** — a comfortable room, slightly dry for October. The
  number is unremarkable; the *path* it took is the experiment.
- **Heterogeneous hardware composes.** A $15 USB sensor stick from one
  vendor, a HAT from another, two Pis, one chat window — no integration
  project, no middleware, just a request.

## Try it

```bash
# on the Pi with the TEMPerX232:
~/temper-venv/bin/python -c "
import temper
print(temper.USBRead('ttyUSB0').read())"

# on the Pi with the Sense HAT:
python3 src/show-temp.py "21.7C 48.7%"
```

## Ideas for extension

- **Live bridge:** a tiny service on Pi #1 publishing sensor readings;
  Pi #2's beacon subscribes and shows them on a schedule — a permanent
  cross-Pi instrument.
- **Threshold alerts:** if humidity drops below 40 %, the HAT flashes amber
  until acknowledged (combine with experiment 01's beacon).
- **Sensor fusion dashboard:** one page showing the TEMPerX232 (Pi #1), the
  HAT's own temp/humidity/pressure (Pi #2), and the camera light meter
  (experiment 04) — the whole lab on one screen.
- **Logging:** append every reading to a CSV; a week later, plot the room's
  climate against the heating cycles.
