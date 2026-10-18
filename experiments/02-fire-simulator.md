# 02 — Fire simulator

**Question:** Can 64 pixels look like fire?

**Answer:** Alarmingly, yes.

## The idea

The request was five words long: *"Show me the fire simulator."* A few
minutes later the 8×8 matrix was flickering with something your lizard brain
immediately files under *flame*. No assets, no images — just an algorithm
from 1990s demo-scene lore doing all the work.

## What was built

`src/fire-sim.py` — the classic Doom fire algorithm, adapted for an 8×8 grid:

1. **Heat field.** An 8×8 array of "temperature" values, 0–255.
2. **Fuel.** Every frame, the bottom row is re-seeded with high random heat
   (200–255). This is the fire's source.
3. **Rise and cool.** Each cell takes heat from the cell below it, with a
   random horizontal jitter (−1…+1) and random cooling (0–40). Heat
   decays as it climbs — exactly like a real flame losing energy.
4. **Palette.** Heat maps to color: black → deep red → orange → yellow-white.

```python
for y in range(H-2, -1, -1):          # bottom-up
    for x in range(W):
        src = clamp(x + random.choice([-1,0,0,1]))
        heat[y][x] = max(0, heat[y+1][src] - random.randint(0, 40))
```

At ~16 fps on the tiny matrix, the randomness reads as turbulence. Your eye
does the rest.

## What was observed

- On 64 LEDs there is no detail — and none is needed. Flicker rate, upward
  motion, and the red→yellow gradient are sufficient cues; the brain
  supplies "fire" for free.
- It looks *better* slightly out of focus or at a glance — the same reason
  stage fire works.
- The algorithm is O(64) per frame. The Pi doesn't even notice.

## Try it

```bash
pip install --break-system-packages sense-hat
python3 src/fire-sim.py     # Ctrl-C to stop; clears the matrix on exit
```

## Ideas for extension

- **Wind:** tilt the HAT and let the accelerometer bend the flames sideways.
- **Palettes:** blue "gas flame", green "alien fire", purple plasma.
- **Interactive:** blow on the (separate) temperature sensor to stoke it —
  heat source strength follows the reading.
- **Bigger canvas:** tile the algorithm across a Unicorn HAT HD (16×16) or
  an LED strip; the math scales unchanged.
- **Ember mode:** let the fuel sputter — random dropouts in the bottom row
  for a dying-fire effect.
