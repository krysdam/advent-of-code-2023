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

def how_many_possibilities_dynamic(record: str, nums: list) -> int:
    """How many ways can these nums describe this record?"""
    # Base cases.
    # If there's not enough room, there are zero possibilities.
    if len(record) < sum(nums) + len(nums) - 1:
        return 0
    # Assuming there's room, an empty record or empty nums means one possibility.
    if len(record) == 0:
        return 1
    if nums == []:
        return 1
    # Recursive case.
    # The only choice is: is the next character part of the next number?
    # If the next char is '.', then it isn't part of the number.
    if record[0] == '.':
        # Cut that char off and pass the buck.
        return how_many_possibilities_dynamic(record[1:], nums)
    # If the next char is '#', then it is part of the number.
    if record[0] == '#':
        # Reduce the first number by one.
        first_num = nums[0] - 1
        # If that number is used up, remove it,
        # and insist that the next char is '.' as a buffer.
        if first_num == 0:
            new_nums = nums[1:]
            if record[1:].startswith('#'):
                return 0
            else:
                return how_many_possibilities_dynamic(record[2:], new_nums)
        # If it's not used up, continue as normal.
        else:
            new_nums = [first_num] + nums[1:]
            return how_many_possibilities_dynamic(record[1:], new_nums)
    # If the next char is '?', then it could be either.
    if record[0] == '?':
        # Option 1: it's not part of the number.
        count1 = how_many_possibilities_dynamic('.' + record[1:], nums)
        # Option 2: it is part of the number.
        count2 = how_many_possibilities_dynamic('#' + record[1:], nums)
        return count1 + count2
    



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
        sum2 += how_many_possibilities_dynamic(record, nums)
    print("Part 2:", sum2)