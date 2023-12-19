def parse_part(s: str) -> tuple:
    """Given a part, return its values."""
    for ch in '{xmas=}':
        s = s.replace(ch, '')
    values = s.split(',')
    values = tuple([int(val) for val in values])
    return values

def greater(x, y):
    return x > y

def less(x, y):
    return x < y

def parse_workflow(s: str):
    name, rules = s.split('{')
    rules = rules.replace('}', '')
    rules = rules.split(',')
    rule_tuples = []
    for rule in rules:
        parts = rule.split(':')
        next = parts[-1]
        if len(parts) == 1:
            rule_tuples.append((-1, -1, -1, next))
            continue
        parts = parts[0]
        if '>' in parts:
            parts = parts.split('>')
            op = greater
        else:
            parts = parts.split('<')
            op = less
        ind = 'xmas'.index(parts[0])
        val = int(parts[-1])
        rule_tuples.append((ind, op, val, next))
    def workflow(xmas: tuple):
        for ind, op, val, next in rule_tuples:
            if ind == -1:
                return next
            if op(xmas[ind], val):
                return next
    return name, workflow

if __name__ == '__main__':
    workflows = {}
    parts = []

    with open('input.txt', 'r') as f:
        on_workflow = True
        for line in f:
            line = line.strip()

            if line == '':
                on_workflow = False
                continue

            if on_workflow:
                name, workflow = parse_workflow(line)
                workflows[name] = workflow

            else:
                parts.append(parse_part(line))

    accepted = []
    for p in parts:
    #for p in ((x, m, a, s) for x in range(1, 4001) for m in range(1, 4001) for a in range(1, 4001) for s in range(1, 4001)):
        #if p[-1] == 1:
        #    print(p)
        workflow = 'in'
        while workflow not in 'AR':
            workflow = workflows[workflow](p)
        if workflow == 'A':
            accepted.append(p)

    print(accepted)
    score = 0
    for x, m, a, s in accepted:
        score += x + m + a + s

    print(score)