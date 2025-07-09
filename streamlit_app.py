def suggest_card_to_discard(hand, discarded):
    all_series = [(i, i+1, i+2) for i in range(1, 7)]

    # Mögliche Serien unter Ausschluss verworfener Karten
    possible_series = []
    for color in COLORS:
        for s in all_series:
            if all((num, color) not in discarded for num in s):
                possible_series.append([(num, color) for num in s])

    # Karten → zu welchen Serien sie passen
    card_series_map = {card: [] for card in hand}
    for serie in possible_series:
        for card in hand:
            if card in serie:
                card_series_map[card].append(serie)

    # 1. Tote Karten sofort verwerfen
    dead_cards = [card for card, series in card_series_map.items() if not series]
    if dead_cards:
        return dead_cards[0]

    # 2. Bewertete Potenziale
    card_scores = {}
    for card, series_list in card_series_map.items():
        score = 0
        for serie in series_list:
            in_hand = sum(1 for c in serie if c in hand)

            if in_hand == 3:
                score += 3  # komplette Serie (wird eh gelegt)
            elif in_hand == 2:
                # Bonus für benachbarte Karten wie 3+4 oder 4+5
                hand_cards = [c for c in serie if c in hand]
                values = sorted([v for v, c in hand_cards])
                if len(values) == 2 and abs(values[0] - values[1]) == 1:
                    score += 6  # direkt nebeneinander → wertvoll!
                else:
                    score += 4  # Lücke → schwächer
            elif in_hand == 1:
                score += 1

        # Extra-Abwertung für Randzahlen (1 oder 8)
        if card[0] == 1 or card[0] == 8:
            score -= 1  # weniger flexibel

        card_scores[card] = score

    # 3. Karte mit dem geringsten Score abwerfen
    sorted_cards = sorted(card_scores.items(), key=lambda x: x[1])
    return sorted_cards[0][0]
