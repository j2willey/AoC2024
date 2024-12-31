import re
import os
import logging

registerA = 0
registerB = 0
registerC = 0
pc = 0
program = []
output  = []
breakpoint = False

def bootstrap(filename):
    global pc, registerA, registerB, registerC, program, output
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    registerA = 0
    registerB = 0
    registerC = 0
    pc = 0
    program = []
    output = []

    registerPattern = r"Register [A-C]: (\d+)"
    programPattern = r"Program: ([\d,]+)"
    match = re.match(registerPattern, lines[0])
    if match:
        registerA = int(match.group(1))
    else:
        logging.warning('Error parsing register A')
    match = re.match(registerPattern, lines[1])
    if match:
        registerB = int(match.group(1))
    else:
        logging.warning('Error parsing register B')
    match = re.match(registerPattern, lines[2])
    if match:
        registerC = int(match.group(1))
    else:
        logging.warning('Error parsing register C')
    match = re.match(programPattern, lines[4])
    if match:
        program = list(map(int, match.group(1).split(',')))
    else:
        logging.warning('Error parsing program')

    logging.debug(f'Register A: {registerA}   B: {registerB}   C: {registerC}')
    logging.debug(f'Program: {program}')
    return program, registerA, registerB, registerC

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
    global registerA, registerB, registerC
    if operand < 4:
        return operand
    elif operand == 4:
        return registerA
    elif operand == 5:
        return registerB
    elif operand == 6:
        return registerC
    else:
        logging.critical('Assertion error: invalid combo operand')
        return None

# The adv instruction (opcode 0) performs division.
# The numerator is the value in the A register.
# The denominator is found by raising 2 to the power of the instruction's combo operand.
# (So, an operand of 2 would divide A by 4 (2^2);
# an operand of 5 would divide A by 2^B.)
# The result of the division operation is truncated to an integer and then written to the A register.
def adv(operand):
    global pc, registerA, registerB, registerC, output, breakpoint
    registerA = registerA // (2 ** combo(operand))

# The bxl instruction (opcode 1) calculates the bitwise XOR of register B
# and the instruction's literal operand, then stores the result in register B.
def bxl(literal):
    global pc, registerA, registerB, registerC, output, breakpoint
    #registerB =  (registerB // 8) * 8 & (registerB % 8) ^ literal
    registerB =  registerB ^ literal

# The bst instruction (opcode 2) calculates the value of its combo
# operand modulo 8 (thereby keeping only its lowest 3 bits),
# then writes that value to the B register.
def bst(operand):
    global pc, registerA, registerB, registerC, output, breakpoint
    registerB = combo(operand) % 8

# The jnz instruction (opcode 3) does nothing if the A register is 0.
# However, if the A register is not zero, it jumps by setting the
# instruction pointer to the value of its literal operand;
# if this instruction jumps, the instruction pointer is not increased
# by 2 after this instruction.
def jnz(literal):
    global pc, registerA, registerB, registerC, output, breakpoint
    if registerA != 0 and breakpoint == False:
        pc = literal - 2

# The bxc instruction (opcode 4) calculates the bitwise XOR of register
# B and register C, then stores the result in register B.
# (For legacy reasons, this instruction reads an operand but ignores it.)
def bxc (operand):
    global pc, registerA, registerB, registerC, output, breakpoint
    registerB = registerB ^ registerC
    #registerB = (((registerB | registerC) // 8) * 8) + (registerB ^ registerC) % 8

# The out instruction (opcode 5) calculates the value of its combo operand
# modulo 8, then outputs that value. (If a program outputs multiple values,
# they are separated by commas.)
def out(operand):
    global pc, registerA, registerB, registerC, output, breakpoint
    output.append(f'{combo(operand)%8}')

# OPCODE 6 is not used in part 1 or part 2
# ======================================================================
# The bdv instruction (opcode 6) works exactly like the adv instruction
# except that the result is stored in the B register. (The numerator is
# still read from the A register.)
    # def bdv(operand):
    #     global pc, registerA, registerB, registerC
    #     registerB = registerA // (2 ** combo(operand))

# The cdv instruction (opcode 7) works exactly like the adv instruction
# except that the result is stored in the C register.
# (The numerator is still read from the A register.)
def cdv(operand):
    global pc, registerA, registerB, registerC
    registerC = registerA // (2 ** combo(operand))


#opc2fxn =  {0: 'adv', 1: 'bxl', 2: 'bst', 3: 'jnz', 4: 'bxc', 5: 'out', 6: 'bdv', 7: 'cdv'}
opc2fxn =  {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: 'bdv', 7: cdv}

def reset_cpu():
    global pc, registerA, registerB, registerC, output
    registerA = 0
    registerB = 0
    registerC = 0
    pc = 0
    output = []

def dump_cpu():
    global pc, registerA, registerB, registerC, output
    logging.debug(f"   CPU State:   registerA: {registerA}  B: {registerB}  C: {registerC}")
    logging.debug(f"                program: {program}")
    logging.debug(f"                pc = {pc}    output: {output}")


