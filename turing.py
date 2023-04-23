import enum
class NondeterministicTuringMachine:
    def __init__(self, Q, Sigma, q0, Space, F, Program):
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.Space = Space
        self.F = F
        self.Program = Program

    class Direction(enum.Enum):
        L = -1
        R = 1

    def run_program(self, input_word):
        configs_list = []
        current_config_index = 0

        configs_list.append((self.q0, 0, input_word))
        
        while True:
            if current_config_index == len(configs_list):
                break
            
            (q, pos, tape) = configs_list[current_config_index]
            current_config_index += 1
            
            if q in self.F:
                print(tape[:pos] + f"({q})" + tape[pos:], "Successful!", sep=", ")
                continue
            
            if (q, tape[pos]) not in self.Program:
                print(tape[:pos] + f"({q})" + tape[pos:], "Unsuccesful!", sep=", ")
                continue
            
            for (q_next, symbol, direction) in self.Program[(q, tape[pos])]:
                new_tape = tape[:pos] + symbol + tape[pos + 1:]
                new_pos = pos + direction.value
                if new_pos < 0:
                    new_tape = "B" + new_tape
                    pos = 0
                elif new_pos == len(new_tape):
                    new_tape += "B"
                configs_list.append((q_next, new_pos, new_tape))

def parse_program_to_blocks(path):
    lines = open(path, "r", encoding="UTF-8").readlines()
    blocks = {}
    cur_block_name = ""
    cur_block = ""
    for line in lines:
        if line[0] == "%":
            blocks[cur_block_name] = cur_block
            cur_block_name = line[1:].strip()
            cur_block = ""
        else:
            cur_block += line
    blocks.pop("")
    return blocks

def create_machine(path):
    blocks = parse_program_to_blocks(path)
    Q = { i for item in blocks["STATES"].split("\n") for i in item.split(";") }
    Sigma = { i for item in blocks["ALPHABET"].split("\n") for i in item.split(";") }
    #Gamma = { i for item in blocks["TAPE_ALPHABET"].split("\n") for i in item.split(";") }
    q0 = blocks["START_STATE"].strip()
    Space = blocks["SPACE"].strip()
    F = { i for item in blocks["FINAL_STATES"].split("\n") for i in item.split(";") }
    Program = {}
    for program_line in blocks["PROGRAM"].split("\n"):
        split = program_line.split(";")
        left = tuple(map(str.strip, split[0].strip("()").split(",")))
        right = { tuple(map(str.strip, item.strip("()").split(","))) for item in split[1:] }
        for item in right:
            (q, s, d) = item
            right.discard(item)
            if d == "R":
                right.add((q, s, NondeterministicTuringMachine.Direction.R))
            elif d == "L":
                right.add((q, s, NondeterministicTuringMachine.Direction.L))
        Program[left] = right
    Program.pop(("",))
    nmt = NondeterministicTuringMachine(Q, Sigma, q0, Space, F, Program)
    return nmt

nmt = create_machine("program.txt")
nmt.run_program("111")

'''if __name__ == "__main__":
    Q = {0, 1, 2, 3}
    Sigma = {"0", "1", "B"}
    q0 = 0
    Space = "B"
    F = {3}
    Program = {
        (0, "1"): {(0, "0", NondeterministicTuringMachine.Direction.R), (1, "0", NondeterministicTuringMachine.Direction.R)},
        (1, "0"): {(2, "1", NondeterministicTuringMachine.Direction.L)},
        (1, "B"): {(3, "B", NondeterministicTuringMachine.Direction.R)},
        (2, "0"): {(0, "0", NondeterministicTuringMachine.Direction.R)}
    }
    input_word = "111"

    nmt = NondeterministicTuringMachine(Q, Sigma, q0, Space, F)
    nmt.run_program()
'''