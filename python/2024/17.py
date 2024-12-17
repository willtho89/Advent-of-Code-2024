from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class Computer:
    registers: Dict[str, int]
    program: List[int]
    ip: int = 0
    outputs: List[int] = field(default_factory=list)

    def get_combo_operand_value(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def adv(self, operand: int) -> None:
        """
        The adv instruction (opcode 0) performs division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then written to the A register.
        """
        denom_power = self.get_combo_operand_value(operand)
        denominator = 2 ** denom_power
        numerator = self.registers['A']
        result = numerator // denominator
        self.registers['A'] = result
        self.ip += 2

    def bxl(self, operand: int) -> None:
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
        the instruction's literal operand, then stores the result in register B.
        """
        value = operand
        self.registers['B'] ^= value
        self.ip += 2

    def bst(self, operand: int) -> None:
        """
        The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        """
        value = self.get_combo_operand_value(operand)
        self.registers['B'] = value % 8
        self.ip += 2

    def jnz(self, operand: int) -> None:
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero, it jumps by setting the instruction
        pointer to the value of its literal operand; if this instruction jumps,
        the instruction pointer is not increased by 2 after this instruction.
        """
        if self.registers['A'] != 0:
            self.ip = operand * 2
        else:
            self.ip += 2

    def bxc(self, operand: int) -> None:
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B.
        (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.registers['B'] ^= self.registers['C']
        self.ip += 2

    def out(self, operand: int) -> None:
        """
        The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
        then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        value = self.get_combo_operand_value(operand) % 8
        self.outputs.append(value)
        self.ip += 2

    def bdv(self, operand: int) -> None:
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction
        except that the result is stored in the B register.
        (The numerator is still read from the A register.)
        """
        denom_power = self.get_combo_operand_value(operand)
        denominator = 2 ** denom_power
        numerator = self.registers['A']
        result = numerator // denominator
        self.registers['B'] = result
        self.ip += 2

    def cdv(self, operand: int) -> None:
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction
        except that the result is stored in the C register.
        (The numerator is still read from the A register.)
        """
        denom_power = self.get_combo_operand_value(operand)
        denominator = 2 ** denom_power
        numerator = self.registers['A']
        result = numerator // denominator
        self.registers['C'] = result
        self.ip += 2

    def execute(self, opcode: int, operand: int) -> None:
        instruction_methods = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        method = instruction_methods.get(opcode)
        if method is None:
            raise ValueError(f"Invalid opcode: {opcode}")
        method(operand)

    def run(self) -> None:
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            self.execute(opcode, operand)
            if self.ip < 0 or self.ip > len(self.program):
                break  # Prevent infinite loops in case of incorrect jumps


with open('17.input', 'r') as file:
    lines = [line.strip() for line in file]
registers: Dict[str, int] = {}
program: List[int] = []
for line in lines:
    if line.startswith('Register'):
        parts = line.split(':')
        register_name = parts[0].split()[1]
        register_value = int(parts[1].strip())
        registers[register_name] = register_value
    elif line.startswith('Program'):
        program = [int(x) for x in line.split(':')[1].strip().split(',')]

# Part One
from time import perf_counter
p1_start = perf_counter()
computer = Computer(registers=registers.copy(), program=program)
computer.run()
output_string = ','.join(map(str, computer.outputs))
print(f"Part One: {output_string}")
p1_end = perf_counter()

# Part Two
p2_start = perf_counter()
print(f"Part Two: no idea yet")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:.2f}s")
