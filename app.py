import streamlit as st
import random
import string

st.set_page_config(page_title="Entraînement Lettres, Logique & Maths", page_icon="🔠", layout="centered")

# ---------------------------
# STYLES
# ---------------------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; max-width: 860px; }
.letter-big { font-size: 42px; font-weight: 800; text-align: center; letter-spacing: .25rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
.cell { display:flex; align-items:center; justify-content:center; height:64px; }
.opt button { width:100%; height:64px; font-size:28px; font-weight:700; letter-spacing:.25rem; }
.caption { color: #6b7280; text-align:center; margin-bottom: .25rem; }
</style>
""", unsafe_allow_html=True)

st.title("🔠 Entraînement Lettres, Logique & Maths (style TAJ)")

# =========================================
# 1) EXERCICE : position dans l'alphabet
# =========================================
st.header("1️⃣ Jeu de l'alphabet")

if "lettre" not in st.session_state:
    st.session_state.lettre = random.choice(string.ascii_uppercase)

st.subheader(f"Quelle est la position de la lettre : **{st.session_state.lettre}** ?")
reponse_alpha = st.number_input("👉 Entrez le numéro :", min_value=1, max_value=26, step=1)

cols_alpha = st.columns(2)
with cols_alpha[0]:
    if st.button("Vérifier", key="verif_alpha"):
        correct = string.ascii_uppercase.index(st.session_state.lettre) + 1
        if reponse_alpha == correct:
            st.success(f"✅ Bravo ! {st.session_state.lettre} est bien la {correct}ᵉ lettre.")
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était {correct}.")
with cols_alpha[1]:
    if st.button("Nouvelle lettre", key="new_alpha"):
        st.session_state.lettre = random.choice(string.ascii_uppercase)
        st.rerun()

st.divider()

# =========================================
# 2) EXERCICES : suites logiques avec croix
# =========================================
st.header("2️⃣ Suites logiques en croix (verticale + horizontale)")

exos = [
    {
        "vertical": ["OUI", "NHK", "?", "LXO", "KYQ"],
        "options": ["ZDT", "UEA", "RGW", "SHC"],
        "reponse": "UEA",
        "explication": (
            "La logique est double :\n\n"
            "👉 Verticalement : chaque ligne subit un décalage des lettres.\n"
            "👉 Horizontalement : les colonnes forment aussi des suites régulières.\n\n"
            "➡️ Seule **UEA** respecte à la fois la logique verticale et horizontale."
        )
    },
    {
        "vertical": ["A", "C", "?", "G", "I"],
        "options": ["E", "F", "H", "K"],
        "reponse": "E",
        "explication": (
            "👉 Verticalement : on saute une lettre à chaque fois (A → C → E → G → I).\n"
            "👉 Horizontalement : simple cohérence alphabétique, seul **E** garde la régularité."
        )
    }
]

if "taj_idx" not in st.session_state:
    st.session_state.taj_idx = 0
if "taj_choice" not in st.session_state:
    st.session_state.taj_choice = None

exo = exos[st.session_state.taj_idx]
rows = exo["vertical"]
opts = exo["options"]

st.markdown('<div class="caption">Clique sur la bonne proposition autour du “?”</div>', unsafe_allow_html=True)

cols_top = st.columns(5, gap="large")
for i in [0,1,3,4]:
    cols_top[i].markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
cols_top[2].markdown(f'<div class="cell letter-big">{rows[0]}</div>', unsafe_allow_html=True)

cols2 = st.columns(5, gap="large")
for i in [0,1,3,4]:
    cols2[i].markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
cols2[2].markdown(f'<div class="cell letter-big">{rows[1]}</div>', unsafe_allow_html=True)

cols3 = st.columns(5, gap="large")
if cols3[0].button(opts[0], key="opt0"):
    st.session_state.taj_choice = opts[0]
if cols3[1].button(opts[1], key="opt1"):
    st.session_state.taj_choice = opts[1]
cols3[2].markdown(f'<div class="cell letter-big">?</div>', unsafe_allow_html=True)
if cols3[3].button(opts[2], key="opt2"):
    st.session_state.taj_choice = opts[2]
if cols3[4].button(opts[3], key="opt3"):
    st.session_state.taj_choice = opts[3]

cols4 = st.columns(5, gap="large")
for i in [0,1,3,4]:
    cols4[i].markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
cols4[2].markdown(f'<div class="cell letter-big">{rows[3]}</div>', unsafe_allow_html=True)

cols5 = st.columns(5, gap="large")
for i in [0,1,3,4]:
    cols5[i].markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
cols5[2].markdown(f'<div class="cell letter-big">{rows[4]}</div>', unsafe_allow_html=True)

if st.session_state.taj_choice is not None:
    if st.session_state.taj_choice == exo["reponse"]:
        st.success(f"✅ Bonne réponse : {exo['reponse']}")
    else:
        st.error(f"❌ Mauvaise réponse. La bonne réponse était **{exo['reponse']}**.")
    st.info(f"💡 Explication : {exo['explication']}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 Nouvel exercice"):
        st.session_state.taj_idx = random.randrange(len(exos))
        st.session_state.taj_choice = None
        st.rerun()
with c2:
    if st.button("♻️ Réinitialiser choix"):
        st.session_state.taj_choice = None
        st.rerun()

st.divider()

# =========================================
# 3) EXERCICES : tables de multiplication (10 → 20)
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
    if st.button("Vérifier", key="verif_mult"):
        correct = a * b
        if reponse_mult == correct:
            st.success(f"✅ Correct ! {a} × {b} = {correct}")
        else:
            st.error(f"❌ Faux. La bonne réponse est {correct}.")
with cols_mult[1]:
    if st.button("Nouveau calcul", key="new_mult"):
        st.session_state.mult_calc = (table, random.randint(1, 20))
        st.rerun()

st.divider()

# =========================================
# 4) EXERCICE : cubes (jusqu’à 13³)
# =========================================
st.header("4️⃣ Les cubes (jusqu’à 13³)")

if "cube_n" not in st.session_state:
    st.session_state.cube_n = random.randint(1, 13)

n = st.session_state.cube_n
st.subheader(f"Calcule : **{n}³**")

reponse_cube = st.number_input("👉 Entrez votre réponse :", min_value=0, step=1)

cols_cube = st.columns(2)
with cols_cube[0]:
    if st.button("Vérifier", key="verif_cube"):
        correct = n ** 3
        if reponse_cube == correct:
            st.success(f"✅ Correct ! {n}³ = {correct}")
        else:
            st.error(f"❌ Faux. La bonne réponse est {correct}.")
with cols_cube[1]:
    if st.button("Nouveau cube", key="new_cube"):
        st.session_state.cube_n = random.randint(1, 13)
        st.rerun()

st.divider()

# =========================================
# 5) EXERCICE : nombres premiers
# =========================================
st.header("5️⃣ Les nombres premiers")

if "prime_n" not in st.session_state:
    st.session_state.prime_n = random.randint(2, 100)

def est_premier(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

n = st.session_state.prime_n
st.subheader(f"Ce nombre est-il premier ? 👉 **{n}**")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ Premier"):
        if est_premier(n):
            st.success(f"✅ Correct ! {n} est bien premier.")
        else:
            st.error(f"❌ Faux. {n} n’est pas premier.")
with c2:
    if st.button("❌ Non premier"):
        if not est_premier(n):
            st.success(f"✅ Correct ! {n} n’est pas premier.")
        else:
            st.error(f"❌ Faux. {n} est premier.")

if st.button("🔄 Nouveau nombre premier", key="new_prime"):
    st.session_state.prime_n = random.randint(2, 100)
    st.rerun()
