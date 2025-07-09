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
def find_colored_series(hand):
    best_series = None
    best_score = -1
    for color in COLORS:
        values = sorted([v for v, c in hand if c == color])
        for i in range(len(values) - 2):
            if values[i+1] == values[i]+1 and values[i+2] == values[i]+2:
                score = values[i] + values[i+1] + values[i+2]  # einfache Bewertung
                series = [(values[i], color), (values[i+1], color), (values[i+2], color)]
                if score > best_score:
                    best_score = score
                    best_series = series
    return best_series

# Empfehlung, wenn 5 Karten in der Hand
if len(st.session_state.hand) == 5:
    st.markdown("### ✅ Empfehlung (basierend auf farbreinen Serien)")

    series = find_colored_series(st.session_state.hand)
    if series:
        st.success("Vorschlag: Serie legen → " + " | ".join([f"{v} {c}" for v, c in series]))
        if st.button("✔️ Serie legen"):
            for card in series:
                st.session_state.hand.remove(card)
            st.session_state.played_series.append(series)
            st.success("Serie gelegt!")
    else:
        st.info("Keine gültige farbreine Serie gefunden.")
        # Karte zum Verwerfen vorschlagen
        count_by_value = Counter([v for v, c in st.session_state.hand])
        least_common = count_by_value.most_common()[-1][0]
        card_to_discard = next(card for card in st.session_state.hand if card[0] == least_common)
        st.write(f"🗑 Vorschlag: Karte abwerfen → {card_to_discard[0]} {card_to_discard[1]}")
        if st.button("🗑 Karte abwerfen"):
            st.session_state.hand.remove(card_to_discard)
            st.session_state.discarded_cards.append(card_to_discard)
            st.success("Karte verworfen.")

# Anzeigen: Spielverlauf
with st.expander("📜 Verlauf anzeigen (Serien, Verworfenes, Gezogene Karten)"):
    st.subheader("✔️ Gespielte Serien:")
    if st.session_state.played_series:
        for idx, s in enumerate(st.session_state.played_series, 1):
            st.write(f"Serie {idx}: " + " | ".join([f"{v} {c}" for v, c in s]))
    else:
        st.write("Noch keine Serien gelegt.")

    st.subheader("🗑️ Verworfen:")
    if st.session_state.discarded_cards:
        st.write(" | ".join([f"{v} {c}" for v, c in st.session_state.discarded_cards]))
    else:
        st.write("Keine Karten verworfen.")

    st.subheader("🃏 Gezogene Karten:")
    if st.session_state.drawn_cards:
        st.write(f"{len(st.session_state.drawn_cards)} / 24")
        st.write(" | ".join([f"{v} {c}" for v, c in st.session_state.drawn_cards]))
    else:
        st.write("Noch keine Karten gezogen.")

# Spiel zurücksetzen
st.markdown("---")
if st.button("🔄 Alles zurücksetzen"):
    for key in ["hand", "drawn_cards", "discarded_cards", "played_series"]:
        st.session_state[key] = []
    st.success("Spiel wurde vollständig zurückgesetzt.")
