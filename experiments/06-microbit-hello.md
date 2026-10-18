# 06 — micro:bit hello

**Question:** Can the Pi talk to the micro:bit sitting next to it?

**Answer:** Yes — by giving it a brain first, then a message.

## The idea

Mid-experiment, a micro:bit v2 got plugged into the Pi's USB port. The
request: *"show hi Tommaso on the micro bit display."* Simple — except the
micro:bit wasn't running anything that would listen.

## What was built

**Reconnaissance.** The micro:bit appeared as `/dev/ttyACM0` (serial) and as
a USB drive labeled `MICROBIT`. Its `DETAILS.TXT` showed DAPLink firmware on
a v2 board — but the serial REPL was completely silent. No MicroPython, no
conversation possible.

**The fix:** flash MicroPython with the message baked in, using `uflash`:

```bash
pip install --break-system-packages uflash
# src/mb-hi.py:
#   from microbit import *
#   display.scroll("hi Tommaso")
python3 -m uflash src/mb-hi.py
```

`uflash` writes a `micropython.hex` (firmware + embedded script) straight to
the `MICROBIT` drive. The board reboots, MicroPython starts, and `"hi
Tommaso"` scrolls across the 5×5 LED matrix. From plug-in to scrolling text:
a few minutes, most of it the flash itself.

## What was observed

- **The micro:bit is a peripheral with amnesia.** Out of the box (or with a
  stale MakeCode program), it won't talk serial. Flashing MicroPython turns
  it into a live Python device — REPL and all — which changes what "talk to
  the micro:bit" can mean afterward.
- **The 5×5 matrix has charm.** Lower resolution than the HAT's 8×8, but the
  scroll is buttery and the board sips power. It's the display you'd actually
  deploy on a battery.
- **Two LED matrices, two philosophies.** The HAT is driven live from the Pi
  (the Pi does the thinking); the micro:bit runs its own program (the
  thinking is onboard). Both were programmed from the same keyboard, in the
  same hour.

## Try it

```bash
pip install --break-system-packages uflash
printf 'from microbit import *\ndisplay.scroll("hello")\n' > hello.py
python3 -m uflash hello.py     # micro:bit reboots and scrolls
```

After flashing, the MicroPython REPL is live on `/dev/ttyACM0` (115200 baud)
— you can drive the display interactively with `pyserial`.

## Ideas for extension

- **Buttons as input:** `button_a.was_pressed()` in a loop — the micro:bit
  becomes a two-button remote for the Pi (advance the HAT slideshow, dismiss
  the beacon).
- **Radio link:** two micro:bits talking over their built-in radio — the Pi
  programs one, it relays to the other across the room.
- **Sensor reporter:** the micro:bit v2 has temperature and accelerometer
  onboard — flash a reporter script and read its sensors from the Pi over
  serial.
- **Scoreboard:** Pi keeps score, micro:bit displays it. The HAT shows the
  home team's color.
