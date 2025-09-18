# Streamlit app: TikTok-style bouncing ball inside a rotating ring
# ---------------------------------------------------------------
# Run: pip install streamlit
#      streamlit run app.py
#
# This single-file Streamlit app embeds an HTML/JS animation using
# st.components.v1.html. The JS implements:
# - a rotating ring (an annulus) composed of drawable segments
# - a small ball that moves and bounces on the ring
# - a rotating gap/hole in the ring
# - when the ball passes through the hole, the ring "breaks" and
#   explodes into fragments
#
# Notes about f-strings & curly braces:
# This file uses a Python f-string to build a large HTML+JS string. Any
# curly braces intended for the JavaScript must be escaped by doubling
# them ({{ and }}). Python placeholders that should be interpolated
# (like {canvas_size}) remain single-braced.

import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="TikTok Bounce — Streamlit", layout="wide")
st.title("TikTok-style bouncing ball — Streamlit demo")

# Sidebar controls
st.sidebar.header("Controls")
rotation_speed = st.sidebar.slider("Vitesse de rotation (deg/s)", 0.0, 360.0, 60.0)
gap_degrees = st.sidebar.slider("Largeur du trou (degrés)", 5, 120, 24)
ball_speed = st.sidebar.slider("Vitesse initiale de la balle", 0.5, 10.0, 3.0)
autoplay = st.sidebar.checkbox("Autoplay", value=True)
canvas_size = st.sidebar.selectbox("Taille du canvas", [400, 600, 800], index=1)

