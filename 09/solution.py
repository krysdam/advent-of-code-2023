def extrapolate_forwards(seq: list) -> int:
    """Extrapolate the next value of the polynomial sequence."""
    # If the sequence is all zeros, the next value is zero.
    if all(x == 0 for x in seq):
        return 0
    # Else, next value is the last value
    # plus the current first-difference.
    differences = [b - a for a, b in zip(seq, seq[1:])]
    return seq[-1] + extrapolate_forwards(differences)
    
if __name__ == '__main__':
    sequences = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            sequence = [int(x) for x in line.split()]
            sequences.append(sequence)

    # Part 1: extrapolate forwards
    sum1 = sum(extrapolate_forwards(seq) for seq in sequences)
    print("Part 1:", sum1)

    # Part 2: extrapolate backwards
    # These are polynomials, so I can just reverse the sequence.
    sum2 = sum(extrapolate_forwards(seq[::-1]) for seq in sequences)
    print("Part 2:", sum2)