# 03 — Counter 1–1000

**Question:** What does a thousand look like, one second at a time?

**Answer:** Longer than you'd think, and weirdly meditative.

## The idea

Two requests, eleven words total: *"Make a display that count 1-1000"* …
*"One sec interval."* The result: every integer from 1 to 1000, scrolled
across the LED matrix in green, each number owning exactly one second.

At 1 Hz, the full run takes about 17 minutes. Nobody watched all of it. That
wasn't the point.

## What was built

`src/count-1000.py` — deliberately the simplest script of the night:

```python
for n in range(1, 1001):
    start = time.time()
    sense.show_message(str(n), text_colour=[0, 255, 0], scroll_speed=0.08)
    elapsed = time.time() - start
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)   # hold the 1-second cadence
```

The scroll itself takes a fraction of a second for short numbers; the sleep
tops each step up to exactly one second. When the loop ends, `"DONE!"` scrolls
in yellow and the matrix clears.

## What was observed

- **Time has texture.** You *know* a thousand seconds is ~17 minutes, but
  watching 1… 2… 3… tick by at human pace makes it visceral in a way the
  arithmetic never does. Around 300, it starts feeling long. That's the
  experiment working.
- **Counting is a display primitive.** Once you can put any number on the
  matrix at a fixed cadence, you have a stopwatch, a countdown timer, a
  scoreboard, a queue-number display. The demo is trivial; the capability
  isn't.
- **Constraints breed clarity.** One-second cadence, one color, one font of
  necessity (5×8-ish glyphs on an 8×8 grid). Nothing to fiddle with, so all
  attention goes to the phenomenon: *duration itself*.

## Try it

```bash
pip install --break-system-packages sense-hat
python3 src/count-1000.py    # ~17 minutes; Ctrl-C to stop early
```

## Ideas for extension

- **Countdown mode:** from N to zero, then flash — a kitchen timer with no
  phone involved.
- **Sensor-driven counting:** increment on each joystick press; decrement on
  shake (accelerometer) — a physical tally counter.
- **Variable cadence:** 10 Hz for the first hundred (a blur), 1 Hz after —
  feel logarithmic time.
- **Binary/hex counter:** same loop, different base. Watch bit patterns march.
