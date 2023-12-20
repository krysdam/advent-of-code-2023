from collections import deque

class Module:
    def __init__(self):
        pass

    def receive(self, origin: str, pulse: bool) -> bool:
        pass


class FlipFlop(Module):
    def __init__(self):
        self.state = False

    def receive(self, origin: str, pulse: bool) -> bool:
        if pulse == False:
            self.state = not self.state
            return self.state
        else:
            return None


class Conjunction(Module):
    def __init__(self, input_modules: list):
        self.memory = {module: False for module in input_modules}
        
    def receive(self, origin: str, pulse: bool) -> bool:
        self.memory[origin] = pulse
        # If all are high, send low. Else, send high.
        return not all(self.memory.values())
    

class Broadcast(Module):
    def __init__(self):
        pass

    def receive(self, origin: str, pulse: bool) -> bool:
        return pulse



if __name__ == '__main__':
    modules_as_tuples = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            name, outputs = line.split(' -> ')
            variety = name[0]
            name = name[1:]
            outputs = outputs.split(', ')
            #print(variety, name, outputs)
            modules_as_tuples.append((variety, name, outputs))


    output_modules = {name: outputs for _, name, outputs in modules_as_tuples}
    input_modules = {name: [] for _, name, _ in modules_as_tuples}
    
    for variety, name, outputs in modules_as_tuples:
        #print(variety, name, outputs)
        for output in outputs:
            try:
                input_modules[output].append(name)
            # Some modules may have no outputs,
            # so they won't be in the dict.
            # That's fine, we want to ignore them.
            except KeyError:
                print(output, 'has no outputs.')
                pass

    modules = {}
    for variety, name, outputs in modules_as_tuples:
        if variety == '%':
            modules[name] = FlipFlop()
        elif variety == '&':
            modules[name] = Conjunction(input_modules[name])
        elif variety == 'b':
            modules[name] = Broadcast()

    START = 'gr'
    #END = 'ql'

    relevant_modules = [START]
    for name in relevant_modules:
        for output in output_modules[name]:
            if output == 'rx':
                print(name)
                END = name
                continue
            if output not in relevant_modules:
                relevant_modules.append(output)
    relevant_modules.append('roadcaster')
    modules = {name: modules[name] for name in relevant_modules}

    highs_seen = 0
    lows_seen = 0

    press = 0
    while True:
        press += 1
        if press % 10000 == 0:
            print("Attempting press", press)
    #for press in range(1000):
        lows_seen += 1
        to_do = deque([('button', False, 'roadcaster')])

        while to_do:
            origin, signal, module = to_do.popleft()
            #print(origin, ['low', 'high'][signal], module)
            # Again, ignore signals to modules with no outputs.
            #if module == 'rx' and signal == False:
            #    print('Presses:', press)
            #    exit()
            if module == END and signal == True:
                print('Presses:', press)
                exit()
            if module not in modules:
                continue
            resultant_signal = modules[module].receive(origin, signal)
            if resultant_signal is None:
                continue

            for dest in output_modules[module]:
                if resultant_signal:
                    highs_seen += 1
                else:
                    lows_seen += 1
                to_do.append((module, resultant_signal, dest))


    print(highs_seen, lows_seen)
    print(highs_seen * lows_seen)