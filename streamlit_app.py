import streamlit as st
from collections import Counter

st.set_page_config(page_title="Metin2 Okey Event - Nur gleichfarbige Serien", layout="wide")

st.title("🃏 Metin2 Okey-Event (Farbreine Serien Only)")

COLORS = ["🔴", "🟡", "🔵"]
COLOR_NAMES = {"🔴": "rot", "🟡": "gelb", "🔵": "blau"}

# Initialisieren des Session State
if "hand" not in st.session_state:
    st.session_state.hand = []

# Karten-Button-Bereich
st.markdown("### ➕ Karte auswählen")
cols = st.columns(8)
for i in range(8):
    with cols[i]:
        for color in COLORS:
            if st.button(f"{i+1} {color}", key=f"{color}{i+1}"):
                if len(st.session_state.hand) < 5:
                    st.session_state.hand.append((i+1, color))
                else:
                    st.warning("Maximal 5 Karten in der Hand!")

# Hand anzeigen
st.markdown("### ✋ Deine aktuelle Hand")
if st.session_state.hand:
    st.write("Karten:", " | ".join([f"{v} {c}" for v, c in st.session_state.hand]))
else:
    st.write("Noch keine Karten auf der Hand.")

# Hilfsfunktion für Serienprüfung
def find_colored_series(hand):
    # Gruppiere nach Farbe
    best_series = None
    best_score = -1

    for color in COLORS:
        values = sorted([v for v, c in hand if c == color])
        for i in range(len(values) - 2):
            if values[i+1] == values[i]+1 and values[i+2] == values[i]+2:
                score = values[i] + values[i+1] + values[i+2]  # einfache Bewertung
                if score > best_score:
                    best_score = score
                    best_series = [(values[i], color), (values[i+1], color), (values[i+2], color)]

    return best_series

# Empfehlungen anzeigen, wenn 5 Karten vorhanden sind
if len(st.session_state.hand) == 5:
    st.markdown("### ✅ Empfehlung")

    series = find_colored_series(st.session_state.hand)
    if series:
        st.success("Du kannst eine Serie legen:")
        st.write(" ➝ ", " | ".join([f"{v} {c}" for v, c in series]))

        if st.button("✔️ Serie bestätigen"):
            for card in series:
                st.session_state.hand.remove(card)
            st.success("Serie gelegt!")
    else:
        st.info("Keine gültige farbreine Serie. Empfehlung: Karte abwerfen.")
        # Zeige Vorschlag, welche Karte weg soll
        count_by_value = Counter([v for v, c in st.session_state.hand])
        least_common = count_by_value.most_common()[-1][0]
        card_to_discard = next(card for card in st.session_state.hand if card[0] == least_common)
        st.write("🗑 Empfehlung: ", f"{card_to_discard[0]} {card_to_discard[1]}")
        if st.button("🗑 Karte abwerfen"):
            st.session_state.hand.remove(card_to_discard)
            st.success("Karte verworfen.")

# Reset-Button
st.markdown("---")
if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.hand = []
    st.success("Hand zurückgesetzt.")
