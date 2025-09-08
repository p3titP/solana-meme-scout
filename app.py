import streamlit as st
import random
import string

st.set_page_config(page_title="Entraînement Lettres & Logique", page_icon="🔠", layout="centered")

# ---------------------------
# STYLES
# ---------------------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; max-width: 860px; }
.letter-big { font-size: 42px; font-weight: 800; text-align: center; letter-spacing: .25rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
.cell { display:flex; align-items:center; justify-content:center; height:64px; }
.opt button { width:100%; height:64px; font-size:28px; font-weight:700; letter-spacing:.25rem; }
.row-gap { margin: 14px 0; }
.caption { color: #6b7280; text-align:center; margin-bottom: .25rem; }
</style>
""", unsafe_allow_html=True)

st.title("🔠 Entraînement Lettres & Logique (style TAJ)")

# =========================================
# 1) EXERCICE : position dans l'alphabet
# =========================================
st.header("1️⃣ Jeu de l'alphabet")

if "lettre" not in st.session_state:
    st.session_state.lettre = random.choice(string.ascii_uppercase)

st.subheader(f"Quelle est la position de la lettre : **{st.session_state.lettre}** ?")
reponse = st.number_input("👉 Entrez le numéro :", min_value=1, max_value=26, step=1)

cols_alpha = st.columns(2)
with cols_alpha[0]:
    if st.button("Vérifier", key="verif_alpha"):
        correct = string.ascii_uppercase.index(st.session_state.lettre) + 1
        if reponse == correct:
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
            "👉 Verticalement : chaque ligne subit un décalage des lettres (OUI → NHK → … → LXO → KYQ).\n"
            "👉 Horizontalement : les 3 colonnes (1ère lettre, 2e, 3e) forment aussi des suites régulières.\n\n"
            "➡️ Seule **UEA** respecte à la fois la logique verticale et horizontale."
        )
    },
    {
        "vertical": ["A", "C", "?", "G", "I"],
        "options": ["E", "F", "H", "K"],
        "reponse": "E",
        "explication": (
            "👉 Verticalement : on saute une lettre à chaque fois (A → C → E → G → I).\n"
            "👉 Horizontalement : ici simple cohérence alphabétique, seul **E** permet de garder la régularité."
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

# ============
# Rendu visuel
# ============
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

# Correction
if st.session_state.taj_choice is not None:
    if st.session_state.taj_choice == exo["reponse"]:
        st.success(f"✅ Bonne réponse : {exo['reponse']}")
    else:
        st.error(f"❌ Mauvaise réponse. La bonne réponse était **{exo['reponse']}**.")
    st.info(f"💡 Explication : {exo['explication']}")

# Boutons
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
