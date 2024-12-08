import os
import copy
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'input.txt')

calcs = []

with open(data_file_path) as f:
    for line in f:
        calc, operands_str = line.strip().split(':')
        operands = operands_str.split()
        calcs.append((int(calc), [ int(o) for o in operands]))

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
consum = 0
for calc, operands in reviewcalcs:
    consum += withconcatenation(calc, operands)

#3749 Correct fpr part 1
print("part 1  valid calibrations:" , sum)
print("part 2  valid concatenations:", consum, sum + consum)