import streamlit as st
import random
import string

st.set_page_config(page_title="Entraînement Lettres, Logique & Maths", page_icon="🔠", layout="centered")

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
reponse_alpha = st.number_input("👉 Entrez le numéro :", min_value=1, max_value=26, step=1, key="alpha_input")

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
# 2) EXERCICES : CROISEMENT (verticale + horizontale) -- style Tage Mage
# =========================================
st.header("2️⃣ Suites croisées (verticale + horizontale) — trouve l'intersection")

# Banque d'exos croisés : chaque exo contient :
# - vertical : liste de 5 éléments (strings)
# - horizontal : liste de 5 éléments (strings)
# - options : liste de 5 propositions (strings)
# - reponse : valeur correcte de la case centrale (string)
# - explication : explication texte
cross_exos = [
    # exo 1 : nombres (centre = 5)
    {
        "vertical": ["3", "4", "5", "6", "7"],
        "horizontal": ["1", "3", "5", "7", "9"],
        "options": ["1", "3", "5", "7", "9"],
        "reponse": "5",
        "explication": "Verticalement la suite augmente de +1 (3,4,5,6,7). Horizontalement la suite augmente de +2 (1,3,5,7,9). Le centre commun est 5."
    },
    # exo 2 : lettres (centre = G)
    {
        "vertical": ["C", "E", "G", "I", "K"],
        "horizontal": ["E", "F", "G", "H", "I"],
        "options": ["C", "E", "G", "H", "I"],
        "reponse": "G",
        "explication": "Verticalement on saute 2 lettres (C,E,G,I,K). Horizontalement progression +1 (E,F,G,H,I). Le centre commun est G."
    },
    # exo 3 : nombres (centre = 12)
    {
        "vertical": ["6", "9", "12", "15", "18"],
        "horizontal": ["2", "7", "12", "17", "22"],
        "options": ["2", "7", "12", "17", "22"],
        "reponse": "12",
        "explication": "Verticalement step = +3 (6,9,12,15,18). Horizontalement step = +5 (2,7,12,17,22). Centre : 12."
    },
    # exo 4 : lettres (centre = M)
    {
        "vertical": ["E", "I", "M", "Q", "U"],
        "horizontal": ["G", "J", "M", "P", "S"],
        "options": ["E", "G", "M", "P", "S"],
        "reponse": "M",
        "explication": "Verticalement +4 lettres (E,I,M,Q,U). Horizontalement +3 lettres (G,J,M,P,S). Centre : M."
    }
]

# état
if "cross_idx" not in st.session_state:
    st.session_state.cross_idx = 0
if "cross_round" not in st.session_state:
    st.session_state.cross_round = 0
if "cross_choice" not in st.session_state:
    st.session_state.cross_choice = None

cross = cross_exos[st.session_state.cross_idx]
vert = cross["vertical"]
horiz = cross["horizontal"]
opts = cross["options"]
correct = cross["reponse"]

st.markdown('<div class="caption">Tu vois la colonne centrale (verticale) et la ligne centrale (horizontale). La case au centre est la même pour les deux suites — choisis la bonne option ci-dessous.</div>', unsafe_allow_html=True)

# fonction d'affichage de cellule
def display_cell(text, is_center=False):
    """Retourne le HTML pour une cellule (text)."""
    if text is None:
        st.markdown('<div class="cell">&nbsp;</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="cell letter-big">{text}</div>', unsafe_allow_html=True)

# on affiche la grille 5x5 "croisée" :
# - pour les lignes 0,1,3,4 : seule la colonne 2 (centre) montre l'élément vertical correspondant
# - pour la ligne 2 : on affiche la suite horizontale (avec centre remplacé par '?', ou la réponse si déjà choisie)
center_shown = correct if st.session_state.cross_choice is not None else "?"

for i in range(5):
    cols = st.columns(5, gap="large")
    for j in range(5):
        with cols[j]:
            # centre réel (i==2 and j==2)
            if i == 2 and j == 2:
                display_cell(center_shown)
            # colonne centrale (j==2) pour lignes autres que centre : vertical element
            elif j == 2:
                display_cell(vert[i])
            # ligne centrale (i==2) pour colonnes autres que centre : horizontal element
            elif i == 2:
                display_cell(horiz[j])
            else:
                display_cell(None)

st.markdown("")  # petit espace

