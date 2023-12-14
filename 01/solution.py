# Names of the digits (excluding 'zero', which the problem doesn't allow).
DIGIT_NAMES = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
               '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               'one': 1, 'two': 2, 'three': 3, 'four': 4,
               'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

def digits_in(s: str) -> list:
    """List of the digits in the string, as ints."""
    return [int(c) for c in s if c.isdigit()]

def generous_digits_in(s: str) -> list:
    """List of the digits in the string, as ints, including spelled digits like 'eight'."""
    digits = []
    for i in range(len(s)):
        for name in DIGIT_NAMES:
            if s[i:].startswith(name):
                digits.append(DIGIT_NAMES[name])
                break
    return digits

def first_and_last_digit(s: str, generous: bool = False) -> int:
    """The number formed from the first and last digits in the string.
    
    If "generous," include spelled digits like 'eight.'
    """
    if generous:
        digits = generous_digits_in(s)
    else:
        digits = digits_in(s)
    return 10*digits[0] + digits[-1]

if __name__ == '__main__':
    sum1 = 0
    sum2 = 0
    with open('input.txt') as f:
        for line in f:
            sum1 += first_and_last_digit(line.strip())
            sum2 += first_and_last_digit(line.strip(), generous=True)
    print("Part 1:", sum1)
    print("Part 2:", sum2)