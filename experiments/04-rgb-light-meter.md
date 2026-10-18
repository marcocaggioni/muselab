# 04 — RGB light meter

**Question:** Can the USB camera become a scientific instrument — a live
light meter with per-channel readout?

**Answer:** Yes, and the moment you wave your hand over the lens, you *feel*
it working.

## The idea

The request was the longest of the night, and the most specific: a web
dashboard showing the **live average intensity of the camera feed**, split
into red, green, and blue channels, so that covering the lens makes the
signal drop and uncovering it makes it rise. "Make me a nice and simple
dashboard… don't take too long."

## What was built

`src/rgb-meter.py` — a Flask app (port 8000) with two parts:

**Capture thread** (OpenCV, 320×240, ~5 fps):
```python
ok, frame = cap.read()
b, g, r = cv2.mean(frame)[:3]   # mean intensity per channel, 0–255
hist_r.append(r); hist_g.append(g); hist_b.append(b)
```
A rolling `deque(maxlen=120)` keeps ~24 seconds of history per channel.

**Dashboard** (single page, Chart.js from CDN):
- Three live line traces — red, green, blue — updating every 500 ms via
  `fetch('/data')`.
- Big current-value badges up top.
- Dark theme, phone-friendly. Open `http://<pi>:8000` and watch.

![RGB dashboard concept](images/rgb-concept.png)

## What was observed

- **It behaves like an instrument immediately.** Hand over the lens: all
  three traces dive. Pull away: they recover. Point at the warm desk lamp:
  red leads. The mapping from gesture to signal is instant and unambiguous —
  the hallmark of a good sensor demo.
- **Channels tell stories.** Under neutral light the three traces track
  together; under colored light they separate. You start *seeing* the color
  temperature of the room in the relative ordering of three lines.
- **Cheap parts, real data.** A sub-$30 USB camera plus ~60 lines of Python
  is a three-channel photometer. Not calibrated, not precise — but
  *responsive*, which is what an experiment needs first.

## Try it

```bash
pip install --break-system-packages opencv-python-headless flask
python3 src/rgb-meter.py
# open http://<this-pi>:8000 on your phone
```

## Ideas for extension

- **Calibration:** hold a known-gray card to the lens, map readings toward
  rough lux. Good enough for "is the grow-light on?" automation.
- **Event detection:** alert when mean intensity drops suddenly (someone
  walked past) or a channel dominates (colored status light turned on).
- **Timelapse:** log one reading per minute for a week; plot the daylight
  curve of the room.
- **Region of interest:** meter only the center crop — ignore the desk, watch
  the window.
- **Compare with the HAT:** overlay the Sense HAT's own ambient-light-free
  sensors (it has none — which is itself a lesson in what each board can
  and can't sense).
