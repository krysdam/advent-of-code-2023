def HASH(s: str) -> int:
    """Perform the 'HASH' function described in the problem."""
    val = 0
    for ch in s:
        val += ord(ch)
        val = (val * 17) % 256
    return val

def HASHMAP(steps: list) -> int:
    """Perform the 'HASHMAP' function described in the problem. Return the boxes."""
    boxes = [[] for _ in range(256)]
    for step in steps:
        # Label is letters.
        # Operation is either '-' or the focal length as a string digit.
        label = ''
        if '=' in step:
            label = step.split('=')[0]
            operation = step.split('=')[1]
        else:
            label = step[:-1]
            operation = '-'
        assert(label.isalpha())

        # The box is the hash of the label.
        box = HASH(label)

        # If the operation is '-', remove the lens from the box.
        if operation == '-':
            for i, b in enumerate(boxes[box]):
                if b.startswith(label):
                    del boxes[box][i]
                    break
        # If the operation is '=', replace or add the lens to the box.
        else:
            for i, b in enumerate(boxes[box]):
                if b.startswith(label):
                    boxes[box][i] = label + operation
                    break
            else:
                boxes[box].append(label + operation)
    return boxes

def focusing_power(boxes: list) -> int:
    """Find the focusing power of the given boxes, as defined in the problem."""
    focusing_power = 0
    for b, box in enumerate(boxes):
        for l, lens in enumerate(box):
            focusing_power += (1 + b) * (1 + l) * int(lens[-1])
    return focusing_power

if __name__ == '__main__':
    steps = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            steps = line.split(',')
    
    # Part 1: HASH checksum
    total = 0
    for step in steps:
        total += HASH(step)
    print("Part 1:", total)

    # Part 2: HASHMAP boxes and lenses
    boxes = HASHMAP(steps)
    print("Part 2:", focusing_power(boxes))