# Boutons d'options (5 choix)
opt_cols = st.columns(5, gap="small")
for idx, opt in enumerate(opts):
    with opt_cols[idx]:
        if st.button(opt, key=f"cross_opt_{st.session_state.cross_round}_{idx}", help="Choisir cette option"):
            st.session_state.cross_choice = opt

# Feedback
if st.session_state.cross_choice is not None:
    if st.session_state.cross_choice == correct:
        st.success(f"✅ Bonne réponse : **{correct}**")
    else:
        st.error(f"❌ Mauvaise réponse. La bonne réponse était **{correct}** (tu as choisi {st.session_state.cross_choice}).")
    st.info(f"💡 Explication : {cross['explication']}")

# Actions : nouvel exo / reset choix / revenir au premier exo
c1, c2, c3 = st.columns([1,1,1])
with c1:
    if st.button("🔄 Mélanger (nouvel exo)", key=f"cross_new"):
        st.session_state.cross_idx = random.randrange(len(cross_exos))
        st.session_state.cross_round += 1
        st.session_state.cross_choice = None
        st.rerun()
with c2:
    if st.button("♻️ Réinitialiser le choix", key="cross_reset"):
        st.session_state.cross_choice = None
        st.rerun()
with c3:
    if st.button("⏮️ Revenir au 1ᵉʳ exo", key="cross_first"):
        st.session_state.cross_idx = 0
        st.session_state.cross_round += 1
        st.session_state.cross_choice = None
        st.rerun()

st.divider()

# =========================================
# 3) EXERCICES : tables de multiplication (10 → 20)
# =========================================
st.header("3️⃣ Tables de multiplication (10 à 20)")

table = st.selectbox("👉 Choisis une table :", list(range(10, 21)), index=0, key="table_select")

if "mult_calc" not in st.session_state or st.session_state.mult_calc[0] != table:
    n = random.randint(1, 20)
    st.session_state.mult_calc = (table, n)

a, b = st.session_state.mult_calc
st.subheader(f"Calcule : **{a} × {b}**")
reponse_mult = st.number_input("👉 Entrez votre réponse :", min_value=0, step=1, key="mult_input")

cols_mult = st.columns(2)
with cols_mult[0]:
    if st.button("Vérifier", key="verif_mult"):
        correct_mult = a * b
        if reponse_mult == correct_mult:
            st.success(f"✅ Correct ! {a} × {b} = {correct_mult}")
        else:
            st.error(f"❌ Faux. La bonne réponse est {correct_mult}.")
with cols_mult[1]:
    if st.button("Nouveau calcul", key="new_mult"):
        st.session_state.mult_calc = (table, random.randint(1, 20))
        st.rerun()

with st.expander(f"📖 Afficher la table de {table}"):
    for i in range(1, 21):
        st.write(f"{table} × {i} = {table*i}")

st.divider()

# =========================================
# 4) EXERCICE : cubes (jusqu’à 13³)
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
        if reponse_cube == correct_cube:
            st.success(f"✅ Correct ! {n}³ = {correct_cube}")
        else:
            st.error(f"❌ Faux. La bonne réponse est {correct_cube}.")
with cols_cube[1]:
    if st.button("Nouveau cube", key="new_cube"):
        st.session_state.cube_n = random.randint(1, 13)
        st.rerun()

with st.expander("📖 Afficher les cubes de 1 à 13"):
    for i in range(1, 14):
        st.write(f"{i}³ = {i**3}")

st.divider()

# =========================================
# 5) EXERCICE : nombres premiers
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
    if st.button("✅ Premier", key="prime_yes"):
        if est_premier(nprime):
            st.success(f"✅ Correct ! {nprime} est bien premier.")
        else:
            st.error(f"❌ Faux. {nprime} n’est pas premier.")
with c2:
    if st.button("❌ Non premier", key="prime_no"):
        if not est_premier(nprime):
            st.success(f"✅ Correct ! {nprime} n’est pas premier.")
        else:
            st.error(f"❌ Faux. {nprime} est premier.")

if st.button("🔄 Nouveau nombre", key="new_prime"):
    st.session_state.prime_n = random.randint(2, 100)
    st.rerun()

with st.expander("📖 Afficher les nombres premiers jusqu’à 100"):
    primes = [x for x in range(2, 101) if est_premier(x)]
    st.write(", ".join(map(str, primes)))
