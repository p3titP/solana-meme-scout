import streamlit as st
import random
import string

st.set_page_config(page_title="Jeu de l'Alphabet", page_icon="🔠", layout="centered")

st.title("🔠 Jeu de l'Alphabet")

# Générer une lettre aléatoire si elle n'existe pas déjà dans la session
if "lettre" not in st.session_state:
    st.session_state.lettre = random.choice(string.ascii_uppercase)

# Afficher la lettre à deviner
st.subheader(f"Quelle est la position de la lettre : **{st.session_state.lettre}** ?")

# Champ de réponse
reponse = st.number_input("👉 Entrez le numéro de la lettre dans l'alphabet :", min_value=1, max_value=26, step=1)

# Vérification de la réponse
if st.button("Vérifier"):
    correct = string.ascii_uppercase.index(st.session_state.lettre) + 1
    if reponse == correct:
        st.success(f"✅ Bravo ! {st.session_state.lettre} est bien la {correct}ᵉ lettre de l'alphabet.")
    else:
        st.error(f"❌ Oups ! La bonne réponse était {correct}.")

# Nouveau tour
if st.button("Nouvelle lettre"):
    st.session_state.lettre = random.choice(string.ascii_uppercase)
    st.rerun()
