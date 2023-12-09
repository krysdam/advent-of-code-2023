def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string of number."""
    return [int(x) for x in s.split()]

def extrapolate_forwards(seq: list) -> int:
    """Extrapolate the next value of the polynomial sequence."""
    # If the sequence is all zeros, the next value is zero.
    if all(x == 0 for x in seq):
        return 0
    # Else, add the next value of this sequence's first differences.
    differences = [b - a for a, b in zip(seq, seq[1:])]
    return seq[-1] + extrapolate_forwards(differences)
    
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