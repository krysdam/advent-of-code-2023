def parse_record(record: str) -> tuple:
    """Parse a line of the puzzle input into (binary-record, [nums])."""
    record, nums = record.split()
    nums = [int(x) for x in nums.split(',')]
    return record, nums

# Memoize this.
# Otherwise, it keeps recalculating the same couple tail-cases.
import functools
@functools.lru_cache(maxsize=None)
def how_many_possibilities_dynamic(record: str, nums: tuple) -> int:
    """How many ways can these nums describe this record?"""
    # Base cases:
    # If there's not enough room for the numbers, there are no possibilities.
    if len(record) < sum(nums) + len(nums) - 1:
        return 0
    # If the record claims '#' but there are no nums, there are no possibilities.
    if '#' in record and nums == ():
        return 0
    # Assuming those are OK, an empty record or empty nums means one possibility.
    if len(record) == 0:
        return 1
    if nums == ():
        return 1
    # Recursive case.
    # The decision is: does the next number start at this character?
    ch = record[0]
    n = nums[0]
    # If the next char is a '.', then it can't start here.
    if ch == '.':
        return how_many_possibilities_dynamic(record[1:], nums)
    # If the next char is a '#', then it must start here.
    if ch == '#':
        # Also, the next n chars must not be '.'
        if '.' in record[:n]:
            return 0
        # Furthermore, the char after the number must be a buffer (not #)
        if len(record) > n and record[n] == '#':
            return 0
        # Cut off the buffer while we're at it.
        return how_many_possibilities_dynamic(record[n+1:], nums[1:])
    # If the next char is a '?', that's basically either '.' or '#'
    if ch == '?':
        record_rest = record[1:]
        # Option 1: the ? is really a .
        count1 = how_many_possibilities_dynamic(record_rest, nums)
        # Option 2: the ? is really a #
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
    for record, nums in records:
        sum1 += how_many_possibilities_dynamic(record, tuple(nums))
        #print()
    print("Part 1:", sum1)

    # Part 2: each record becomes five of itself
    multiplier = 5
    sum2 = 0
    records = sorted(records, key=lambda x: x[0].count('?'))
    new_records = []
    for record, nums in records:
        while '..' in record:
            record = record.replace('..', '.')
        new_records.append((record, nums))
    records = new_records
    for i, (record, nums) in enumerate(records):
        print(i, i / len(records), record, nums)
        record = '?'.join([record] * multiplier)
        nums = nums * multiplier
        sum2 += how_many_possibilities_dynamic(record, tuple(nums))
    print("Part 2:", sum2)