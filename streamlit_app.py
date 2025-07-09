import streamlit as st
from collections import Counter

st.set_page_config(page_title="Metin2 Okey Event - Nur farbige Serien", layout="wide")
st.title("🃏 Metin2 Okey-Event – Nur farbreine Serien (6-7-8 Ziel)")

COLORS = ["🔴", "🟡", "🔵"]
COLOR_NAMES = {"🔴": "rot", "🟡": "gelb", "🔵": "blau"}

# Initialisieren von Session States
for key in ["hand", "drawn_cards", "discarded_cards", "played_series"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Karten-Button-Bereich
st.markdown("### ➕ Karte auswählen (max 24 insgesamt, max 5 in Hand)")
cols = st.columns(8)
for i in range(8):
    with cols[i]:
        for color in COLORS:
            card = (i+1, color)
            if st.button(f"{i+1} {color}", key=f"{color}{i+1}"):
                if len(st.session_state.drawn_cards) >= 24:
                    st.warning("Du hast bereits 24 Karten gezogen.")
                elif len(st.session_state.hand) >= 5:
                    st.warning("Deine Hand ist voll (5 Karten).")
                else:
                    st.session_state.hand.append(card)
                    st.session_state.drawn_cards.append(card)

# Anzeige: Hand
st.markdown("### ✋ Aktuelle Hand (max 5 Karten)")
if st.session_state.hand:
    st.write(" | ".join([f"{v} {c}" for v, c in st.session_state.hand]))
else:
    st.info("Noch keine Karten in der Hand.")

# Hilfsfunktion zum Finden gültiger farbiger Serien
def find_colored_
