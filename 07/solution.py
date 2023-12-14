CARD_TYPES_PLAIN = 'AKQJT98765432'
CARD_TYPES_JOKER = 'AKQT98765432J'

def hand_type(hand: str) -> int:
    """The "type" of the hand (5 = five of a kind, and so on downwards)."""
    # Count the number of each card type
    counts = [0 for ct in CARD_TYPES_PLAIN]
    for card in hand:
        counts[CARD_TYPES_PLAIN.index(card)] += 1
    # Sort the non-zero counds
    signature = sorted([c for c in counts if c > 0])
    # Five of a kind
    if signature == [5]:
        return 5
    # Four of a kind
    if signature == [1, 4]:
        return 4
    # Full house
    if signature == [2, 3]:
        return 3
    # Three of a kind
    if signature == [1, 1, 3]:
        return 2
    # Two pairs
    if signature == [1, 2, 2]:
        return 1
    # One pair
    if signature == [1, 1, 1, 2]:
        return 0
    # High card
    return -1

def best_possible_hand(hand: str) -> str:
    """The "type" of the hand, at best, with J = Joker = wildcard."""
    options = []
    # Try all the possible interpretations of the Joker
    for card in CARD_TYPES_JOKER:
        if card == 'J':
            continue
        new_hand = hand.replace('J', card)
        options.append(hand_type(new_hand))
    return max(options)

def hand_key(hand: str, jokers: bool = False) -> list:
    """Key for sorting hands."""
    key = []
    # First, the rank of the hand (possibly with generous joker interpretation)
    if jokers:
        key.append(best_possible_hand(hand))
    else:
        key.append(hand_type(hand))
    # Then, the cards in the hand, A is best
    ranking = CARD_TYPES_JOKER if jokers else CARD_TYPES_PLAIN
    key.extend([-ranking.index(card) for card in hand])
    return key

def evaluate_hands(hands: list, jokers: bool = False) -> int:
    """Evaluate the hands, given as a list of tuples (hand, bid)."""
    # Sort the hands, worst first
    hands.sort(key = lambda hand_bid: hand_key(hand_bid[0], jokers = jokers))
    # Calculate the score
    score = 0
    for i, (hand, bid) in enumerate(hands):
        score += bid * (i+1)
    return score

if __name__ == '__main__':
    hands = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue

            hand, bid = line.split(' ')
            bid = int(bid)
            hands.append((hand, bid))

    # Part 1: J means Jack
    print("Part 1:", evaluate_hands(hands, jokers = False))

    # Part 2: J means Joker
    print("Part 2:", evaluate_hands(hands, jokers = True))