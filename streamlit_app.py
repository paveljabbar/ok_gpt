import streamlit as st
from okey_logic import (
    get_valid_color_series,
    recommend_discard,
    play_color_series
)

st.set_page_config(page_title="Metin2 Okey Event", layout="centered")
st.title("🃏 Metin2 Okey Event – Farbgleiche Straße Builder")

if "hand" not in st.session_state:
    st.session_state.hand = []
if "played_sets" not in st.session_state:
    st.session_state.played_sets = []
if "score" not in st.session_state:
    st.session_state.score = 0

def reset_game():
    st.session_state.hand = []
    st.session_state.played_sets = []
    st.session_state.score = 0

st.sidebar.button("🔄 Neues Spiel", on_click=reset_game)

# Karten hinzufügen
st.subheader("📥 Karte ziehen")
color = st.selectbox("Farbe", ["r", "g", "b"], format_func=lambda c: {"r": "Rot", "g": "Grün", "b": "Blau"}[c])
number = st.number_input("Zahl", min_value=1, max_value=8, step=1)
if st.button("Karte hinzufügen"):
    st.session_state.hand.append(f"{number}{color}")

# Hand anzeigen
st.subheader("🖐️ Deine Karten")
if st.session_state.hand:
    st.write(" | ".join(st.session_state.hand))
else:
    st.info("Noch keine Karten auf der Hand.")

# Empfehlung anzeigen
if len(st.session_state.hand) >= 5:
    recommended = recommend_discard(st.session_state.hand)
    st.info(f"💡 Empfehlung: Verwerfe **{recommended}**")

# Verwerfen
st.subheader("🗑️ Karte verwerfen")
discard = st.selectbox("Welche Karte willst du verwerfen?", st.session_state.hand)
if st.button("Verwerfen"):
    st.session_state.hand.remove(discard)

# Farbgleiche Serien spielen
st.subheader("✅ Farbgleiche Serie spielen")
valid_sets = get_valid_color_series(st.session_state.hand)

if valid_sets:
    to_play = st.selectbox("Wähle eine farbgleiche Serie", valid_sets, format_func=lambda s: " - ".join(s))
    if st.button("Serie spielen"):
        st.session_state.hand = play_color_series(st.session_state.hand, to_play)
        st.session_state.played_sets.append(to_play)
        st.session_state.score += 60  # Jede farbgleiche Serie = 60 Punkte
        st.success(f"Serie gespielt: {' - '.join(to_play)} (+60 Punkte)")
else:
    st.info("Keine gültige farbgleiche Serie verfügbar.")

# Punktestand
st.subheader("🎯 Punktestand")
st.write(f"**{st.session_state.score} Punkte**")

# Gespielte Serien anzeigen
if st.session_state.played_sets:
    st.subheader("🃏 Gespielte Serien")
    for s in st.session_state.played_sets:
        st.write(" - ".join(s))
