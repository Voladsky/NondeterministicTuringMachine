import enum
class NondeterministicTuringMachine:
    def __init__(self, Q, Sigma, q0, Space, F, Program, input_word):
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.Space = Space
        self.F = F
        self.Program = Program
        self.input_word = input_word
    
    def __init__(self, Q, Sigma, q0, Space, F):
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.Space = Space
        self.F = F

    class Direction(enum.Enum):
        L = -1
        R = 1

    def run_program(self):
        # Конфигурация хранится в кортеже (q, pos, tape)
        configs_list = []
        # Индекс текущей конфигурации в списке
        current_config_index = 0

        configs_list.append((self.q0, 0, self.input_word))
        
        while True:
            if current_config_index == len(configs_list):
                break
            
            (q, pos, tape) = configs_list[current_config_index]
            current_config_index += 1
            
            if q in self.F:
                print(tape[:pos] + f"(q{q})" + tape[pos:], ", Successful!")
                continue
            
            if (q, tape[pos]) not in self.Program:
                print(tape[:pos] + f"(q{q})" + tape[pos:], "Unsuccesful!", sep=", ")
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

if __name__ == "__main__":
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
