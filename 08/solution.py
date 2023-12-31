def parse_fork(fork: str) -> tuple:
    """Parse AAA = (BBB, CCC) into ('AAA', 'BBB', 'CCC')."""
    for superfluous in '=(),':
        fork = fork.replace(superfluous, '')
    return tuple(fork.split())

def steps_from_AAA_to_ZZZ(forks: dict, instructions: str) -> int:
    """How many instruction steps from AAA to ZZZ?"""
    # Start at AAA
    position = 'AAA'
    # Follow the instructions
    count = 0
    while position != 'ZZZ':
        for inst in instructions:
            count += 1
            if inst == 'L':
                position = forks[position][0]
            elif inst == 'R':
                position = forks[position][1]
    return count

def steps_from_As_to_Zs(forks: dict, instructions: str) -> int:
    """How many instruction steps from all **As to all **Zs?"""
    starting_points = [k for k in forks.keys() if k[-1] == 'A']
    # The paths from each starting point, up to the first repeat
    cycles = [path_until_repeat(forks, instructions, start) for start in starting_points]

    # In the general case, any element of a cycle could end with Z,
    # and worse still, the cycles might not hit these **Zs at the end of the instructions.
    # However, the puzzle is simpler than the instructions imply.

    # Empirically, the cycles all work like this:
    # - Step 0 is the starting point, which ends with A
    # - Steps 1 to the end are the cycle, which has a prime length
    # - The last step, and only the last step, ends with Z
    # Therefore, the first step at which all paths are at a Z is
    # the product of (len - 1) for each cycle,
    # all multiplied by the number of instructions.

    count = 1
    for cycle in cycles:
        count *= (len(cycle) - 1)
    count *= len(instructions)
    return count
            
def path_until_repeat(forks: dict, instuctrions: str, start: str) -> list:
    """What is the pattern of states from the start?"""
    # Start at the start
    position = start
    path = [position]
    # Follow the instructions
    while True:
        for inst in instructions:
            if inst == 'L':
                position = forks[position][0]
            elif inst == 'R':
                position = forks[position][1]
        # If we've seen this state before, we're done
        if position in path:
            return path
        path.append(position)

if __name__ == '__main__':
    instructions = ""
    forks = {}

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue

            # If line has no space, it's the LR instructions
            if ' ' not in line:
                instructions = line
                continue

            # Else, it's a fork in the road
            fork, left, right = parse_fork(line)
            forks[fork] = (left, right)

    print("Part 1:", steps_from_AAA_to_ZZZ(forks, instructions))
    print("Part 2:", steps_from_As_to_Zs(forks, instructions))