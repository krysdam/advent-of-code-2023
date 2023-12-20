from collections import deque

class Module:
    """A module."""
    def __init__(self):
        pass

    def receive(self, origin: str, pulse: bool) -> bool:
        """Receive a signal, and emit a signal (bool, or None for no signal).)"""
        pass

class FlipFlop(Module):
    def __init__(self):
        self.state = False

    def receive(self, origin: str, pulse: bool) -> bool:
        # If the pulse is high, ignore it and don't emit.
        if pulse:
            return None
        # If the pulse is low, flip state and emit state.
        else:
            self.state = not self.state
            return self.state

class Conjunction(Module):
    def __init__(self, input_modules: list):
        # Remember last signal from each input module.
        self.memory = {module: False for module in input_modules}
        
    def receive(self, origin: str, pulse: bool) -> bool:
        # Remember the new signal.
        self.memory[origin] = pulse
        # If all are high, send low. Else, send high.
        return not all(self.memory.values())

class Broadcast(Module):
    def __init__(self):
        pass

    def receive(self, origin: str, pulse: bool) -> bool:
        # Forward the pulse.
        return pulse
    
def build_modules(modules_as_tuples: list, input_modules: dict) -> dict:
    modules = {}
    for variety, name, outputs in modules_as_tuples:
        if variety == '%':
            modules[name] = FlipFlop()
        elif variety == '&':
            modules[name] = Conjunction(input_modules[name])
        elif variety == 'b':
            modules[name] = Broadcast()
    return modules
    
def press_button(modules: list, output_modules: dict, target_module: str, target_signal: bool) -> tuple:
    """Press the button.
    
    Return the tuple:
    (# high signals sent,
     # low signals sent,
     bool: did the target module receive the target signal?)
    """
    highs_seen = 0
    lows_seen = 0
    target_signal_received = False

    # Press the button.
    lows_seen += 1
    to_do = deque([('button', False, 'broadcaster')])

    # Propogate all signals.
    while to_do:
        # Take the first signal.
        origin, signal, module = to_do.popleft()

        # If this is the target signal, record that.
        if module == target_module and signal == target_signal:
            target_signal_received = True

        # Ignore signals to modules we're ignoring.
        if module not in modules:
            continue
    
        # Poll this module for its response signal. Ignore None.
        resultant_signal = modules[module].receive(origin, signal)
        if resultant_signal is None:
            continue

        # Propogate the signal to all output modules.
        for dest in output_modules[module]:
            if resultant_signal:
                highs_seen += 1
            else:
                lows_seen += 1
            to_do.append((module, resultant_signal, dest))
    return highs_seen, lows_seen, target_signal_received


if __name__ == '__main__':
    # Read in each module as (variety, name, outputs).
    # For example, ('%', 'gr', ['rx', 'ry'])
    modules_as_tuples = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            name, outputs = line.split(' -> ')
            variety = name[0]
            name = name[1:]
            if variety == 'b':
                name = 'broadcaster'
            outputs = outputs.split(', ')
            modules_as_tuples.append((variety, name, outputs))

    # Some modules have no outputs,
    # so they aren't listed in the input,
    # so we don't have them in the list of modules.
    # This also means we don't know their variety (% or &).
    # That's fine, we actually want to ignore them.

    # Create dict for {module: [output modules]}.
    output_modules = {name: outputs for _, name, outputs in modules_as_tuples}

    # Create dict for {module: [input modules]}.
    input_modules = {name: [] for _, name, _ in modules_as_tuples}
    for variety, name, outputs in modules_as_tuples:
        for output in outputs:
            # Modules with no output modules aren't in that list of names.
            # But that's also fine. We won't need a list of their inputs.
            try:
                input_modules[output].append(name)
            except KeyError:
                #print(output, 'has no outputs.')
                pass

    # Part 1: Press 1000 times. How many low and high signals?
    modules1 = build_modules(modules_as_tuples, input_modules)
    total_highs = 0
    total_lows = 0
    for _ in range(1000):
        highs, lows, _ = press_button(modules1, output_modules, 'broadcaster', True)
        total_highs += highs
        total_lows += lows
    print("Part 1:", total_highs * total_lows)


    # Part 2: Press until 'rx' receives a low signal.

    # Here I exploit a nice feature of the data.
    # The circuit is four disjoint branches.
    # Each branch leads from the button, to a shared conjunction 'ql',
    # which is the only input to 'rx'.
    # So, we want to know when all four branches send a high signal to 'ql'.
    # Since the branches are disjoint,
    # we can look at each branch separately.

    # Find the four branches.
    branch_heads = output_modules['broadcaster']
    # Record how many presses each branch needs.
    press_needed_counts = []

    for branch_head in branch_heads:
        # Re-build the modules.
        modules2 = build_modules(modules_as_tuples, input_modules)

        # Find the dict of only the modules on this branch.
        relevant_modules = [branch_head]
        for name in relevant_modules:
            for output in output_modules[name]:
                # Ignore 'rx'.
                if output == 'rx':
                    continue
                if output not in relevant_modules:
                    relevant_modules.append(output)
        # Add broadcaster back in.
        relevant_modules.append('broadcaster')
        # This is the branch.
        branch = {name: modules2[name] for name in relevant_modules}

        # Press until the branch end receives a high signal.
        press = 0
        while True:
            press += 1
            if press % 10000 == 0:
                print("Attempting press", press)
            highs, lows, target_signal_received = press_button(branch, output_modules, 'ql', True)
            if target_signal_received:
                #print("Branch {}: {} presses.".format(branch_head, press))
                break
        press_needed_counts.append(press)

    # Another nice feature of the data:
    # Each branch loops exactly through (1 - p) low signals to 'ql',
    # then one high signal to 'ql',
    # and p is prime.
    # So, the total number of presses needed is the product of the four branches.
        
    product = 1
    for count in press_needed_counts:
        product *= count
    print("Part 2:", product)