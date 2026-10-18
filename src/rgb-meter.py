#!/usr/bin/env python3
"""Live RGB light meter: Flask dashboard showing per-channel average
intensity from the USB camera feed as updating line charts.

Open http://<pi-ip>:8000 — cover the camera with your hand and watch
the traces drop.
"""
import cv2, time, threading
from collections import deque
from flask import Flask, jsonify

app = Flask(__name__)
BUF = 120
hist_r = deque(maxlen=BUF)
hist_g = deque(maxlen=BUF)
hist_b = deque(maxlen=BUF)
running = True

def capture_loop():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    while running:
        ok, frame = cap.read()
        if ok:
            b, g, r = cv2.mean(frame)[:3]
            hist_r.append(round(r, 1))
            hist_g.append(round(g, 1))
            hist_b.append(round(b, 1))
        time.sleep(0.2)
    cap.release()

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RGB Light Meter</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>body{font-family:sans-serif;max-width:800px;margin:20px auto;
padding:0 15px;background:#111;color:#eee}
.vals{display:flex;gap:20px;font-size:1.4em;margin:10px 0}
.vals span{padding:5px 12px;border-radius:8px}</style></head><body>
<h2>Live Camera RGB Intensity</h2>
<div class="vals">
<span id="vr" style="background:#3a1010">R: --</span>
<span id="vg" style="background:#103a10">G: --</span>
<span id="vb" style="background:#10103a">B: --</span>
</div>
<canvas id="c" height="120"></canvas>
<script>
const ctx = document.getElementById('c');
const chart = new Chart(ctx, {type:'line',
data:{labels:[],datasets:[
 {label:'R',data:[],borderColor:'#ff4444',pointRadius:0,tension:0.2},
 {label:'G',data:[],borderColor:'#44ff44',pointRadius:0,tension:0.2},
 {label:'B',data:[],borderColor:'#4488ff',pointRadius:0,tension:0.2}]},
options:{animation:false,scales:{y:{min:0,max:255}},
plugins:{legend:{labels:{color:'#eee'}}}}});
async function tick(){
 const d = await (await fetch('/data')).json();
 chart.data.labels = d.r.map((_,i)=>i);
 chart.data.datasets[0].data = d.r;
 chart.data.datasets[1].data = d.g;
 chart.data.datasets[2].data = d.b;
 chart.update();
 const n = d.r.length-1;
 if(n>=0){vr.textContent='R: '+d.r[n];
          vg.textContent='G: '+d.g[n];
          vb.textContent='B: '+d.b[n];}
}
setInterval(tick, 500); tick();
</script></body></html>"""

@app.route('/')
def index():
    return PAGE

@app.route('/data')
def data():
    return jsonify(r=list(hist_r), g=list(hist_g), b=list(hist_b))

if __name__ == '__main__':
    t = threading.Thread(target=capture_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8000)
