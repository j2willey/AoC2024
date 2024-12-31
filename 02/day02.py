
# This script is for Advent of Code 2024, Day 2, Part 1 and Part 2

import os

# Get the directory of the current script
def loaddata(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    with open(data_file_path) as f:
        lines = f.readlines()
        return lines


def safeLevels(reports):
    diffs = [ reports[i + 1] - reports[i] for i in range(len(reports) - 1) ]
    monotonic = (all(x > 0 for x in diffs) or all(x < 0 for x in diffs))
    return all([ 1 <= abs(num) <= 3 for num in diffs ]) and monotonic

def reviewReports(lines):
    safeReports = 0
    safeDampenedReports = 0

    for line in lines:
        reports = [ int(i) for i in line.split() ]
        if safeLevels(reports):
            safeReports += 1
        else:
            for i in range(len(reports)):
                creports = reports[:i] + reports[i+1:]
                if safeLevels(creports):
                    safeDampenedReports += 1
                    break
    return safeReports, safeDampenedReports

def day2Part1(filename = 'input.txt'):
    lines = loaddata(filename)
    safeReports, _ = reviewReports(lines)
    return safeReports, "Safe Reports"

def day2Part2(filename = 'input.txt'):
    lines = loaddata(filename)
    safeReports, safeDampenedReports = reviewReports(lines)
    return safeReports + safeDampenedReports, "All reports, incl Safe Dampened Reports"

if __name__ == '__main__':

    safeReports, description = day2Part1()

    print(f"Part 1: {safeReports}  # {description}")

    safeDampenedReports, description = day2Part2()
    print(f"Part 2: {safeReports + safeDampenedReports}  # {description}")



