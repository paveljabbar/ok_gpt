from collections import defaultdict

def get_valid_color_series(hand):
    color_map = defaultdict(list)
    for card in hand:
        num = int(card[:-1])
        color = card[-1]
        color_map[color].append(num)

    valid_series = []
    for color, nums in color_map.items():
        nums = sorted(set(nums))
        for i in range(len(nums) - 2):
            if nums[i+1] == nums[i]+1 and nums[i+2] == nums[i]+2:
                valid_series.append([
                    f"{nums[i]}{color}",
                    f"{nums[i+1]}{color}",
                    f"{nums[i+2]}{color}",
                ])
    return valid_series

def play_color_series(hand, series):
    return [card for card in hand if card not in series]

def recommend_discard(hand):
    # Karten, die in keiner potenziellen Serie sind
    all_series_cards = set()
    for series in get_valid_color_series(hand):
        all_series_cards.update(series)

    candidates = [card for card in hand if card not in all_series_cards]
    if candidates:
        # Einfachste Heuristik: verwerfe niedrigste Karte unter den nutzlosen
        return sorted(candidates, key=lambda x: int(x[:-1]))[0]
    else:
        # Wenn alle Karten potenziell brauchbar sind, verwerfe niedrigste
        return sorted(hand, key=lambda x: int(x[:-1]))[0]
