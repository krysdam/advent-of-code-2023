def parse_record(record: str) -> tuple:
    """Parse a line of the puzzle input into (binary-record, [nums])."""
    record, nums = record.split()
    nums = [int(x) for x in nums.split(',')]
    return record, nums

def all_possible_records(length: int, nums: list, isfirst: bool = False) -> list:
    """Generate all possible records of the given length."""
    #print("Finding all possible for", length, nums)
    if length == 0:
        yield ""
        return
    if nums == []:
        yield "." * length
        return
    space_needed = sum(nums) + len(nums) - 1
    max_prefix = length - space_needed
    min_prefix = 0 if isfirst else 1
    for prefixlen in range(min_prefix, max_prefix + 1):
        prefix = '.' * prefixlen
        for record in all_possible_records(length - prefixlen - nums[0], nums[1:]):
            yield prefix + nums[0] * '#' + record

def is_consistent(record1: str, record2: str) -> bool:
    """Are the two records consistent?"""
    for c1, c2 in zip(record1, record2):
        # If either record is unsure, we're good
        if c1 == '?' or c2 == '?':
            continue
        # If they don't match, we're not good
        if c1 != c2:
            return False
    return True

def how_many_possibilities(record: str, nums: list) -> int:
    """How many ways can these nums describe this record?"""
    count = 0
    for possible_record in all_possible_records(len(record), nums, True):
    #    print(possible_record, is_consistent(record, possible_record))
        if is_consistent(record, possible_record):
            count += 1
    #print(count)
    return count



if __name__ == '__main__':
    records = []

    with open('example.txt', 'r') as f:
        for line in f:
            line = line.strip()

            records.append(parse_record(line))

    # Part 1: how many possibilities are there for each record?
    sum1 = 0
    for record, nums in records:
        sum1 += how_many_possibilities(record, nums)
        #print()
    print("Part 1:", sum1)

    # Part 2: each record becomes five of itself
    sum2 = 0
    for record, nums in records:
        record = '?'.join(record * 5)
        nums = nums * 5
        sum2 += how_many_possibilities(record, nums)
    print("Part 2:", sum2)