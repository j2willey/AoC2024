import os
import re

def loaddata(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    memory = None
    with open(data_file_path) as f:
        memory = f.read()
    return memory


def mul(a, b):
    return a * b

def day3Part1(filename = 'input.txt'):
    memory = loaddata(filename)
    memory1 = re.findall(r'mul\(\d{1,3},\d{1,3}\)', memory)
    return sum([eval(m) for m in memory1]), "sum"

def day3Part2(filename = 'input.txt'):
    memory = loaddata(filename)
    memory2 = re.findall(r'(don\'t\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\))', memory)

    sum2 = 0
    enabled = True
    for m in memory2:
        if m == "don't()":
            enabled = False
        elif m == "do()":
            enabled = True
        elif enabled:
            sum2 += eval(m)
    return sum2, "sum 2"


if __name__ == '__main__':

    part1, description = day3Part1()
    print(f"Part 1: {part1}  # {description}")

    part2, description = day3Part2()
    print(f"Part 2: {part2}  # {description}")
