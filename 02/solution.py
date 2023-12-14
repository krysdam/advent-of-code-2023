def parse_line(line: str):
    """Parse a game string into (game number, red max, green max, blue max)."""
    # For example:
    # "Game 1: 4 blue, 4 red, 16 green; 14 green, 5 red; 1 blue, 3 red, 5 green"
    # --> (1, 5, 16, 4)

    # Remove syntax
    line = line.strip()
    line = line.replace('Game ', '')
    line = line.replace(':', '')
    line = line.replace(',', '')
    line = line.replace(';', '')

    # Game number and [count, color,  count, color,  ...]
    number, *parts = line.split(' ')
    number = int(number)

    # Counts seen for each color
    reds, greens, blues = [], [], []

    # Counts and colors mentioned in the game data
    counts = parts[::2]
    colors = parts[1::2]

    # Sort the counts into color lists
    for count, color in zip(counts, colors):
        count = int(count)
        if color == 'red':
            reds.append(count)
        elif color == 'green':
            greens.append(count)
        elif color == 'blue':
            blues.append(count)

    # Maximums
    red_max = max(reds)
    green_max = max(greens)
    blue_max = max(blues)
    
    # Return the game number and the counts for each color)
    return (number, red_max, green_max, blue_max)
        
def is_compatible(game: tuple, red: int, green: int, blue: int) -> bool:
    """Is the game compatible with the given facts?"""
    _, red_seen, green_seen, blue_seen = game
    return (red_seen <= red) and (green_seen <= green) and (blue_seen <= blue)

def power(game: tuple):
    """Return the power (product) of a game."""
    _, red_seen, green_seen, blue_seen = game
    return red_seen * green_seen * blue_seen

if __name__ == '__main__':
    sum1 = 0
    sum2 = 0
    with open('input.txt', 'r') as f:
        for line in f:
            game = parse_line(line)

            # Part 1: is the game compatible with 12, 13, 14?
            if is_compatible(game, 12, 13, 14):
                sum1 += game[0]

            # Part 2: what is the power of the game?
            sum2 += power(game)
    print("Part 1:", sum1)
    print("Part 2:", sum2)