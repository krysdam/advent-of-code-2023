def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string of number."""
    return [int(x) for x in s.split()]

def build_differences_pyramid(seq: list) -> list:
    """A pyramid of Nth differences, down to a row of all zeros."""
    # Start with the sequence itself.
    pyramid = [seq]
    # Build rows of differences until we get a row of all zeros.
    while not all(x == 0 for x in pyramid[-1]):
        last_row = pyramid[-1]
        differences = [b - a for a, b in zip(last_row, last_row[1:])]
        pyramid.append(differences)
    return pyramid

def extrapolate_forwards(seq: list) -> int:
    """Extrapolate the next value of the polynomial sequence."""
    # Build a pyramid of Nth differences.
    pyramid = build_differences_pyramid(seq)
    # Starting from the row of zeros, consruct one more value for each row.
    for r, row in enumerate(reversed(pyramid)):
        if r == 0:
            row.append(0)
        else:
            row.append(row[-1] + pyramid[-r][-1])
    # Return the last value of the sequence itself (row 0).
    return pyramid[0][-1]
    
if __name__ == '__main__':
    total1 = 0
    total2 = 0

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue
            
            numbers = pull_numbers(line)
            
            # Part 1: extrapolate forwards
            total1 += extrapolate_forwards(numbers)

            # Part 2: extrapolate backwards
            total2 += extrapolate_forwards(numbers[::-1])

    print("Part 1:", total1)
    print("Part 2:", total2)