# Build HTML + JS
html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  html,body {{ margin:0; height:100%; background:#111; color:#eee; }}
  #container {{ display:flex; align-items:center; justify-content:center; height:100%; }}
  canvas {{ background: radial-gradient(circle at 50% 20%, #222 0%, #101010 60%); border-radius:8px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); }}
</style>
</head>
<body>
<div id="container"><canvas id="c" width="{canvas_size}" height="{canvas_size}"></canvas></div>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
const cx = W/2, cy = H/2;

// Configurable params passed from Streamlit
let rotationSpeed = {rotation_speed}; // degrees per second
let gapWidthDeg = {gap_degrees};
let initialBallSpeed = {ball_speed};
let autoplay = {str(autoplay).lower()};

// Ring geometry
const outerR = Math.min(W,H)*0.42;
const innerR = outerR - Math.min(W,H)*0.12;

// Ball state
let ball = {{ x: cx, y: cy - (innerR - 6), vx: 0.0, vy: 0.0, r: Math.max(6, Math.min(12, Math.round(W/60))) }};
let speedScale = initialBallSpeed;

// Ring state
let rot = 0; // degrees
let destroyed = false;
let fragments = []; // for explosion

// Initialize ball with a random velocity
function resetBall() {{
  const a = (Math.random()*Math.PI*2);
  ball.vx = Math.cos(a)*speedScale;
  ball.vy = Math.sin(a)*speedScale;
  ball.x = cx;
  ball.y = cy - (innerR - 10);
  destroyed = false;
  fragments = [];
}}

resetBall();

function drawRing() {{
  // Draw ring as two arcs: the intact segments and the hole
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(rot * Math.PI/180);

  // draw base ring shadow
  ctx.beginPath();
  ctx.arc(0,0, (innerR+outerR)/2, 0, Math.PI*2);
  ctx.lineWidth = outerR-innerR;
  ctx.strokeStyle = 'rgba(180,180,180,0.03)';
  ctx.stroke();

  if (!destroyed) {{
    const gap = gapWidthDeg * Math.PI/180;
    const halfGap = gap/2;
    // We'll draw ring as two arcs: from gap_end to gap_start
    const start = halfGap;
    const end = Math.PI*2 - halfGap;

    ctx.beginPath();
    ctx.arc(0,0, (innerR+outerR)/2, end, start + Math.PI*2, false);
    ctx.lineWidth = outerR-innerR;
    // gradient stroke
    const grad = ctx.createLinearGradient(-outerR, -outerR, outerR, outerR);
    grad.addColorStop(0, '#ffd966');
    grad.addColorStop(1, '#ff6b6b');
    ctx.strokeStyle = grad;
    ctx.shadowColor = 'rgba(0,0,0,0.6)';
    ctx.shadowBlur = 12;
    ctx.lineCap = 'round';
    ctx.stroke();

    // subtle inner rim
    ctx.beginPath();
    ctx.arc(0,0, innerR+2, end, start + Math.PI*2, false);
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.stroke();
  }}

  ctx.restore();
}}

function drawBall() {{
  ctx.beginPath();
  ctx.fillStyle = '#ffffff';
  // soft glow
  ctx.shadowColor = '#ffb3b3';
  ctx.shadowBlur = 12;
  ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
  ctx.fill();
  ctx.shadowBlur = 0;
}}

function drawFragments() {{
  if (fragments.length === 0) return;
  fragments.forEach(f => {{
    ctx.beginPath();
    ctx.fillStyle = f.color;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(f.rot);
    ctx.rect(f.x, f.y, f.w, f.h);
    ctx.fill();
    ctx.restore();
  }});
}}

function update(dt) {{
  if (!autoplay) return;
  // rotation
  rot += rotationSpeed * dt/1000.0; // degrees
  rot %= 360;

  if (destroyed) {{
    // update fragments
    fragments.forEach(f => {{
      f.vx += f.ax*dt/1000;
      f.vy += f.ay*dt/1000;
      f.x += f.vx*dt/1000;
      f.y += f.vy*dt/1000;
      f.rot += f.vrot*dt/1000;
    }});
    return;
  }}

  // move ball
  ball.x += ball.vx * dt/16.0;
  ball.y += ball.vy * dt/16.0;

  // gravity-like pull toward center (subtle)
  const dx = cx - ball.x;
  const dy = cy - ball.y;
  const dist = Math.sqrt(dx*dx + dy*dy);

  // Collision with outer/inner ring walls depends on rotated ring
  // Compute ball polar coords relative to center and subtract rotation
  let ang = Math.atan2(ball.y - cy, ball.x - cx); // radians
  let angDeg = ang * 180/Math.PI;
  // normalise
  // compute angle in ring's rotating frame
  let ringAng = angDeg - rot;
  while (ringAng <= -180) ringAng += 360;
  while (ringAng > 180) ringAng -= 360;

  // distance to center
  if (dist + ball.r >= innerR && dist - ball.r <= outerR) {{
    // ball intersects the annulus region; check gap
    const halfGap = gapWidthDeg/2;
    if (ringAng > -halfGap && ringAng < halfGap) {{
      // It's within the gap -> ball escapes through the hole
      // Trigger destroy
      destroyAtAngle(ang + rot*Math.PI/180);
      return;
    }} else {{
      // Reflect off ring normal
      // radial normal vector
      const nx = dx/dist;
      const ny = dy/dist;
      // velocity vector
      const vdotn = ball.vx * nx + ball.vy * ny;
      // reflect
      ball.vx = ball.vx - 2*vdotn*nx;
      ball.vy = ball.vy - 2*vdotn*ny;
      // damping
      ball.vx *= 0.98;
      ball.vy *= 0.98;
      // push ball slightly to avoid sticking
      const overlap = Math.max(0, (innerR + ball.r) - dist);
      if (overlap > 0) {{
        ball.x -= nx * (overlap + 0.5);
        ball.y -= ny * (overlap + 0.5);
      }}
    }}
  }} else {{
    // keep ball inside by small central force
    ball.vx += dx/dist * 0.05;
    ball.vy += dy/dist * 0.05;
    // cap speeds
    const sp = Math.sqrt(ball.vx*ball.vx + ball.vy*ball.vy);
    if (sp > 60) {{ ball.vx *= 60/sp; ball.vy *= 60/sp; }}
  }}
}}

function destroyAtAngle(angleRad) {{
  destroyed = true;
  // create fragments along ring arc near the angle
  const segCount = 18;
  for (let i=0;i<segCount;i++) {{
    const theta = angleRad + (Math.random()-0.5) * (gapWidthDeg*Math.PI/180*2);
    const rmid = (innerR+outerR)/2;
    const fx = Math.cos(theta) * rmid;
    const fy = Math.sin(theta) * rmid;
    const size = (outerR-innerR) * (0.2 + Math.random()*0.6);
    fragments.push({{
      x: fx, y: fy, w: size*0.9, h: size*0.4,
      vx: (Math.cos(theta) * (50+Math.random()*150)),
      vy: (Math.sin(theta) * (50+Math.random()*150)),
      ax: 0, ay: 200, // gravity
      rot: Math.random()*Math.PI*2,
      vrot: (Math.random()-0.5)*5,
      color: 'rgba(' + (200 + Math.floor(Math.random()*55)) + ', ' + (120 + Math.floor(Math.random()*80)) + ', ' + (80 + Math.floor(Math.random()*120)) + ', 1)'
    }});
  }}

  // give the ball an outward impulse
  const dirx = Math.cos(angleRad);
  const diry = Math.sin(angleRad);
  ball.vx = dirx * 120;
  ball.vy = diry * 120;
}}

let last = performance.now();
function loop(now) {{
  const dt = now - last;
  last = now;
  update(dt);
  render();
  requestAnimationFrame(loop);
}}

function render() {{
  ctx.clearRect(0,0,W,H);
  // soft vignette
  const g = ctx.createRadialGradient(cx, cy, Math.min(W,H)*0.1, cx, cy, Math.max(W,H));
  g.addColorStop(0, 'rgba(255,255,255,0.02)');
  g.addColorStop(1, 'rgba(0,0,0,0.6)');
  ctx.fillStyle = g;
  ctx.fillRect(0,0,W,H);

  drawRing();
  drawFragments();
  drawBall();
}}

requestAnimationFrame(loop);

// Click to nudge / reset
canvas.addEventListener('click', (e) => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  // give ball a tiny push towards click
  ball.vx += (mx - ball.x) * 0.05;
  ball.vy += (my - ball.y) * 0.05;
}});

// Double click to reset entire scene
canvas.addEventListener('dblclick', (e) => {{ resetBall(); destroyed=false; fragments=[]; }});

</script>
</body>
</html>
"""

# Streamlit display
import streamlit.components.v1 as components
components.html(html, height=canvas_size+20, scrolling=False)

st.markdown(dedent('''
**Instructions rapides**
- Cliquez pour pousser la balle, double-cliquez pour réinitialiser.
- Ajustez la vitesse de rotation, la taille du trou et la vitesse de la balle dans la barre latérale.

**À propos**: ce fichier est pensé pour être le point de départ. Si tu veux, je peux aussi:
- Te fournir un `README.md` complet prêt à déposer sur GitHub.
- Ajouter un fichier `requirements.txt` et des tests minimaux.
'''))

# Minimal smoke tests (run when executing the file directly, not when Streamlit runs it)
if __name__ == "__main__":
    # Basic checks to help catching template/braces issues
    assert '<canvas' in html, "HTML should contain a canvas element"
    assert 'rotationSpeed' in html, "HTML should contain rotationSpeed placeholder"
    assert 'autoplay' in html, "HTML should contain autoplay setting"
    assert 'rgba(' in html, "Fragment color should be generated using rgba"
    assert '${' not in html, "There should be no JS template literal '${' left unescaped in the HTML"
    print('Smoke tests passed: HTML generated OK.')
