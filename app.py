# Streamlit app: Balle libre avec gravité + anneaux fins
# ---------------------------------------------------------------
# Run: pip install streamlit
#      streamlit run app.py
#
# Jeu: une balle se déplace librement avec gravité (comme sur Terre),
# rebondit sur les bords, et interagit avec plusieurs anneaux fins
# concentriques tournants. Chaque anneau a un trou large; si la balle
# passe par le trou, l'anneau est détruit avec un effet de chute.

import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Balle libre + anneaux fins — Streamlit", layout="wide")
st.title("Balle gravité + anneaux fins — demo")

# Sidebar controls
st.sidebar.header("Contrôles")
num_rings = st.sidebar.slider("Nombre d'anneaux", 1, 8, 5)
hole_width_deg = st.sidebar.slider("Largeur du trou (degrés)", 45, 120, 75)
max_rot_speed = st.sidebar.slider("Vitesse max rotation (deg/s)", 10, 360, 120)
ball_init_speed = st.sidebar.slider("Vitesse initiale de la balle", 1.0, 12.0, 4.0)
gravity = st.sidebar.slider("Gravité (px/s²)", 50, 500, 150)
bounce_damping = st.sidebar.slider("Rebond (%)", 80, 100, 95)
autoplay = st.sidebar.checkbox("Autoplay", value=True)
canvas_size = st.sidebar.selectbox("Taille du canvas", [400, 600, 800], index=1)

# Colors
bg_color = st.sidebar.color_picker("Couleur de fond", "#0f0f12")
ring_color1 = st.sidebar.color_picker("Couleur anneaux 1", "#ffd966")
ring_color2 = st.sidebar.color_picker("Couleur anneaux 2", "#ff6b6b")

# HTML + JS
html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  html,body {{ margin:0; height:100%; background:{bg_color}; }}
  #container {{ display:flex; align-items:center; justify-content:center; height:100%; }}
  canvas {{ border-radius:8px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); }}
  .overlay {{ position:absolute; top:12px; left:12px; color: rgba(255,255,255,0.9); font-family: sans-serif; }}
</style>
</head>
<body>
<div id="container"><canvas id="c" width="{canvas_size}" height="{canvas_size}"></canvas></div>
<div class="overlay">Clic: pousse la balle • dblclick ou 'r': reset</div>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
const cx = W/2, cy = H/2;

// Parameters
const NUM_RINGS = {num_rings};
const HOLE_WIDTH_DEG = {hole_width_deg};
const MAX_ROT_SPEED = {max_rot_speed};
const BALL_INIT_SPEED = {ball_init_speed};
const GRAVITY = {gravity};
const BOUNCE_DAMPING = {bounce_damping}/100;
let autoplay = {str(autoplay).lower()};

const RING_COLOR_A = '{ring_color1}';
const RING_COLOR_B = '{ring_color2}';

const ringThickness = Math.min(W,H) * 0.03; // fine rings

// Ball state
let ball = {{ x: cx, y: cy, vx: 0, vy: 0, r: Math.max(5, Math.round(W/80)) }};
function randomizeBall() {{
  const a = Math.random()*Math.PI*2;
  ball.vx = Math.cos(a) * BALL_INIT_SPEED;
  ball.vy = Math.sin(a) * BALL_INIT_SPEED;
  ball.x = cx + (Math.random()-0.5) * 20;
  ball.y = cy + (Math.random()-0.5) * 20;
}}

// Rings
let rings = [];
function initRings() {{
  rings = [];
  const base = Math.min(W,H) * 0.18;
  for (let i=0;i<NUM_RINGS;i++) {{
    const innerR = base + i * (ringThickness + 6);
    const outerR = innerR + ringThickness;
    const speed = (20 + Math.random() * (MAX_ROT_SPEED-20));
    const holeCenter = Math.random() * 360;
    rings.push({{
      innerR: innerR,
      outerR: outerR,
      rot: 0,
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

function drawRings() {{
  rings.forEach(ring => {{
    if (ring.destroyed) return;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(ring.rot * Math.PI/180);
    const midR = (ring.innerR + ring.outerR)/2;
    const lw = ring.outerR - ring.innerR;
    ctx.beginPath();
    ctx.arc(0,0, midR, 0, Math.PI*2);
    ctx.lineWidth = lw;
    ctx.strokeStyle = 'rgba(255,255,255,0.03)';
    ctx.stroke();
    const gapRad = ring.holeWidth * Math.PI/180;
    const half = gapRad/2;
    const start = (ring.holeCenter * Math.PI/180) - half;
    const end = (ring.holeCenter * Math.PI/180) + half;
    ctx.beginPath();
    ctx.arc(0,0, midR, end, start + Math.PI*2, false);
    ctx.lineWidth = lw;
    const grad = ctx.createLinearGradient(-midR,-midR,midR,midR);
    grad.addColorStop(0, RING_COLOR_A);
    grad.addColorStop(1, RING_COLOR_B);
    ctx.strokeStyle = grad;
    ctx.lineCap = 'round';
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
      ctx.globalAlpha = Math.max(0,1-(p.life/2000));
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.restore();
    }});
  }});
}}

function update(dt) {{
  if (!autoplay) return;

  // Update rings rotation
  rings.forEach(ring => {{ if(!ring.destroyed) ring.rot += ring.speed * dt/1000; }});

  // Apply gravity
  ball.vy += GRAVITY * dt/1000;

  // Move ball
  ball.x += ball.vx * dt/16.0;
  ball.y += ball.vy * dt/16.0;

  // Bounce on canvas edges
  if (ball.x - ball.r < 0) {{ ball.x = ball.r; ball.vx *= -BOUNCE_DAMPING; }}
  if (ball.x + ball.r > W) {{ ball.x = W-ball.r; ball.vx *= -BOUNCE_DAMPING; }}
  if (ball.y - ball.r < 0) {{ ball.y = ball.r; ball.vy *= -BOUNCE_DAMPING; }}
  if (ball.y + ball.r > H) {{ ball.y = H-ball.r; ball.vy *= -BOUNCE_DAMPING; }}

  // Check collision with rings for destruction
  rings.forEach(ring => {{
    if(ring.destroyed) return;
    const dx = ball.x - cx;
    const dy = ball.y - cy;
    const br = Math.sqrt(dx*dx + dy*dy);
    if(br + ball.r >= ring.innerR && br - ball.r <= ring.outerR) {{
      let ang = Math.atan2(dy, dx) * 180/Math.PI;
      if(ang<0) ang+=360;
      let localAng = ang - ring.rot;
      while