def run_program(program):
    global pc, registerA, registerB, registerC, output, breakpoint
    #dump_cpu()
    while pc < len(program):
        logging.debug(f'pc: {pc}  program[pc]: {program[pc]} function: {opc2fxn[program[pc]]}')
        logging.debug(f'rA: {registerA}  rB: {registerB}  rC: {registerC}')
        opcode = program[pc]
        operand = program[pc + 1]
        opc2fxn[opcode](operand)
        pc += 2
    logging.debug(f" output > {','.join(output)}")
    #dump_cpu()

def find_initial_registerA(rA, rB, start = 0):
    global program, registerA, registerB, registerC, pc, output, breakpoint
    log = []
    logging.debug(f'  find_initial_registerA(rA: {rA} rB: {rB})')
    for r3A in range(start, 2048):
        try_regA = (rA * 8) + r3A
        if try_regA == 0:
            continue
        log.append(f'{try_regA} = ({rA} * 8) + {r3A}  ')
        reset_cpu()
        registerA = try_regA
        logging.info(f'   checking if registerA: {registerA}  => rB: {rB}')
        breakpoint = True
        run_program(program)
        breakpoint = False

        #if rB == registerB:
        if rB == registerB % 8:
            return try_regA, r3A
        log.append( f'  tried regA {try_regA} => regA: {registerA}   regB: {registerB}  output: {output}    looking for rB: {rB}\n')
    logging.debug(f'  No initial registerA found\n{"".join(log)}')
    return None

def day17Part1TestCases(filename):
    logging.info(f"\n--------\n# Part 1:  test.txt")
    bootstrap('test.txt')
    logging.info(f" expect > 4,6,3,5,6,3,5,2,1,0 ")
    run_program(program)
    logging.info(f" output > {','.join(output)}")
    return ','.join(output), "Day 17 Part 1 test case1. Expect > 4,6,3,5,6,3,5,2,1,0 "

def day17Part1TestCase2(filename):
    logging.info(f"\n--------\n## Part 1:  test.txt + regA = 2024")
    reset_cpu()
    registerA = 2024
    logging.info(f" expect > 4,2,5,6,7,7,7,7,3,1,0 ")
    run_program(program)
    logging.info(f" output >  {','.join(output)}")
    return ','.join(output), "Day 17 Part 1 test case2. Expect > 4,2,5,6,7,7,7,7,3,1,0 "

def day17Part1(filename):
    logging.info(f"\n--------\n# Part 1:  input.txt")
    bootstrap('input.txt')
    logging.info(f" expect=> 7,1,5,2,4,0,7,6,1 ")
    run_program(program)
    logging.info(f" output >  {','.join(output)}")
    return ','.join(output), "Day 17 Part 1"

def day17Part2TestCase1(filename):
    logging.info(f"\n--------\n## Part 2:  test2.txt")
    logging.info('test2.txt')
    logging.info(f" expect=> {",".join([str(i) for i in program])} ")
    run_program(program)
    logging.info(f" output > {','.join(output)}")
    return ','.join(output), f"Day 17 Part 2 test case1. Expect > {",".join([str(i) for i in program])} "

def day17Part2(filename):
    global pc, registerA, registerB, registerC, output, breakpoint
    logging.info("\n=====================================")
    logging.info(f"\n--------\n## Part 2:  input.txt")
    bootstrap('input.txt')
    save_program = list(program)
    program_reversed = save_program[::-1]

    regA = 0
    for i, rB in enumerate(program_reversed):
        r3A = 0

        expect = [str(p) for p in program[len(program)-1 - i:]]

        regAbase = regA
        while r3A < 2048:
            reset_cpu()
            logging.info(f"expected state: regA: {regA}  rB: {rB}")
            regA, r3A = find_initial_registerA(regA, rB, r3A)

            reset_cpu()
            registerA = regA
            logging.info(f" expect=> {",".join(expect)} ")
            run_program(program)
            result = (f" output > {','.join(output)}")
            if expect == output:
                logging.info(f"{result}   Success!!!")
                break
            else:
                logging.info(f"{result}   Failed:"  )
                logging.info(f"   regA: {regA}  rB: {rB}  registerB: {registerB}  output: {output}")
                regA = regAbase
                r3A += 1
        logging.info(f' regA: {regA}  rB: {rB}  r3A: {r3A}  output: {output}')
        logging.info("    | loop |")
    return regA, f"Part 2:  RegA:  returns {','.join(output)}"

    # FINALLY!!!!!!
    #  find_initial_registerA(rA: 4652784244670 rB: 2)
    #  expect=> 2,4,1,2,7,5,1,3,4,4,5,5,0,3,3,0
    #  output > 2,4,1,2,7,5,1,3,4,4,5,5,0,3,3,0   Success!!!
    #  regA: 37222273957364  rB: 2  r3A: 4  output: ['2', '4', '1', '2', '7', '5', '1', '3', '4', '4', '5', '5', '0', '3', '3', '0']
    #        ^^^^^^^^^^^^^^

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')
    #print(day17Part1TestCases('test.txt'))
    #print(day17Part1TestCase2('test.txt'))
    print(day17Part1('input.txt'))
    #print(day17Part2TestCase1('test2.txt'))
    print(day17Part2('input.txt'))



