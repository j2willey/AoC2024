
# This script is for Advent of Code 2024, Day 2, Part 1 and Part 2

import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'reports.txt')

def safeLevels(reports):
    diffs = [ reports[i + 1] - reports[i] for i in range(len(reports) - 1) ]
    monotonic = (all(x > 0 for x in diffs) or all(x < 0 for x in diffs))
    return all([ 1 <= abs(num) <= 3 for num in diffs ]) and monotonic

safeReports = 0
safeDampenedReports = 0

with open(data_file_path) as f:
    for line in f:
        reports = [ int(i) for i in line.split() ]
        if safeLevels(reports):
            safeReports += 1
        else:
            for i in range(len(reports)):
                creports = reports[:i] + reports[i+1:]
                if safeLevels(creports):
                    safeDampenedReports += 1
                    break

print("safeReports:", safeReports)
print("safeDampenedReports:", safeReports + safeDampenedReports)
