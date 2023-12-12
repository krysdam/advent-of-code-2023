def parse_record(conditions: str) -> tuple:
    """Parse a line of the puzzle input into (binary-record, [nums])."""
    conditions, nums = conditions.split()
    nums = tuple([int(x) for x in nums.split(',')])
    return conditions, nums

def expand_record(record: tuple, factor: int) -> tuple:
    """Expand a record and nums by a factor, per the problem."""
    conditions, nums = record
    conditions = '?'.join([conditions] * factor)
    nums = nums * factor
    return conditions, nums

# Memoize this.
# Otherwise, it keeps recalculating the same couple tail-cases.
import functools
@functools.lru_cache(maxsize=None)
def how_many_possibilities_dynamic(conditions: str, nums: tuple) -> int:
    """How many ways can these nums describe this record?"""
    # Base cases:
    # If there's not enough room for the numbers, there are no possibilities.
    if len(conditions) < sum(nums) + len(nums) - 1:
        return 0
    # If the record claims '#' but there are no nums, there are no possibilities.
    if '#' in conditions and nums == ():
        return 0
    # Assuming those are OK, an empty record or empty nums means one possibility.
    if len(conditions) == 0:
        return 1
    if nums == ():
        return 1
    # Recursive case.
    # The decision is: does the next number start at this character?
    ch = conditions[0]
    n = nums[0]
    # If the next char is a '.', then it can't start here.
    if ch == '.':
        return how_many_possibilities_dynamic(conditions[1:], nums)
    # If the next char is a '#', then it must start here.
    if ch == '#':
        # Forbid '.' inside the number.
        if '.' in conditions[:n]:
            return 0
        # Require a buffer after the number.
        if len(conditions) > n and conditions[n] == '#':
            return 0
        # Cut of the number and the buffer.
        return how_many_possibilities_dynamic(conditions[n+1:], nums[1:])
    # If the next char is a '?', then it can start here or not.
    if ch == '?':
        record_rest = conditions[1:]
        # Option 1: the '?' is really a '.'
        count1 = how_many_possibilities_dynamic('.' + record_rest, nums)
        # Option 2: the '?' is really a '#'
        count2 = how_many_possibilities_dynamic('#' + record_rest, nums)
        return count1 + count2

if __name__ == '__main__':
    records = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            records.append(parse_record(line))

    # Part 1: how many possibilities are there for each record?
    sum1 = 0
    for record in records:
        sum1 += how_many_possibilities_dynamic(*record)
    print("Part 1:", sum1)

    # Part 2: each record becomes five of itself
    multiplier = 5
    sum2 = 0
    for record in records:
        record = expand_record(record, multiplier)
        sum2 += how_many_possibilities_dynamic(*record)
    print("Part 2:", sum2)