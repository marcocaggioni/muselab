# 05 — Color feedback loop

**Question:** Can the Pi *see its own display* — closing the loop from
actuator to sensor?

**Answer:** Put the Sense HAT under the camera, cycle red/green/blue, and
watch each dashboard channel spike in turn. The loop is closed.

## The idea

The request, verbatim in spirit: *"put the HAT under the camera, rotate
displaying red blue and green one every second, reopen the server — we should
see the different channel change according to the color rotation. Do it.
Fast."*

Two experiments from earlier in the night (the HAT as display, the camera as
light meter) snapped together into one: the Pi stimulating its own sensor.

## What was built

Two scripts, running simultaneously on the same Pi:

**`src/color-cycle.py`** — full-matrix color rotation:
```python
colors = [(255,0,0), (0,255,0), (0,0,255)]
while True:
    sense.clear(colors[i % 3])   # 1 second each: red → green → blue
    i += 1
    time.sleep(1)
```

**`src/rgb-meter.py`** (from experiment 04) — the dashboard, restarted,
watching the camera feed that now frames the glowing HAT.

## What was observed

- **Each channel spiked in turn.** Red screen → red trace jumps. Green →
  green jumps. Blue → blue jumps. The dashboard became a real-time
  verification that the display was doing what the code claimed — an
  independent measurement of the actuator, through optics, with no shared
  state between the two programs.
- **It's a closed loop with a human in it** — for now. The natural next step
  (see below) is to close it in software: read the dashboard's numbers back
  and let the program *decide* what to display.
- **Latency is visible.** The trace lags the color switch by a fraction of a
  second — capture interval, exposure, buffering. A feedback loop makes
  timing concrete in a way that staring at code never does.

## Try it

```bash
# terminal 1: cycle the colors
python3 src/color-cycle.py
# terminal 2: watch the light meter
python3 src/rgb-meter.py
# aim the USB camera at the HAT, open http://<pi>:8000
```

## Ideas for extension

- **Software-closed loop:** feed `/data` back into the display program —
  show green only until the green channel confirms, then advance. A true
  sense-and-respond cycle.
- **Latency measurement:** timestamp each color switch, find the spike in
  the trace, measure end-to-end delay. A real instrument characterization.
- **Color calibration:** sweep hues and record the camera's response curve —
  characterize *both* devices at once.
- **Follow-the-leader:** show on the HAT whatever color the camera sees most
  of — point it at a red mug, the matrix turns red.
