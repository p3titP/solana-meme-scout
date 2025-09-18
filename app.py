# Streamlit app: Multi-ring bouncing ball (concentric rings with holes)
# ---------------------------------------------------------------
# Run: pip install streamlit
#      streamlit run app.py
#
# Jeu: une seule boule se balade et rebondit ; plusieurs cercles concentriques
# tournent autour d'elle (même sens, vitesses différentes). Chaque cercle a
# un trou large et aléatoire ; quand la boule passe par le trou d'un cercle,
# ce cercle est supprimé avec un effet visuel de chute.

import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Multi-ring Bounce — Streamlit", layout="wide")
st.title("Boule + anneaux concentriques — demo")

# Sidebar controls
st.sidebar.header("Contrôles")
num_rings = st.sidebar.slider("Nombre d'anneaux", 1, 8, 5)
hole_width_deg = st.sidebar.slider("Largeur du trou (degrés)", 30, 120, 75)
max_rot_speed = st.sidebar.slider("Vitesse max rotation (deg/s)", 10, 360, 120)
ball_init_speed = st.sidebar.slider("Vitesse initiale de la balle", 1.0, 12.0, 4.0)
autoplay = st.sidebar.checkbox("Autoplay", value=True)
canvas_size = st.sidebar.selectbox("Taille du canvas", [400, 600, 800], index=1)

# Other cosmetic options
bg_color = st.sidebar.color_picker("Couleur de fond", "#0f0f12")
ring_color1 = st.sidebar.color_picker("Couleur anneaux 1", "#ffd966")
ring_color2 = st.sidebar.color_picker("Couleur anneaux 2", "#ff6b6b")

# Build HTML + JS
# NOTE: in this Python f-string we must escape any literal curly braces intended
# for the JavaScript by doubling them ({{ and }}). Python placeholders remain
# single-braced so they are interpolated.
html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  html,body {{ margin:0; height:100%; background:{bg_color}; color:#eee; }}
  #container {{ display:flex; align-items:center; justify-content:center; height:100%; }}
  canvas {{ border-radius:8px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); }}
  .overlay {{ position: absolute; top:12px; left:12px; color: rgba(255,255,255,0.9); font-family: sans-serif; }}
</style>
</head>
<body>
<div id="container"><canvas id="c" width="{canvas_size}" height="{canvas_size}"></canvas></div>
<div class="overlay">Appuie: clic pour pousser la balle • dblclick pour reset</div>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
const cx = W/2, cy = H/2;

// Parameters injected from Streamlit
const NUM_RINGS = {num_rings};
const HOLE_WIDTH_DEG = {hole_width_deg};
const MAX_ROT_SPEED = {max_rot_speed}; // deg/s
let ballInitSpeed = {ball_init_speed};
let autoplay = {str(autoplay).lower()};

// Ring colors
const RING_COLOR_A = '{ring_color1}';
const RING_COLOR_B = '{ring_color2}';

// Geometry: create rings concentric from inner to outer
const minOuter = Math.min(W,H) * 0.42; // outermost radius baseline
const ringThickness = Math.min(W,H) * 0.08; // thickness of each ring

// Ball state — random initial direction and position near center
let ball = {{ x: cx, y: cy, vx: 0, vy: 0, r: Math.max(5, Math.round(W/80)) }};
function randomizeBall() {{
  const a = Math.random()*Math.PI*2;
  ball.vx = Math.cos(a) * ballInitSpeed;
  ball.vy = Math.sin(a) * ballInitSpeed;
  // place a bit off-center so it can move
  ball.x = cx + (Math.random()-0.5) * 10;
  ball.y = cy + (Math.random()-0.5) * 10;
}}

// Rings array: from inner (index 0) to outer
let rings = [];
function initRings() {{
  rings = [];
  // inner base radius for first ring
  const base = Math.min(W,H) * 0.18;
  for (let i=0;i<NUM_RINGS;i++) {{
    const innerR = base + i * (ringThickness + 6);
    const outerR = innerR + ringThickness;
    // rotation speed: same direction (positive) but random magnitude
    const speed = (20 + Math.random() * (MAX_ROT_SPEED-20)); // deg/s
    // random hole center angle in degrees
    const holeCenter = Math.random() * 360;
    rings.push({{
      innerR: innerR,
      outerR: outerR,
      rot: 0, // current rotation angle in degrees
      speed: speed,
      holeCenter: holeCenter,
      holeWidth: HOLE_WIDTH_DEG,
      destroyed: false,
      fallingPieces: []
    }});
  }}
}}

initRings();
randomizeBall();

// Draw functions
function drawRings() {{
  rings.forEach((ring, idx) => {{
    if (ring.destroyed) return;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(ring.rot * Math.PI/180);
    const midR = (ring.innerR + ring.outerR)/2;
    const lw = ring.outerR - ring.innerR;

    // draw full ring as light shadow first
    ctx.beginPath();
    ctx.arc(0,0, midR, 0, Math.PI*2);
    ctx.lineWidth = lw;
    ctx.strokeStyle = 'rgba(255,255,255,0.03)';
    ctx.stroke();

    // determine gap arc (hole)
    const gapRad = ring.holeWidth * Math.PI/180;
    const half = gapRad/2;
    const start = (ring.holeCenter * Math.PI/180) - half;
    const end = (ring.holeCenter * Math.PI/180) + half;

    // draw left arc (end -> start+2PI)
    ctx.beginPath();
    ctx.arc(0,0, midR, end, start + Math.PI*2, false);
    ctx.lineWidth = lw;
    // gradient for visual
    const grad = ctx.createLinearGradient(-midR, -midR, midR, midR);
    grad.addColorStop(0, RING_COLOR_A);
    grad.addColorStop(1, RING_COLOR_B);
    ctx.strokeStyle = grad;
    ctx.lineCap = 'round';
    ctx.stroke();

    // subtle inner rim
    ctx.beginPath();
    ctx.arc(0,0, ring.innerR + 2, end, start + Math.PI*2, false);
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.stroke();

    ctx.restore();
  }});
}}

function drawBall() {{
  ctx.beginPath();
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = '#ddd';
  ctx.shadowBlur = 10;
  ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
  ctx.fill();
  ctx.shadowBlur = 0;
}}

function drawFallingPieces() {{
  rings.forEach(ring => {{
    ring.fallingPieces.forEach(p => {{
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0, 1 - (p.life/2000));
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.restore();
    }});
  }});
}}

