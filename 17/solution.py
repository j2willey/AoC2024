import re
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'test.txt')
data_file_path = os.path.join(script_dir, 'input.txt')

# Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

registerA = 0
registerB = 0
registerC = 0
pc = 0
program = []

registerPattern = r"Register [A-C]: (\d+)"
programPattern = r"Program: ([\d,]+)"
match = re.match(registerPattern, lines[0])
if match: 
    registerA = int(match.group(1))
else:
    print('Error parsing register A')
match = re.match(registerPattern, lines[1])
if match: 
    registerB = int(match.group(1))
else:
    print('Error parsing register B')
match = re.match(registerPattern, lines[2])
if match: 
    registerC = int(match.group(1))
else:
    print('Error parsing register C')
match = re.match(programPattern, lines[4])
if match:
    program = list(map(int, match.group(1).split(','))) 
else:
    print('Error parsing program')

print(f'Register A: {registerA}')
print(f'Register B: {registerB}')
print(f'Register C: {registerC}')
print(f'Program: {program}')

# There are two types of operands; each instruction specifies the type of its operand. 
# The value of a literal operand is the operand itself. 
# For example, the value of the literal operand 7 is the number 7. 
# The value of a combo operand can be found as follows:

# Combo operands 0 through 3 represent literal values 0 through 3.
# Combo operand 4 represents the value of register A.
# Combo operand 5 represents the value of register B.
# Combo operand 6 represents the value of register C.
# Combo operand 7 is reserved and will not appear in valid programs.
# The eight instructions are as follows:
def combo(operand):
    if operand < 4:
        return operand
    elif operand == 4:
        return registerA
    elif operand == 5:
        return registerB
    elif operand == 6:
        return registerC
    else:
        print('Assertion error: invalid combo operand')
        return None

# The adv instruction (opcode 0) performs division. 
# The numerator is the value in the A register. 
# The denominator is found by raising 2 to the power of the instruction's combo operand. 
# (So, an operand of 2 would divide A by 4 (2^2); 
# an operand of 5 would divide A by 2^B.) 
# The result of the division operation is truncated to an integer and then written to the A register.
def adv(operand):
    registerA = registerA // (2 ** combo(operand))

# The bxl instruction (opcode 1) calculates the bitwise XOR of register B 
# and the instruction's literal operand, then stores the result in register B.
def bxl(literal):
    registerB = registerB ^ literal

# The bst instruction (opcode 2) calculates the value of its combo 
# operand modulo 8 (thereby keeping only its lowest 3 bits), 
# then writes that value to the B register.
def bst(operand):
    registerB = combo(operand) % 8

# The jnz instruction (opcode 3) does nothing if the A register is 0. 
# However, if the A register is not zero, it jumps by setting the 
# instruction pointer to the value of its literal operand; 
# if this instruction jumps, the instruction pointer is not increased 
# by 2 after this instruction.
def jnz(literal):
    if registerA != 0:
        pc = literal - 2

# The bxc instruction (opcode 4) calculates the bitwise XOR of register 
# B and register C, then stores the result in register B. 
# (For legacy reasons, this instruction reads an operand but ignores it.)
def bxc (operand):
    registerB = registerB ^ registerC

# The out instruction (opcode 5) calculates the value of its combo operand 
# modulo 8, then outputs that value. (If a program outputs multiple values, 
# they are separated by commas.)
def out(operand):
    print(f'{combo(operand)%8}', end=',')

# The bdv instruction (opcode 6) works exactly like the adv instruction 
# except that the result is stored in the B register. (The numerator is 
# still read from the A register.)
def bdv(operand):
    registerB = registerA // (2 ** combo(operand))

# The cdv instruction (opcode 7) works exactly like the adv instruction 
# except that the result is stored in the C register. 
# (The numerator is still read from the A register.)
def cdv(operand):
    registerC = registerA // (2 ** combo(operand))


#opc2fxn =  {0: 'adv', 1: 'bxl', 2: 'bst', 3: 'jnz', 4: 'bxc', 5: 'out', 6: 'bdv', 7: 'cdv'}
opc2fxn =  {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

print("# Part 1:  test.txt   expected output  4,6,3,5,6,3,5,2,1,0 ")


pc = 0
while pc < len(program):
    opcode = program[pc]
    operand = program[pc + 1]
    opc2fxn[opcode](operand)
    pc += 2

print('') 

# Part 1:  test.txt   expected output  4,6,3,5,6,3,5,2,1,0 






