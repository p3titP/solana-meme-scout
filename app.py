import streamlit as st
import random
import string
import os

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Entraînement Lettres, Logique & Maths",
    page_icon="🔠",
    layout="centered"
)

# ---------------------------
# STYLES
# ---------------------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; max-width: 980px; }
.letter-big { font-size: 38px; font-weight: 800; text-align: center; letter-spacing: .20rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
.cell { display:flex; align-items:center; justify-content:center; height:64px; }
.option-btn { width:100%; height:56px; font-size:18px; font-weight:700; }
.caption { color: #6b7280; text-align:center; margin-bottom: .25rem; }
.section { margin-top: 18px; margin-bottom: 18px; }

/* ---- STYLE IMAGE ---- */
.image-box {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    text-align: center;
}
.image-box img {
    border-radius: 12px;
    max-width: 100%;
    height: auto;
}
.image-caption {
    color: #6b7280;
    font-size: 14px;
    margin-top: .5rem;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITRE
# ---------------------------
st.title("🔠 Entraînement Lettres, Logique & Maths (style TAJ)")

# ---------------------------
# IMAGE D’ACCUEIL
# ---------------------------
img_path = "Gemini_Generated_Image_exwfzoexwfzoexwf.png"
if os.path.exists(img_path):
    with st.container():
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.image(img_path, use_container_width=True)
        st.markdown('<div class="image-caption">Exemple d’un intérieur moderne et lumineux</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ Image introuvable : ajoute le fichier dans le même dossier que app.py")

# ---------------------------
# OUTIL : feedback commun
# ---------------------------
def feedback(condition, msg_ok, msg_fail):
    if condition:
        st.success(msg_ok)
    else:
        st.error(msg_fail)

# =========================================
# 1) EXERCICE : position dans l'alphabet
# =========================================
st.header("1️⃣ Jeu de l'alphabet")

if "lettre" not in st.session_state:
    st.session_state.lettre = random.choice(string.ascii_uppercase)

st.subheader(f"Quelle est la position de la lettre : **{st.session_state.lettre}** ?")
reponse_alpha = st.number_input("👉 Entrez le numéro :", min_value=1, max_value=26, step=1, key="alpha_input")

cols_alpha = st.columns(2)
with cols_alpha[0]:
    if st.button("Vérifier", key="verif_alpha"):
        correct = string.ascii_uppercase.index(st.session_state.lettre) + 1
        feedback(
            reponse_alpha == correct,
            f"✅ Bravo ! {st.session_state.lettre} est bien la {correct}ᵉ lettre.",
            f"❌ Mauvaise réponse. La bonne réponse était {correct}."
        )
with cols_alpha[1]:
    if st.button("Nouvelle lettre", key="new_alpha"):
        st.session_state.lettre = random.choice(string.ascii_uppercase)
        st.rerun()

st.divider()

# =========================================
# 2) EXERCICES : Suites croisées
# =========================================
st.header("2️⃣ Suites croisées (verticale + horizontale) — trouve l'intersection")

cross_exos = [
    {"vertical": ["3", "4", "5", "6", "7"], "horizontal": ["1", "3", "5", "7", "9"], "options": ["1", "3", "5", "7", "9"], "reponse": "5", "explication": "Verticalement : +1. Horizontalement : +2. Centre commun = 5."},
    {"vertical": ["C", "E", "G", "I", "K"], "horizontal": ["E", "F", "G", "H", "I"], "options": ["C", "E", "G", "H", "I"], "reponse": "G", "explication": "Verticalement : +2 lettres. Horizontalement : +1. Centre = G."},
    {"vertical": ["6", "9", "12", "15", "18"], "horizontal": ["2", "7", "12", "17", "22"], "options": ["2", "7", "12", "17", "22"], "reponse": "12", "explication": "Verticalement : +3. Horizontalement : +5. Centre = 12."},
    {"vertical": ["E", "I", "M", "Q", "U"], "horizontal": ["G", "J", "M", "P", "S"], "options": ["E", "G", "M", "P", "S"], "reponse": "M", "explication": "Verticalement : +4 lettres. Horizontalement : +3. Centre = M."}
]

if "cross_idx" not in st.session_state:
    st.session_state.cross_idx = 0
if "cross_round" not in st.session_state:
    st.session_state.cross_round = 0
if "cross_choice" not in st.session_state:
    st.session_state.cross_choice = None

cross = cross_exos[st.session_state.cross_idx]
vert, horiz, opts, correct = cross["vertical"], cross["horizontal"], cross["options"], cross["reponse"]

st.markdown('<div class="caption">La colonne centrale et la ligne centrale se croisent. Trouve la valeur au centre.</div>', unsafe_allow_html=True)

def display_cell(text):
    if text is None:
        st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="cell letter-big">{text}</div>', unsafe_allow_html=True)

center_shown = correct if st.session_state.cross_choice is not None else "?"
for i in range(5):
    cols = st.columns(5, gap="large")
    for j in range(5):
        with cols[j]:
            if i == 2 and j == 2:
                display_cell(center_shown)
            elif j == 2:
                display_cell(vert[i])
            elif i == 2:
                display_cell(horiz[j])
            else:
                display_cell(None)

opt_cols = st.columns(5, gap="small")
for idx, opt in enumerate(opts):
    with opt_cols[idx]:
        if st.button(opt, key=f"cross_opt_{st.session_state.cross_round}_{idx}"):
            st.session_state.cross_choice = opt

if st.session_state.cross_choice is not None:
    feedback(
        st.session_state.cross_choice == correct,
        f"✅ Bonne réponse : **{correct}**",
        f"❌ Mauvaise réponse. Correct = **{correct}**, tu as choisi {st.session_state.cross_choice}."
    )
    st.info(f"💡 Explication : {cross['explication']}")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    if st.button("🔄 Mélanger (nouvel exo)"):
        st.session_state.cross_idx = random.randrange(len(cross_exos))
        st.session_state.cross_round += 1
        st.session_state.cross_choice = None
        st.rerun()
with c2:
    if st.button("♻️ Réinitialiser"):
        st.session_state.cross_choice = None
        st.rerun()
with c3:
    if st.button("⏮️ Revenir au 1ᵉʳ exo"):
        st.session_state.cross_idx = 0
        st.session_state.cross_round += 1
        st.session_state.cross_choice = None
        st.rerun()

st.divider()

# =========================================
# 3) Tables de multiplication (10 à 20)
# =========================================
st.header("3️⃣ Tables de multiplication (10 à 20)")

table = st.selectbox("👉 Choisis une table :", list(range(10, 21)), index=0)

if "mult_calc" not in st.session_state or st.session_state.mult_calc[0] != table:
    n = random.randint(1, 20)
    st.session_state.mult_calc = (table, n)

a, b = st.session_state.mult_calc
st.subheader(f"Calcule : **{a} × {b}**")
reponse_mult = st.number_input("👉 Entrez votre réponse :", min_value=0, step=1)

cols_mult = st.columns(2)
with cols_mult[0]:
    if st.button("Vérifier"):
        correct_mult = a * b
        feedback(
            reponse_mult == correct_mult,
            f"✅ Correct ! {a} × {b} = {correct_mult}",
            f"❌ Faux. La bonne réponse est {correct_mult}."
        )
with cols_mult[1]:
    if st.button("Nouveau calcul"):
        st.session_state.mult_calc = (table, random.randint(1, 20))
        st.rerun()

with st.expander(f"📖 Afficher la table de {table}"):
    for i in range(1, 21):
        st.write(f"{table} × {i} = {table*i}")

st.divider()

# =========================================
# 4) Cubes (jusqu’à 13³)
# =========================================
st.header("4️⃣ Les cubes (jusqu’à 13³)")

if "cube_n" not in st.session_state:
    st.session_state.cube_n = random.randint(1, 13)

n = st.session_state.cube_n
st.subheader(f"Calcule : **{n}³**")
reponse_cube = st.number_input("👉 Entrez votre réponse :", min_value=0, step=1, key="cube_input")

cols_cube = st.columns(2)
with cols_cube[0]:
    if st.button("Vérifier", key="verif_cube"):
        correct_cube = n ** 3
        feedback(
            reponse_cube == correct_cube,
            f"✅ Correct ! {n}³ = {correct_cube}",
            f"❌ Faux. La bonne réponse est {correct_cube}."
        )
with cols_cube[1]:
    if st.button("Nouveau cube"):
        st.session_state.cube_n = random.randint(1, 13)
        st.rerun()

with st.expander("📖 Afficher les cubes de 1 à 13"):
    for i in range(1, 14):
        st.write(f"{i}³ = {i**3}")

st.divider()

# =========================================
# 5) Nombres premiers
# =========================================
st.header("5️⃣ Les nombres premiers")

if "prime_n" not in st.session_state:
    st.session_state.prime_n = random.randint(2, 100)

def est_premier(x):
    if x < 2:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

nprime = st.session_state.prime_n
st.subheader(f"Ce nombre est-il premier ? 👉 **{nprime}**")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ Premier"):
        feedback(
            est_premier(nprime),
            f"✅ Correct ! {nprime} est bien premier.",
            f"❌ Faux. {nprime} n’est pas premier."
        )
with c2:
    if st.button("❌ Non premier"):
        feedback(
            not est_premier(nprime),
            f"✅ Correct ! {nprime} n’est pas premier.",
            f"❌ Faux. {nprime} est premier."
        )

if st.button("🔄 Nouveau nombre"):
    st.session_state.prime_n = random.randint(2, 100)
    st.rerun()

with st.expander("📖 Afficher les nombres premiers jusqu’à 100"):
    primes = [x for x in range(2, 101) if est_premier(x)]
    st.write(", ".join(map(str, primes)))
