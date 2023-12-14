def is_a_symbol(s: str) -> bool:
    """Is s a 'symbol'? (Not a digit or a period.)"""
    return s not in '0123456789.'

def pull_number(schematic: list, l: int, start: int, stop: int) -> int:
    """Return the number in schematic[l][start:stop]."""
    return int(schematic[l][start:stop])

def safe_index(s: str, i: int) -> str:
    """Return s[i] if i is in range, otherwise return ''."""
    if 0 <= i < len(s):
        return s[i]
    else:
        return ''

def find_number_coordinates(s: str) -> list:
    """List of tuples indicating [start:stop] of numbers in the string."""
    coords = []
    start = None
    for i in range(len(s)):
        if s[i].isdigit():
            if start is None:
                start = i
        else:
            if start is not None:
                coords.append((start, i))
                start = None
    if start is not None:
        coords.append((start, len(s)))
    return coords

def find_numbers_adjacent_to_symbols(schematic: list) -> list:
    """List (l, start, stop) coordinates of numbers in schematic that are adjacent to 'symbols'."""
    numbers = []
    for l, line in enumerate(schematic):
        for start, stop in find_number_coordinates(line):
            include = False
            # Check left
            if is_a_symbol(safe_index(line, start-1)):
                include = True
            # Check right
            if is_a_symbol(safe_index(line, stop)):
                include = True
            # Check up
            if l > 0:
                for i in range(start-1, stop+1):
                    if is_a_symbol(safe_index(schematic[l-1], i)):
                        include = True
            # Check down
            if l < len(schematic) - 1:
                for i in range(start-1, stop+1):
                    if is_a_symbol(safe_index(schematic[l+1], i)):
                        include = True
            # Append if include
            if include:
                numbers.append((l, start, stop))
    return numbers

def find_gears(schematic: list, numbers: list) -> list:
    """List of pairs of numbers adjacent to 'gear' asterisks in schematic."""
    gears = []
    for l, line in enumerate(schematic):
        for i, char in enumerate(line):
            # Asterisks are candidates for being gears
            if char == '*':
                # Find all adjacent numbers
                adjacent_numbers = []
                for n in numbers:
                    # Within one line, and within one char on either end
                    if n[0] in [l-1, l, l+1] and n[1]-1 <= i <= n[2]:
                        adjacent_numbers.append(pull_number(schematic, *n))
                # If there are two numbers, it's a gear
                if len(adjacent_numbers) == 2:
                    gears.append(adjacent_numbers)
    return gears

if __name__ == '__main__':
    schematic = []
    with open('input.txt') as f:
        for line in f:
            schematic.append(line.strip())
    # [start:stop] coordinates of numbers adjacent to symbols
    numbers = find_numbers_adjacent_to_symbols(schematic)

    # Part 1: sum the numbers
    sum1 = 0
    for l, start, stop in numbers:
        sum1 += pull_number(schematic, l, start, stop)
    print("Part 1:", sum1)

    # Part 2: sum the gear ratios
    sum2 = 0
    gears = find_gears(schematic, numbers)
    for n1, n2 in gears:
        sum2 += n1 * n2
    print("Part 2:", sum2)