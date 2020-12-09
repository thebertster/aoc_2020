class GameConsole:
    def __init__(self, program):
        self.acc = 0
        self.pc = 0
        self.program = []
        for instruction in program:
            parsed_instruction = instruction.split(' ')
            opcode = parsed_instruction[0]
            if opcode in ('nop', 'acc', 'jmp'):
                self.program.append((opcode, int(parsed_instruction[1])))

    def process_instruction(self, opcode, param):
        if opcode == 'nop':
            self.pc += 1
        elif opcode == 'jmp':
            self.pc += param
        elif opcode == 'acc':
            self.acc += param
            self.pc += 1

    def check_for_loop(self, mutator=None):
        if mutator:
            mutated_pc = mutator[0]
            opcode = self.program[mutated_pc][0]
            if opcode in mutator[1]:
                mutated_opcode = mutator[1][opcode]
            else:
                return True, None
        else:
            mutated_pc = None
            mutated_opcode = None

        self.pc = 0
        self.acc = 0
        pc_history = set()
        while True:
            instruction = self.program[self.pc]
            opcode = instruction[0]
            param = instruction[1]
            if self.pc == mutated_pc:
                opcode = mutated_opcode
            self.process_instruction(opcode, param)
            if self.pc in pc_history:
                return True, self.acc
            if self.pc == len(self.program):
                return False, self.acc
            pc_history.add(self.pc)
