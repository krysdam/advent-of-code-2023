def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string of number."""
    return [int(x) for x in s.split()]

def build_differences_pyramid(seq: list) -> list:
    # Consruct a pyramid of Nth differences,
    # Until you hit a row of all zeros.
    pyramid = [seq]
    while not all(x == 0 for x in pyramid[-1]):
        last_row = pyramid[-1]
        differences = [b - a for a, b in zip(last_row, last_row[1:])]
        pyramid.append(differences)
    return pyramid

def extrapolate_forwards(seq: list) -> int:
    """Extrapolate the next value of the polynomial sequence."""
    # Build a pyramid of Nth differences.
    pyramid = build_differences_pyramid(seq)
    # Expand each row, starting from the all zeros row.
    for r, row in enumerate(reversed(pyramid)):
        if r == 0:
            row.append(0)
        else:
            row.append(row[-1] + pyramid[-r][-1])
    # Return the last value of the top row, indicating the actual sequence.
    return pyramid[0][-1]

def extrapolate_backwards(seq: list) -> int:
    """Extrapolate the previous value of the polynomial sequence."""
    # Build a pyramid of Nth differences.
    pyramid = build_differences_pyramid(seq)
    # Expand each row, starting from the all zeros row.
    for r, row in enumerate(reversed(pyramid)):
        if r == 0:
            row.insert(0, 0)
        else:
            row.insert(0, row[0] - pyramid[-r][0])
    # Return the first value of the top row.
    return pyramid[0][0]
    


if __name__ == '__main__':
    total1 = 0
    total2 = 0

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue
            
            # Pull the numbers out of the line
            numbers = pull_numbers(line)
            # Extrapolate the next number in the sequence
            total1 += extrapolate_forwards(numbers)
            # And the previous number
            total2 += extrapolate_backwards(numbers)


    print("Part 1:", total1)
    print("Part 2:", total2)