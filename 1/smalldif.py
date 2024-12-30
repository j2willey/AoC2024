import os
from collections import Counter

def loaddata(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)
    with open(data_file_path) as f:
        lines = f.readlines()
    return lines

def Day1Part1(lines):
    l1 = []
    l2 = []

    for line in lines:
        nums = line.split()
        l1.append(int(nums[0]))
        l2.append(int(nums[1]))

    l1.sort()
    l2.sort()

    #for i in range(5):  # len(l1)):
    #    print(l1[i], l2[i])

    return sum([abs(x-y) for x, y in zip(l1, l2)])


def day1Part2(lines):
    l1 = []
    l2 = []

    for line in lines:
        nums = line.split()
        l1.append(int(nums[0]))
        l2.append(int(nums[1]))

    l1.sort()
    l2.sort()
    l2counts = Counter(l2)

    simscore = 0

    for i in range(len(l1)):
        if l1[i] in l2counts:
            simscore +=  l2counts[l1[i]] * l1[i]
        #print(l1[i], l2[i])

    return simscore

if __name__ == '__main__':

    lines = loaddata('input.txt')

    part1 = Day1Part1(lines)
    print(f"Part 1: {part1}")

    simscore = day1Part2(lines)
    print(f"Part 2: {simscore}")
