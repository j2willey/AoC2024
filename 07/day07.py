import os
import copy

def load_data(data_file_path):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'input.txt')

    calcs = []

    with open(data_file_path) as f:
        for line in f:
            calc, operands_str = line.strip().split(':')
            operands = operands_str.split()
            calcs.append((int(calc), [ int(o) for o in operands]))
    return calcs

def calibration(calc, operands):
    # print("calibration: ", calc, operands)
    for cops in range(2**(len(operands)-1)):
        valid = operands[0]
        strcalc = str(calc) + " ?= " + str(operands[0])
        for i in operands[1:]:
            if cops % 2 == 0:
                op = ' + '
                valid += i
            else:
                op = ' * '
                valid *= i
            strcalc += op + str(i)
            cops = cops >> 1
        #print(strcalc)
        if calc == valid:
            return calc
    return 0

def withconcatenation(calc, operands):
    # print("concatenation: ", calc, operands)
    newoperands = []
    for cops in range(3**(len(operands)-1)):
        res = operands[0]
        strcalc = str(res)
        for i in operands[1:]:
            if cops % 3 == 0:
                # concat the string
                res = int(str(res) + str(i))
                strcalc += " || " + str(i)
            elif cops % 3 == 1:
                # add the operand
                res +=i
                strcalc += " + " + str(i)
            else:
                res *= i
                strcalc += " * " + str(i)
            cops = cops // 3
        if res == calc:
            # print("valid concatenation: ", strcalc)
            return res
        # else :
            # print("   invalid concatenation: ", strcalc)
    return 0

__day7Part1 = None

def day7Part1(filename = "input.txt"):
    global __day7Part1
    calcs = load_data("input.txt")
    sum = 0
    reviewcalcs = []
    for calc, operands in calcs:
        tmpsum = calibration(calc, operands)
        if tmpsum:
            sum += tmpsum
            # print("valid calibration: ", calc, operands)
        else:
            reviewcalcs.append((calc, operands))

    # print("review calcs: ", reviewcalcs)

    __day7Part1 = (sum, reviewcalcs)
    return sum, "valid calibrations "

def day7Part2(filename = "input.txt"):
    global __day7Part1
    if not __day7Part1:
        day7Part1(filename)
    (sum, reviewcalcs) = __day7Part1

    consum = 0
    for calc, operands in reviewcalcs:
        consum += withconcatenation(calc, operands)
    return sum + consum, "valid calibrations w/ concatenations"

if __name__ == "__main__":
    part1, desc1 = day7Part1()
    part2, desc2 = day7Part2()
    print(f"part 1  {desc1}:  {part1}")
    print(f"part 2  {desc2}:  {part2}")

