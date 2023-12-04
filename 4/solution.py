def parse_card(card: str) -> tuple:
    """Parse a card into ([numbers needed], [numbers had])"""
    # Reduce all whitespace to single spaces
    while '  ' in card:
        card = card.replace('  ', ' ')
    # Split into left and right of |
    left, right = card.split('|')
    left = left.strip()
    right = right.strip()
    # Split into items, and toss "Card N:"
    leftparts = left.split(' ')[2:]
    rightparts = right.split(' ')
    # Numbers needed and had
    needed = [int(s) for s in leftparts]
    had = [int(s) for s in rightparts]
    return (needed, had)

def count_matches(needed: list, had: list) -> int:
    """Count the matches between 'needed' and 'had'."""
    return len(set(needed) & set(had))

def score_matches(matches: int) -> int:
    """Score the matches."""
    return 0 if matches == 0 else 2**(matches-1)

def process_won_copies(match_counts: list) -> list:
    """Propogate copies won by the rules."""
    # Start with one of each card
    card_copies = [1] * len(match_counts)
    # For each match-count...
    for i, m in enumerate(match_counts):
        for j in range(m):
            # The next m cards get one copy per copy of this card
            card_copies[i+j+1] += card_copies[i]
    return card_copies

if __name__ == '__main__':
    sum1 = 0
    card_matches = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            # Count matches
            needed, had = parse_card(line)
            matches = count_matches(needed, had)
            card_matches.append(matches)

            # Part 1: score the cards naively by doubling points
            sum1 += score_matches(matches)
    print("Part 1:", sum1)

    # Part 2: score properly by giving out copies
    winnings = process_won_copies(card_matches)
    print("Part 2:", sum(winnings))