// Update physics and state
function update(dt) {{
  if (!autoplay) return;

  // update ring rotations
  rings.forEach(ring => {{
    if (ring.destroyed) return;
    ring.rot += ring.speed * dt/1000.0; // degrees per ms->s
    ring.rot %= 360;
  }});

  // move ball
  ball.x += ball.vx * dt/16.0;
  ball.y += ball.vy * dt/16.0;

  // simple wall bounce inside innermost ring's inner radius
  const arenaR = rings.length>0 ? rings[0].innerR - 6 : Math.min(W,H)/4;
  // keep ball near center by bouncing on a virtual circle (arena)
  const dx = ball.x - cx;
  const dy = ball.y - cy;
  const dist = Math.sqrt(dx*dx + dy*dy);
  if (dist + ball.r > arenaR) {{
    // reflect velocity about radial normal
    const nx = dx/dist;
    const ny = dy/dist;
    const vdotn = ball.vx*nx + ball.vy*ny;
    ball.vx = ball.vx - 2*vdotn*nx;
    ball.vy = ball.vy - 2*vdotn*ny;
    // push inwards
    ball.x = cx + nx*(arenaR - ball.r - 1);
    ball.y = cy + ny*(arenaR - ball.r - 1);
  }}

  // friction / damping to keep speeds stable
  ball.vx *= 0.999;
  ball.vy *= 0.999;

  // Check collisions with rings: if ball radial distance intersects a ring and
  // its angular position (in ring's rotated frame) is within the hole, then
  // destroy ring.
  rings.forEach(ring => {{
    if (ring.destroyed) return;
    const bx = ball.x - cx;
    const by = ball.y - cy;
    const br = Math.sqrt(bx*bx + by*by);
    if (br + ball.r >= ring.innerR && br - ball.r <= ring.outerR) {{
      // compute ball angle in degrees
      let ang = Math.atan2(ball.y - cy, ball.x - cx) * 180/Math.PI; // -180..180
      if (ang < 0) ang += 360;
      // bring into ring's rotating frame by subtracting ring.rot
      let localAng = ang - ring.rot;
      while (localAng < 0) localAng += 360;
      while (localAng >= 360) localAng -= 360;
      const halfHole = ring.holeWidth/2;
      const holeStart = (ring.holeCenter - halfHole + 360) % 360;
      const holeEnd = (ring.holeCenter + halfHole + 360) % 360;

      let inHole = false;
      if (holeStart <= holeEnd) {{
        if (localAng >= holeStart && localAng <= holeEnd) inHole = true;
      }} else {{
        // hole wraps around 360
        if (localAng >= holeStart || localAng <= holeEnd) inHole = true;
      }}

      if (inHole) {{
        // Destroy ring: mark destroyed and spawn falling pieces
        ring.destroyed = true;
        const seg = 12;
        for (let i=0;i<seg;i++) {{
          const theta = (ring.holeCenter + (Math.random()-0.5)*ring.holeWidth) * Math.PI/180;
          const midR = (ring.innerR + ring.outerR)/2;
          const px = Math.cos(theta) * midR;
          const py = Math.sin(theta) * midR;
          const w = (ring.outerR - ring.innerR) * (0.9 + Math.random()*0.8);
          const h = w * 0.35;
          ring.fallingPieces.push({{
            x: px + (Math.random()-0.5)*10,
            y: py + (Math.random()-0.5)*10,
            w: w,
            h: h,
            vx: (Math.random()-0.5)*80,
            vy: 40 + Math.random()*120,
            ax: 0,
            ay: 300,
            rot: Math.random()*Math.PI*2,
            vrot: (Math.random()-0.5)*4,
            life: 0,
            color: 'rgba(' + (200 + Math.floor(Math.random()*55)) + ', ' + (120 + Math.floor(Math.random()*80)) + ', ' + (80 + Math.floor(Math.random()*120)) + ', 1)'
          }});
        }}
      }}
    }}
  }});

  // update falling pieces motion
  rings.forEach(ring => {{
    ring.fallingPieces.forEach(p => {{
      p.vx += p.ax * dt/1000;
      p.vy += p.ay * dt/1000;
      p.x += p.vx * dt/1000;
      p.y += p.vy * dt/1000;
      p.rot += p.vrot * dt/1000;
      p.life += dt;
    }});
    // optional: trim old pieces
    ring.fallingPieces = ring.fallingPieces.filter(p => p.life < 3000);
  }});
}}

