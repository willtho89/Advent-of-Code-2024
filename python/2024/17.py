from dataclasses import dataclass, field
import sys
import re

@dataclass
class Computer:
    registers: dict[str, int]
    program: list[int]
    ip: int = 0
    outputs: list[int] = field(default_factory=list)
    max_outputs: int | None = None  # Added to control max outputs

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
        denom_power = self.get_combo_operand_value(operand)
        denominator = 2 ** denom_power
        numerator = self.registers['A']
        result = numerator // denominator
        self.registers['A'] = result
        self.ip += 2

    def bxl(self, operand: int) -> None:
        value = operand
        self.registers['B'] ^= value
        self.ip += 2

    def bst(self, operand: int) -> None:
        value = self.get_combo_operand_value(operand)
        self.registers['B'] = value % 8
        self.ip += 2

    def jnz(self, operand: int) -> None:
        if self.registers['A'] != 0:
            self.ip = operand * 2
        else:
            self.ip += 2

    def bxc(self, operand: int) -> None:
        self.registers['B'] ^= self.registers['C']
        self.ip += 2

    def out(self, operand: int) -> None:
        value = self.get_combo_operand_value(operand) % 8
        self.outputs.append(value)
        self.ip += 2

    def bdv(self, operand: int) -> None:
        denom_power = self.get_combo_operand_value(operand)
        denominator = 2 ** denom_power
        numerator = self.registers['A']
        result = numerator // denominator
        self.registers['B'] = result
        self.ip += 2

    def cdv(self, operand: int) -> None:
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

    def run(self, max_outputs: int = None) -> None:
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            self.execute(opcode, operand)
            if max_outputs is not None and len(self.outputs) >= max_outputs:
                break
            if self.ip < 0 or self.ip >= len(self.program):
                break


def expect(program: list[int], out: list[int], prev_a: int = 0) -> int | None:
    if not out:
        return prev_a
    for a in range(1 << 10):  # From 0 to 1023
        if (a >> 3) == (prev_a & 127):
            # Create a computer with registers A=a, B=0, C=0, and run the program
            computer = Computer(registers={'A': a, 'B': 0, 'C': 0}, program=program)
            computer.run(max_outputs=1)
            if computer.outputs and computer.outputs[0] == out[-1]:
                ret = expect(program, out[:-1], (prev_a << 3) | (a % 8))
                if ret is not None:
                    return ret
    return None




# Read input as in the original working.py
nums = list(map(int, re.findall(r'\d+', sys.stdin.read())))
regs = {'A': nums[0], 'B': nums[1], 'C': nums[2]}
program = nums[3:]

# Part One
from time import perf_counter
p1_start = perf_counter()
computer = Computer(registers=regs.copy(), program=program)
computer.run()
output_string = ','.join(map(str, computer.outputs))
print(f"Part One: {output_string}")
p1_end = perf_counter()

# Part Two
p2_start = perf_counter()
output_a = expect(program, program)
print(f"Part Two: {output_a}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:.2f}s")