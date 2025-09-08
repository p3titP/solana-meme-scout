import streamlit as st
import random
import string

st.set_page_config(page_title="Entraînement Lettres & Logique", page_icon="🔠", layout="centered")

st.title("🔠 Entraînement Lettres & Logique (style TAJ MAJ)")

# ---------------------------
# EXERCICE 1 : Position dans l'alphabet
# ---------------------------
st.header("1️⃣ Jeu de l'Alphabet")

if "lettre" not in st.session_state:
    st.session_state.lettre = random.choice(string.ascii_uppercase)

st.subheader(f"Quelle est la position de la lettre : **{st.session_state.lettre}** ?")

reponse = st.number_input("👉 Entrez le numéro :", min_value=1, max_value=26, step=1)

if st.button("Vérifier", key="verif_alpha"):
    correct = string.ascii_uppercase.index(st.session_state.lettre) + 1
    if reponse == correct:
        st.success(f"✅ Bravo ! {st.session_state.lettre} est bien la {correct}ᵉ lettre de l'alphabet.")
    else:
        st.error(f"❌ Mauvaise réponse ! La bonne réponse était {correct}.")

if st.button("Nouvelle lettre", key="new_alpha"):
    st.session_state.lettre = random.choice(string.ascii_uppercase)
    st.rerun()

# ---------------------------
# EXERCICE 2 : Suites logiques de lettres
# ---------------------------
st.header("2️⃣ Suites logiques de lettres")

exercices_logiques = [
    {
        "question": ["OUI", "NHK", "?", "LXO", "KYQ"],
        "options": ["ZDT", "UEA", "RGW", "SHC"],
        "reponse": "UEA",
        "explication": "La suite logique suit un décalage de lettres dans l’alphabet."
    },
    {
        "question": ["A", "C", "E", "?", "I"],
        "options": ["G", "H", "J", "K"],
        "reponse": "G",
        "explication": "On saute une lettre à chaque fois (A, C, E, G, I)."
    },
    {
        "question": ["B", "D", "H", "N", "?"],
        "options": ["T", "U", "V", "W"],
        "reponse": "T",
        "explication": "Les positions doublent à chaque fois : 2, 4, 8, 14, 20 (lettre T)."
    }
]

if "exo" not in st.session_state:
    st.session_state.exo = random.choice(exercices_logiques)

exo = st.session_state.exo

st.subheader("Trouve la suite logique :")
st.write(" → ".join(exo["question"]))

choix = st.radio("Choisis la bonne réponse :", exo["options"], key="choix")

if st.button("Vérifier", key="verif_suite"):
    if choix == exo["reponse"]:
        st.success(f"✅ Bonne réponse ! ({exo['reponse']})")
    else:
        st.error(f"❌ Mauvaise réponse. La bonne réponse était {exo['reponse']}.")
    st.info(f"💡 Explication : {exo['explication']}")

if st.button("Nouvel exercice", key="new_suite"):
    st.session_state.exo = random.choice(exercices_logiques)
    st.rerun()

