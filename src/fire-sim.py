#!/usr/bin/env python3
"""Doom-style fire simulation on the Sense HAT 8x8 LED matrix.

Heat rises from the bottom row and cools randomly as it climbs,
mapped through a black -> red -> orange -> yellow palette.
"""
import time, random
from sense_hat import SenseHat

sense = SenseHat()
W, H = 8, 8
heat = [[0] * W for _ in range(H)]

def heat_to_rgb(t):
    t = max(0, min(255, int(t)))
    if t < 85:
        return (t * 3, 0, 0)
    elif t < 170:
        return (255, (t - 85) * 3, 0)
    else:
        return (255, 255, (t - 170) * 3)

try:
    while True:
        for x in range(W):
            heat[H - 1][x] = 200 + random.randint(0, 55)
        for y in range(H - 2, -1, -1):
            for x in range(W):
                src_x = x + random.choice([-1, 0, 0, 1])
                src_x = max(0, min(W - 1, src_x))
                cooling = random.randint(0, 40)
                heat[y][x] = max(0, heat[y + 1][src_x] - cooling)
        for y in range(H):
            for x in range(W):
                sense.set_pixel(x, y, heat_to_rgb(heat[y][x]))
        time.sleep(0.06)
finally:
    sense.clear()