// Render loop
let last = performance.now();
function loop(now) {{
  const dt = now - last;
  last = now;
  update(dt);

  // clear
  ctx.clearRect(0,0,W,H);

  // background vignette
  const g = ctx.createRadialGradient(cx, cy, Math.min(W,H)*0.05, cx, cy, Math.max(W,H));
  g.addColorStop(0, 'rgba(255,255,255,0.02)');
  g.addColorStop(1, 'rgba(0,0,0,0.6)');
  ctx.fillStyle = g;
  ctx.fillRect(0,0,W,H);

  drawRings();
  drawFallingPieces();
  drawBall();

  requestAnimationFrame(loop);
}}

requestAnimationFrame(loop);

// Interactions
canvas.addEventListener('click', (e) => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  // nudge ball toward click
  ball.vx += (mx - ball.x) * 0.03;
  ball.vy += (my - ball.y) * 0.03;
}});

canvas.addEventListener('dblclick', (e) => {{
  // reset everything
  initRings();
  randomizeBall();
}});

// expose simple debug reset via keyboard 'r'
window.addEventListener('keydown', (e) => {{
  if (e.key === 'r') {{ initRings(); randomizeBall(); }}
}});

</script>
</body>
</html>
"""

# Streamlit display
import streamlit.components.v1 as components
components.html(html, height=canvas_size+20, scrolling=False)

st.markdown(dedent('''
**Instructions**
- Clique pour pousser la balle.
- Double-clique pour réinitialiser les anneaux et la balle.
- Appuie sur `r` pour réinitialiser aussi.

Paramètres visibles dans la barre latérale : nombre d'anneaux, largeur du trou,
vitesses, etc.
'''))

# Minimal smoke tests when running as script (won't run under Streamlit launch)
if __name__ == "__main__":
    assert '<canvas' in html, "HTML should contain a canvas element"
    assert 'NUM_RINGS' in html, "NUM_RINGS must be injected"
    assert 'HOLE_WIDTH_DEG' in html, "HOLE_WIDTH_DEG must be injected"
    assert 'initRings' in html, "initRings function must be present"
    assert 'randomizeBall' in html, "randomizeBall must be present"
    print('Smoke tests passed: HTML generated OK.')
