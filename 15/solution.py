def HASH(s: str) -> int:
    val = 0
    for ch in s:
        val += ord(ch)
        val = (val * 17) % 256
    return val

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
    boxes = [[] for _ in range(256)]
    for step in steps:
        label = ''
        if '=' in step:
            label = step.split('=')[0]
            operation = step.split('=')[1]
        else:
            label = step[:-1]
            operation = '-'
        assert(label.isalpha())
        box = HASH(label)

        if operation == '-':
            for i, b in enumerate(boxes[box]):
                if b.startswith(label):
                    del boxes[box][i]
                    break
        else:
            for i, b in enumerate(boxes[box]):
                if b.startswith(label):
                    boxes[box][i] = label + operation
                    break
            else:
                boxes[box].append(label + operation)

        
    focusing_power = 0
    for b, box in enumerate(boxes):
        for l, lens in enumerate(box):
            focusing_power += (1 + b) * (1 + l) * int(lens[-1])
    print("Part 2:", focusing_power)