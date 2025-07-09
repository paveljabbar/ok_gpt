import streamlit as st
from collections import Counter

st.set_page_config(page_title="Metin2 Okey Event - Nur farbige Serien", layout="wide")
st.title("🃏 Metin2 Okey-Event – Nur farbreine Serien (tote Karten zuerst)")

COLORS = ["🔴", "🟡", "🔵"]

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
            disabled = card in st.session_state.drawn_cards
            button_key = f"btn_{card[0]}_{color}"
            if disabled:
                st.button(f"{card[0]} {color}", key=button_key, disabled=True)
            else:
                if st.button(f"{card[0]} {color}", key=button_key):
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

# Serie finden (erste gültige farbreine 3er-Serie)
def find_colored_series(hand):
    for color in COLORS:
        values = sorted([v for v, c in hand if c == color])
        for i in range(len(values) - 2):
            if values[i+1] == values[i]+1 and values[i+2] == values[i]+2:
                return [(values[i], color), (values[i+1], color), (values[i+2], color)]
    return None

# ✅ NEUE Abwurf-Logik: Tote Karten zuerst!
def suggest_card_to_discard(hand, discarded):
    all_series = [(i, i+1, i+2) for i in range(1, 7)]

    # Mögliche Serien pro Farbe, unter Berücksichtigung der verworfenen Karten
    possible_series = []
    for color in COLORS:
        for s in all_series:
            if all((num, color) not in discarded for num in s):
                possible_series.append([(num, color) for num in s])

    card_scores = {}
    for card in hand:
        count = 0
        for serie in possible_series:
            if card in serie:
                count += 1
        card_scores[card] = count

    # 1. Finde tote Karten (keine Serie möglich)
    dead_cards = [card for card, score in card_scores.items() if score == 0]
    if dead_cards:
        return dead_cards[0]  # Priorität: erste tote Karte

    # 2. Sonst: wähle Karte mit geringstem Serienpotenzial
    sorted_cards = sorted(card_scores.items(), key=lambda x: x[1])
    return sorted_cards[0][0] if sorted_cards else None

# Empfehlung bei 5 Karten
if len(st.session_state.hand) == 5:
    st.markdown("### ✅ Empfehlung (tote Karten werden bevorzugt abgeworfen)")

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

        card_to_discard = suggest_card_to_discard(
            st.session_state.hand, st.session_state.discarded_cards
        )

        if card_to_discard:
            st.write(f"🗑 Vorschlag: Karte abwerfen → {card_to_discard[0]} {card_to_discard[1]}")
            if st.button("🗑 Karte abwerfen"):
                st.session_state.hand.remove(card_to_discard)
                st.session_state.discarded_cards.append(card_to_discard)
                st.success("Karte verworfen.")
        else:
            st.warning("Keine Empfehlung möglich.")

# Spielverlauf anzeigen
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

# Zurücksetzen
st.markdown("---")
if st.button("🔄 Alles zurücksetzen"):
    for key in ["hand", "drawn_cards", "discarded_cards", "played_series"]:
        st.session_state[key] = []
    st.success("Spiel wurde vollständig zurückgesetzt.")
