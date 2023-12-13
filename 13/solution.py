def get_signature(pattern: list) -> list:
    """The signature of unique rows present in the pattern."""
    return [pattern.index(row) for row in pattern]

def is_symmetric_about(ls: list, i: int) -> bool:
    """Is the list symmetric, first i elements with the rest?"""
    # Before the mirror (inverted) and after the mirror.
    part1 = list(reversed(ls[:i]))
    part2 = ls[i:]
    for el1, el2 in zip(part1, part2):
        if el1 != el2:
            return False
    return True

def find_horizontal_mirrors(pattern: list) -> list:
    """Return the horizontal mirrors of the given pattern."""
    sig = get_signature(pattern)
    mirrors = []
    for i in range(1, len(sig)):
        if is_symmetric_about(sig, i):
            mirrors.append(i)
    return mirrors

def transpose(pattern: list) -> list:
    return [''.join(row) for row in zip(*pattern)]

def get_score(pattern: list) -> int:
    """The score of the given pattern."""
    horizontal_score = sum(find_horizontal_mirrors(pattern)) * 100
    vertical_score = sum(find_horizontal_mirrors(transpose(pattern)))
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

    score = 0
    for pattern in patterns:
        score += get_score(pattern)
    print("Part 1:", score)