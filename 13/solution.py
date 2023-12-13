def pattern_difference(pattern1: list, pattern2: list) -> int:
    """How many pixels differ between these patterns, within their limits?"""
    count = 0
    for row1, row2 in zip(pattern1, pattern2):
        for ch1, ch2 in zip(row1, row2):
            if ch1 != ch2:
                count += 1
    return count

def mirror_smudginess(pattern: list, i: int) -> int:
    """If this pattern has a mirror after row i, how many pixels are smudged?"""
    part1 = list(reversed(pattern[:i]))
    part2 = pattern[i:]
    return pattern_difference(part1, part2)

def find_horizontal_mirrors(pattern: list, smudge: int) -> list:
    """Where could this pattern have horizontal mirrors, allowing for some smudges?"""
    mirrors = []
    for i in range(1, len(pattern)):
        if mirror_smudginess(pattern, i) == smudge:
            mirrors.append(i)
    return mirrors

def transpose(pattern: list) -> list:
    """Transpose the given pattern, rows to columns."""
    return [''.join(row) for row in zip(*pattern)]

def get_score(pattern: list, smudge: int) -> int:
    """The 'score' of the given pattern, as defined in the problem."""
    horizontal_score = sum(find_horizontal_mirrors(pattern, smudge)) * 100
    vertical_score = sum(find_horizontal_mirrors(transpose(pattern), smudge))
    return horizontal_score + vertical_score

if __name__ == '__main__':
    patterns = []
    pattern = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            if line == '':
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(line)
        patterns.append(pattern)

    score1 = sum(get_score(pattern, smudge = 0) for pattern in patterns)
    print("Part 1:", score1)

    score2 = sum(get_score(pattern, smudge = 1) for pattern in patterns)
    print("Part 2:", score2)