#!/usr/bin/env python3
"""Generate 5 diagram images for the midland repo. Dark 'night lab' theme."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

OUT = os.path.expanduser('~/workspace/midland/images')
BG = '#16161f'
PANEL = '#1f1f2b'
TXT = '#e8e8f0'
DIM = '#8a8a99'
ACCENT = '#00d4ff'
GREEN = '#39d353'
AMBER = '#ffb020'
RED = '#ff5555'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'text.color': TXT,
})

def new_fig(w, h, dpi=100):
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax

def panel(ax, x, y, w, h, title, title_color=ACCENT, fs=22):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=8,rounding_size=14",
                         facecolor=PANEL, edgecolor='#3a3a4d', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 28, title, ha='center', va='top', fontsize=fs,
            color=title_color, weight='bold')
    return box

def item(ax, x, y, text, color=TXT, fs=17, ha='left', weight='normal', **kw):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=color, weight=weight, **kw)

def arrow(ax, x1, y1, x2, y2, label=None, color=ACCENT, ls='-', lw=2.2, rad=0.0, fs=14):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                        color=color, linewidth=lw, linestyle=ls,
                        connectionstyle=f'arc3,rad={rad}',
                        mutation_scale=18, shrinkA=4, shrinkB=6)
    ax.add_patch(a)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2 + 16
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=fs,
                color=color, style='italic')

# ---------------------------------------------------------------- 1. architecture
def architecture():
    W, H = 1600, 1000
    fig, ax = new_fig(W, H)
    ax.text(W/2, 968, 'MUSELAB — Night-Lab System Architecture', ha='center', va='top',
            fontsize=27, weight='bold', color=TXT)
    ax.text(W/2, 924, 'Two Raspberry Pi 4s · Sense HAT · USB sensors · natural-language control via Muse Gadget',
            ha='center', va='top', fontsize=13, color=DIM)

    # Experimenter: single centered line, no box
    ax.text(W/2, 822, 'Experimenter  ·  laptop / phone  ·  natural-language requests',
            ha='center', va='center', fontsize=16, color=AMBER, weight='bold')

    # Pi panels
    pw = 600
    p1x, p2x, py, ph = 70, W-70-pw, 130, 600
    panel(ax, p1x, py, pw, ph, 'Pi #1 · pi4officiacase', GREEN, 18)
    ax.text(p1x+pw/2, py+ph-56, '192.168.68.77', ha='center', va='top', fontsize=12, color=DIM)
    panel(ax, p2x, py, pw, ph, 'Pi #2 · pi4leddisplay', GREEN, 18)
    ax.text(p2x+pw/2, py+ph-56, '192.168.68.78', ha='center', va='top', fontsize=12, color=DIM)

    def rows(x0, y0, entries):
        y = y0
        for bold_text, sub in entries:
            item(ax, x0, y, '› ' + bold_text, fs=14, weight='bold')
            y -= 24
            if sub:
                item(ax, x0+26, y, sub, fs=11.5, color=DIM)
                y -= 21
            y -= 12

    rows(p1x+24, py+ph-104, [
        ('TEMPerX232 sensor', 'temperature + humidity, 9600 baud'),
        ('USB camera', 'room photos for Kindle dashboard'),
        ('Kindle server :8000', 'photo + readings every 10 min'),
        ('Muse Gadget (e88a1e)', 'paired · online'),
        ('cron: sensor-cam-dashboard.py', ''),
        ('Kindle 4 (D01100) on LAN', ''),
    ])
    rows(p2x+24, py+ph-104, [
        ('Sense HAT v1.0', '8x8 LED matrix + joystick + sensors'),
        ('USB microscope camera', 'watches the LED matrix'),
        ('micro:bit v2 (ttyACM0)', '5x5 LED via MicroPython'),
        ('Muse Gadget (6985CF)', 'paired · online'),
        ('flash-until-read messages', ''),
        ('fire sim · RGB meter · demos', ''),
    ])

    # LAN box below, centered in the gap
    lanx, lanw = W/2-150, 300
    lan = FancyBboxPatch((lanx, 24), lanw, 80, boxstyle="round,pad=8,rounding_size=14",
                         facecolor='#23232f', edgecolor=ACCENT, linewidth=2, linestyle=(0, (6, 4)))
    ax.add_patch(lan)
    ax.text(W/2, 78, 'Home LAN / Wi-Fi', ha='center', va='center', fontsize=16, weight='bold', color=ACCENT)
    ax.text(W/2, 50, '192.168.68.0/24', ha='center', va='center', fontsize=11, color=DIM)

    # SSH hop: plain small text in the gap, no box
    ax.text(W/2, 420, 'SSH hop\nPi #1 → Pi #2', ha='center', va='center', fontsize=11,
            color='#55556a', style='italic')

    # Arrows (kept short, clear of boxes)
    arrow(ax, W/2-170, 790, p1x+pw-60, py+ph, '“flash a message”', AMBER, fs=12)
    arrow(ax, W/2+170, 790, p2x+60, py+ph, '“show the fire sim”', AMBER, fs=12)
    # Pi <-> LAN: simple vertical pairs at the panel bottoms, labels staggered
    arrow(ax, p1x+150, py, p1x+150, 108, '', GREEN, fs=12)
    ax.text(p1x+150, 88, 'sensor readings ↓', ha='center', fontsize=11, color=GREEN, style='italic')
    arrow(ax, p1x+300, 104, p1x+300, py, '', GREEN, fs=12)
    ax.text(p1x+300, 116, '↑ dashboard :8000', ha='center', fontsize=11, color=GREEN, style='italic')
    arrow(ax, p2x+pw-300, py, p2x+pw-300, 108, '', GREEN, fs=12)
    ax.text(p2x+pw-300, 88, 'camera frames ↓', ha='center', fontsize=11, color=GREEN, style='italic')
    arrow(ax, p2x+pw-150, 104, p2x+pw-150, py, '', AMBER, fs=12)
    ax.text(p2x+pw-150, 116, '↑ LED commands', ha='center', fontsize=11, color=AMBER, style='italic')

    fig.savefig(f'{OUT}/architecture.png', facecolor=BG)
    plt.close(fig)

# ---------------------------------------------------------------- 2. workflow
def workflow():
    W, H = 1600, 900
    fig, ax = new_fig(W, H)
    ax.text(W/2, H-40, 'The Experiment Loop', ha='center', va='top',
            fontsize=32, weight='bold', color=TXT)
    ax.text(W/2, H-88, 'Muse Gadget: from question to hardware in minutes — no driver spelunking',
            ha='center', va='top', fontsize=16, color=DIM)

    # Circular loop - 5 nodes
    cx, cy, R = W/2, 490, 260
    steps = [
        ('Idea /\nQuestion', '#ff9f43'),
        ('Natural-language\nrequest', AMBER),
        ('Muse builds\n& deploys', GREEN),
        ('Observe on\nhardware', ACCENT),
        ('Iterate', '#c678dd'),
    ]
    n = len(steps)
    pos = []
    for i, (label, col) in enumerate(steps):
        ang = np.pi/2 + i * 2*np.pi/n
        x, y = cx + R*np.cos(ang), cy + R*np.sin(ang)*0.82
        pos.append((x, y))
        b = FancyBboxPatch((x-140, y-52), 280, 104,
                           boxstyle="round,pad=6,rounding_size=18",
                           facecolor=PANEL, edgecolor=col, linewidth=2.5)
        ax.add_patch(b)
        ax.text(x, y+8, label.split('\n')[0], ha='center', va='center', fontsize=17,
                weight='bold', color=col)
        if '\n' in label:
            ax.text(x, y-20, label.split('\n')[1], ha='center', va='center', fontsize=17,
                    weight='bold', color=col)
    # curved arrows between nodes
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i+1) % n]
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', color='#55556a',
                            linewidth=2.5, connectionstyle='arc3,rad=0.28',
                            mutation_scale=20, shrinkA=58, shrinkB=58)
        ax.add_patch(a)
    ax.text(cx, cy, 'minutes,\nnot days', ha='center', va='center', fontsize=20,
            color=TXT, weight='bold', style='italic')

    # Traditional path - greyed out below
    y0 = 130
    ax.text(90, y0+62, 'The old way:', fontsize=17, color='#55556a', style='italic', va='center')
    trad = ['read datasheets', 'write drivers', 'dependency hell', 'debug at 1am', '…maybe works']
    x = 280
    for i, t in enumerate(trad):
        b = FancyBboxPatch((x, y0-28), 200, 56, boxstyle="round,pad=4,rounding_size=12",
                           facecolor='#1c1c26', edgecolor='#3d3d4d', linewidth=1.2)
        ax.add_patch(b)
        ax.text(x+100, y0, t, ha='center', va='center', fontsize=14, color='#6a6a7a')
        if i < len(trad)-1:
            ax.annotate('', xy=(x+205, y0), xytext=(x+232, y0),
                        arrowprops=dict(arrowstyle='->', color='#3d3d4d', lw=1.5))
        x += 232
    ax.plot([60, W-60], [y0-58, y0-58], color='#2c2c38', lw=1)

    fig.savefig(f'{OUT}/workflow.png', facecolor=BG)
    plt.close(fig)

# ---------------------------------------------------------------- 3. fire palette
def fire_palette():
    W, H = 800, 300
    fig, ax = new_fig(W, H)
    ax.text(W/2, H-28, 'Fire simulation palette (heat → color)', ha='center', va='top',
            fontsize=20, weight='bold', color=TXT)

    def heat_rgb(t):
        t = max(0, min(255, int(t)))
        if t < 85:  return (t*3/255, 0, 0)
        if t < 170: return (1.0, (t-85)*3/255, 0)
        return (1.0, 1.0, (t-170)*3/255)

    n = 256
    grad = np.zeros((1, n, 3))
    for i in range(n):
        grad[0, i] = heat_rgb(i)
    ax.imshow(grad, extent=[60, W-60, 110, 175], aspect='auto')

    labels = [(0, '0\ncold'), (64, '64'), (128, '128'), (192, '192'), (255, '255\nwhite-hot')]
    for v, lab in labels:
        x = 60 + (W-120) * v/255
        ax.plot([x, x], [100, 110], color=DIM, lw=1.2)
        ax.text(x, 82, lab, ha='center', va='top', fontsize=13, color=DIM)
    for v, name, col in [(20, 'black', TXT), (70, 'dark red', '#ff6b6b'),
                         (128, 'red-orange', '#ffa94d'), (185, 'yellow', '#ffe066'),
                         (240, 'white', TXT)]:
        x = 60 + (W-120) * v/255
        ax.text(x, 196, name, ha='center', va='bottom', fontsize=13, color=col)

    ax.text(W/2, 30, 'Doom-style algorithm: heat rises, cools, and maps through this ramp',
            ha='center', fontsize=13, color=DIM, style='italic')
    fig.savefig(f'{OUT}/fire-palette.png', facecolor=BG)
    plt.close(fig)

# ---------------------------------------------------------------- 4. rgb concept
def rgb_concept():
    W, H = 1000, 600
    fig, ax = new_fig(W, H)
    ax.text(W/2, H-30, 'RGB Light Meter — concept', ha='center', va='top',
            fontsize=24, weight='bold', color=TXT)

    # Camera icon (left)
    cam = FancyBboxPatch((70, 200), 170, 120, boxstyle="round,pad=6,rounding_size=12",
                         facecolor=PANEL, edgecolor=ACCENT, linewidth=2)
    ax.add_patch(cam)
    ax.add_patch(Circle((155, 260), 32, facecolor='#0d0d14', edgecolor=ACCENT, linewidth=2))
    ax.add_patch(Circle((155, 260), 14, facecolor=ACCENT, alpha=0.35, edgecolor='none'))
    ax.text(155, 215, 'USB camera', ha='center', fontsize=13, color=DIM)
    ax.text(155, 150, 'pi4leddisplay', ha='center', fontsize=13, color=DIM, style='italic')

    # Hand partially covering (simple mitt shape)
    hand = mpatches.Ellipse((150, 360), 120, 70, facecolor='#c9a06a', edgecolor='#8a6a3a', linewidth=1.5, alpha=0.95, zorder=5)
    ax.add_patch(hand)
    for fx in [-30, -10, 10, 30]:
        ax.add_patch(Rectangle((150+fx-9, 375), 18, 55, facecolor='#c9a06a',
                               edgecolor='#8a6a3a', linewidth=1.2, zorder=5))
    ax.text(150, 455, 'hand', ha='center', fontsize=14, color='#c9a06a', weight='bold')

    # Chart (right)
    cx0, cx1, cy0, cy1 = 330, 940, 120, 480
    chart_bg = FancyBboxPatch((cx0, cy0), cx1-cx0, cy1-cy0,
                              boxstyle="round,pad=4,rounding_size=10",
                              facecolor='#101018', edgecolor='#3a3a4d', linewidth=1.2)
    ax.add_patch(chart_bg)
    # axes
    ax.plot([cx0+40, cx0+40], [cy0+30, cy1-20], color='#3a3a4d', lw=1)
    ax.plot([cx0+40, cx1-20], [cy0+30, cy0+30], color='#3a3a4d', lw=1)
    ax.text(cx0+18, cy1-40, '255', fontsize=11, color=DIM, ha='right')
    ax.text(cx0+18, cy0+40, '0', fontsize=11, color=DIM, ha='right')

    xs = np.linspace(0, 1, 200)
    dip = np.exp(-((xs-0.55)/0.09)**2)          # hand dip
    base = 0.62 + 0.05*np.sin(xs*22) + 0.02*np.random.RandomState(7).randn(200)
    for ch, col, amp, off in [('R', '#ff5555', 1.0, 0.02), ('G', '#39d353', 0.92, 0.0), ('B', '#4488ff', 0.85, -0.02)]:
        ys = (base*amp + off) * (1 - 0.75*dip)
        X = cx0+45 + xs*(cx1-cx0-70)
        Y = cy0+35 + ys*(cy1-cy0-70)
        ax.plot(X, Y, color=col, lw=2.4)
    # dip annotation (no bbox — boxstyle renders oversized)
    dx = cx0+45 + 0.55*(cx1-cx0-70)
    ax.annotate('hand covers lens\n→ intensity drops', xy=(dx, cy0+90), xytext=(dx+40, cy0+170),
                fontsize=13, color=AMBER, ha='left',
                arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.8))
    ax.text(cx1-30, cy1-32, 'time →', fontsize=12, color=DIM, ha='right')
    for lab, col, yy in [('R', '#ff5555', 0), ('G', '#39d353', 1), ('B', '#4488ff', 2)]:
        ax.text(cx1-90, cy1-58-yy*24, lab, fontsize=15, weight='bold', color=col)

    # flow arrow camera -> chart
    arrow(ax, 245, 260, cx0-8, 260, 'frames', ACCENT, fs=13)

    fig.savefig(f'{OUT}/rgb-concept.png', facecolor=BG)
    plt.close(fig)

# ---------------------------------------------------------------- 5. sense hat diagram
def sensehat_diagram():
    W, H = 1000, 800
    fig, ax = new_fig(W, H)
    ax.text(W/2, H-24, 'Sense HAT v1.0 — anatomy', ha='center', va='top',
            fontsize=26, weight='bold', color=TXT)
    ax.text(W/2, H-56, 'the Astro Pi add-on board · 8×8 RGB matrix · joystick · 6 sensors',
            ha='center', va='top', fontsize=13, color=DIM)

    # Board — bigger, centered
    bx, by, bw, bh = 330, 60, 400, 590
    board = FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=8,rounding_size=18",
                           facecolor='#1d5c38', edgecolor='#0f3a22', linewidth=3)
    ax.add_patch(board)

    # 8x8 LED grid (upper part of board)
    gs, gap = 32, 6
    grid_w = 8*gs + 7*gap
    gx = bx + (bw-grid_w)/2
    gy_top = by+bh-90
    for r in range(8):
        for c in range(8):
            on = (r + c) % 3 == 0
            col = ['#ff5555', '#ffb020', '#00d4ff'][(r*8+c) % 3] if on else '#0d2818'
            ax.add_patch(Rectangle((gx + c*(gs+gap), gy_top - (r+1)*(gs+gap) + gap), gs, gs,
                                   facecolor=col, edgecolor='#0a1f12', linewidth=1))
    grid_bottom = gy_top - 8*(gs+gap)
    ax.text(bx+bw/2, grid_bottom-18, '8×8 RGB LED matrix', ha='center', va='top',
            fontsize=15, color=TXT, weight='bold')

    # Joystick (lower part of board)
    jx, jy = bx+bw/2, by+95
    ax.add_patch(Circle((jx, jy), 24, facecolor='#2b2b38', edgecolor='#55556a', linewidth=2))
    ax.add_patch(Circle((jx, jy), 11, facecolor='#8a8a99', edgecolor='#55556a', linewidth=1.5))
    for dx, dy, lab in [(0, 38, 'up'), (0, -38, 'down'), (-42, 0, 'left'), (42, 0, 'right')]:
        ax.text(jx+dx, jy+dy, lab, ha='center', va='center', fontsize=10, color=DIM)
    ax.text(jx, by+28, '5-way joystick (click = middle)', ha='center', va='center',
            fontsize=12, color=TXT, weight='bold')

    # Sensor list with leader lines (left side)
    sensors = [
        ('Temperature', '−40…+120 °C', ACCENT),
        ('Humidity', '0…100 %RH', ACCENT),
        ('Pressure', '260…1260 hPa', ACCENT),
        ('Gyroscope', '±245/500/2000 dps', '#c678dd'),
        ('Accelerometer', '±2/4/8/16 g', '#c678dd'),
        ('Magnetometer', '±4/8/12/16 gauss', '#c678dd'),
    ]
    sx = 36
    sy0 = 600
    for i, (name, spec, col) in enumerate(sensors):
        y = sy0 - i*78
        ax.add_patch(Circle((sx+8, y), 6, facecolor=col, edgecolor='none'))
        ax.text(sx+24, y+11, name, fontsize=14, weight='bold', color=TXT, va='center')
        ax.text(sx+24, y-13, spec, fontsize=11, color=DIM, va='center')
        ax.plot([sx+170, bx-8], [y, by+bh-70-i*62], color='#3a3a4d', lw=1.1,
                linestyle=(0, (4, 3)))
    ax.text(sx, sy0+46, 'SENSORS (I²C)', fontsize=13, weight='bold', color=AMBER)

    # Right side notes
    nx = 768
    ax.text(nx, 600, 'WHAT IT DOES', fontsize=13, weight='bold', color=AMBER)
    notes = ['scroll text & symbols', 'pixel art & animation',
             'tilt games (joystick+IMU)', 'log weather data',
             'detect orientation']
    for i, n_ in enumerate(notes):
        ax.text(nx, 562-i*32, '•  ' + n_, fontsize=12, color=TXT, va='center')
    ax.text(nx, 562-5*32-20, 'flown on the ISS\n(Astro Pi program)', fontsize=11,
            color=DIM, style='italic', va='top')

    fig.savefig(f'{OUT}/sensehat-diagram.png', facecolor=BG)
    plt.close(fig)

if __name__ == '__main__':
    architecture();  print('architecture.png ok')
    workflow();      print('workflow.png ok')
    fire_palette();  print('fire-palette.png ok')
    rgb_concept();   print('rgb-concept.png ok')
    sensehat_diagram(); print('sensehat-diagram.png ok')
