import streamlit as st
import random
import string

st.set_page_config(page_title="Entraînement Lettres & Logique", page_icon="🔠", layout="centered")

# ---------------------------
# STYLES (pour mimer la photo)
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
# 2) EXERCICES : suites logiques (affichage photo)
# =========================================
st.header("2️⃣ Suites logiques (affichage identique à la photo)")

# Banque d'exercices (tu peux en ajouter autant que tu veux)
# Chaque question est une liste de 5 éléments avec un "?" au centre (index 2).
exos = [
    # ⬇️ Celui de ta photo
    {
        "question": ["OUI", "NHK", "?", "LXO", "KYQ"],
        "options":  ["ZDT", "UEA", "RGW", "SHC"],
        "reponse":  "UEA",
        "explication": "Déplacements réguliers (type César) par colonne ; parmi les 4 choix, **UEA** est le seul qui respecte simultanément les 3 colonnes."
    },
    {
        "question": ["A", "C", "?", "G", "I"],
        "options":  ["D", "E", "F", "H"],
        "reponse":  "E",
        "explication": "On avance de 2 lettres à chaque ligne : A → C → E → G → I."
    },
    {
        "question": ["BDF", "CEG", "?", "EGI", "FHJ"],
        "options":  ["DEF", "DGH", "DFH", "DGI"],
        "reponse":  "DFH",
        "explication": "Dans chaque triplet, chaque lettre décale de +1 à la ligne suivante."
    },
]

# État
if "taj_idx" not in st.session_state:
    st.session_state.taj_idx = 0  # on montrera le 1er exo (la photo)
if "taj_round" not in st.session_state:
    st.session_state.taj_round = 0
if "taj_choice" not in st.session_state:
    st.session_state.taj_choice = None
if "taj_show_solution" not in st.session_state:
    st.session_state.taj_show_solution = False

exo = exos[st.session_state.taj_idx]
rows = exo["question"]
assert len(rows) == 5 and rows[2] == "?", "Chaque exercice doit avoir 5 lignes avec '?' au centre."
opts = exo["options"]
assert len(opts) == 4, "Chaque exercice doit avoir 4 propositions."

# ============
# Rendu visuel
# ============
st.markdown('<div class="caption">Clique directement sur une des 4 propositions autour du “?”</div>', unsafe_allow_html=True)

def render_row(left=None, left_mid=None, center=None, right_mid=None, right=None, row_key="row"):
    # 5 colonnes comme sur la photo : [gauche, mid-gauche, centre, mid-droite, droite]
    cols = st.columns([1,1,1,1,1], gap="large")
    with cols[0]:
        if left is not None:
            st.markdown(f'<div class="cell letter-big">{left}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
    with cols[1]:
        if left_mid is not None:
            st.markdown(f'<div class="cell letter-big">{left_mid}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="cell letter-big">{center if center else "&nbsp;"}</div>', unsafe_allow_html=True)
    with cols[3]:
        if right_mid is not None:
            st.markdown(f'<div class="cell letter-big">{right_mid}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
    with cols[4]:
        if right is not None:
            st.markdown(f'<div class="cell letter-big">{right}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)

# Lignes 1 et 2 (uniquement au centre)
render_row(center=rows[0], row_key="r0")
render_row(center=rows[1], row_key="r1")

# Ligne 3 (celle du “?”) avec 4 propositions autour
cols_mid = st.columns([1,1,1,1,1], gap="large")
with cols_mid[0]:
    if st.button(opts[0], key=f"opt_{st.session_state.taj_round}_0", help="Choisir"):
        st.session_state.taj_choice = opts[0]
with cols_mid[1]:
    if st.button(opts[1], key=f"opt_{st.session_state.taj_round}_1", help="Choisir"):
        st.session_state.taj_choice = opts[1]
with cols_mid[2]:
    st.markdown(f'<div class="cell letter-big">?</div>', unsafe_allow_html=True)
with cols_mid[3]:
    if st.button(opts[2], key=f"opt_{st.session_state.taj_round}_2", help="Choisir"):
        st.session_state.taj_choice = opts[2]
with cols_mid[4]:
    if st.button(opts[3], key=f"opt_{st.session_state.taj_round}_3", help="Choisir"):
        st.session_state.taj_choice = opts[3]

# Lignes 4 et 5 (uniquement au centre)
render_row(center=rows[3], row_key="r3")
render_row(center=rows[4], row_key="r4")

st.markdown('<div class="row-gap"></div>', unsafe_allow_html=True)

# Vérification immédiate + explication
if st.session_state.taj_choice is not None:
    if st.session_state.taj_choice == exo["reponse"]:
        st.success(f"✅ Bonne réponse : {exo['reponse']}")
    else:
        st.error(f"❌ Mauvaise réponse. La bonne réponse était **{exo['reponse']}**.")
    st.info(f"💡 Explication : {exo['explication']}")

# Actions
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔄 Mélanger (nouvel exercice)", key="new_taj"):
        st.session_state.taj_idx = random.randrange(len(exos))
        st.session_state.taj_round += 1
        st.session_state.taj_choice = None
        st.rerun()
with c2:
    if st.button("⏮️ Revenir à l'exercice de la photo", key="goto_photo"):
        st.session_state.taj_idx = 0
        st.session_state.taj_round += 1
        st.session_state.taj_choice = None
        st.rerun()
with c3:
    if st.button("♻️ Réinitialiser le choix", key="reset_choice"):
        st.session_state.taj_choice = None
        st.rerun()
