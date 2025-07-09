import streamlit as st
from collections import Counter

st.set_page_config(page_title="Metin2 Okey Event", layout="wide")
st.title("🃏 Metin2 Okey-Event")

COLORS = ["🔴", "🟡", "🔵"]

# CSS für kompaktes Grid
st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: repeat(8, auto);
        gap: 4px 8px;
        margin-bottom: 10px;
    }
    .card-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }
    .card-col button {
        padding: 2px 6px;
        font-size: 15px;
    }
    div[data-testid="column"] {
        padding-left: 2px;
        padding-right: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisieren von States
for key in ["hand", "drawn_cards", "discarded_cards", "played_series", "last_action"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Kompakter Karten-Auswahlbereich
st.markdown("### ➕ Kartedeck")
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
                        st.warning("Deine Hand ist voll (max. 5 Karten).")
                    else:
                        st.session_state.hand.append(card)
                        st.session_state.drawn_cards.append(card)

# Aktuelle Hand anzeigen
st.markdown("### ✋ Aktuelle Hand")
if st.session_state.hand:
    st.write(" | ".join([f"{v} {c}" for v, c in st.session_state.hand]))
else:
    st.info("Noch keine Karten in der Hand.")

# Serienerkennung
def find_colored_series(hand):
    for color in COLORS:
        values = sorted([v for v, c in hand if c == color])
        for i in range(len(values) - 2):
            if values[i+1] == values[i]+1 and values[i+2] == values[i]+2:
                return [(values[i], color), (values[i+1], color), (values[i+2], color)]
    return None

# Karte zum Abwerfen ermitteln (mit Serie-Potenzial-Multiplikator)
def suggest_card_to_discard(hand, discarded):
    all_series = [(i, i+1, i+2) for i in range(1, 7)]
    possible_series = []
    for color in COLORS:
        for s in all_series:
            if all((num, color) not in discarded for num in s):
                possible_series.append([(num, color) for num in s])

    card_series_map = {card: [] for card in hand}
    for serie in possible_series:
        for card in hand:
            if card in serie:
                card_series_map[card].append(serie)

    # 1. Tote Karten priorisieren
    dead_cards = [card for card, series in card_series_map.items() if not series]
    if dead_cards:
        return dead_cards[0]

    # 2. Bewertete Karten nach Seriennähe und -potenzial
    card_scores = {}
    for card, series_list in card_series_map.items():
        score = 0

        # Wie viele Serien gibt es, in denen die Karte vorkommen kann?
        total_possible_series = len(series_list)

        # Grundwertung nach In-Progress Serien
        for serie in series_list:
            in_hand = sum(1 for c in serie if c in hand)
            values = [v for v, c in serie if (v, c) in hand]
            values.sort()

            if in_hand == 3:
                score += 3
            elif in_hand == 2:
                if abs(values[0] - values[1]) == 1:
                    score += 6
                else:
                    score += 4
            elif in_hand == 1:
                score += 1

        # Bonus: Je mehr verbleibende Serien möglich, desto besser
        score += total_possible_series * 1.5

        # Randkarten abwerten
        if card[0] == 1 or card[0] == 8:
            score -= 1

        card_scores[card] = score

    # Karte mit niedrigstem Score wird abgeworfen
    sorted_cards = sorted(card_scores.items(), key=lambda x: x[1])
    return sorted_cards[0][0]

# Hauptlogik bei voller Hand
if len(st.session_state.hand) == 5:
    st.markdown("### ✅ Automatische Aktion")

    series = find_colored_series(st.session_state.hand)
    if series:
        for card in series:
            st.session_state.hand.remove(card)
        st.session_state.played_series.append(series)
        msg = "Serie automatisch gelegt: " + " | ".join([f"{v} {c}" for v, c in series])
        st.session_state.last_action = msg
        st.success(msg)
    else:
        card_to_discard = suggest_card_to_discard(
            st.session_state.hand, st.session_state.discarded_cards
        )
        st.session_state.hand.remove(card_to_discard)
        st.session_state.discarded_cards.append(card_to_discard)
        msg = f"Karte automatisch abgeworfen: {card_to_discard[0]} {card_to_discard[1]}"
        st.session_state.last_action = msg
        st.info(msg)

# Letzte Aktion anzeigen
if st.session_state.get("last_action"):
    st.caption(f"🕒 Letzte Aktion: {st.session_state.last_action}")

# Verlauf
with st.expander("📜 Verlauf anzeigen"):
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
    for key in ["hand", "drawn_cards", "discarded_cards", "played_series", "last_action"]:
        st.session_state[key] = []
    st.success("Spiel wurde vollständig zurückgesetzt.")
