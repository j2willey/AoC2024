import os
from collections import Counter

print("Advent of Code 2019 - Day 19\n\n")

def loadtowelsandpatterns(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)


    with open(data_file_path) as f:
        line = f.readline().strip()
        towels = [towel.strip() for towel in line.split(",") if towel.strip() != '']    
        f.readline()
        lines = f.readlines()
        patterns = [line.strip() for line in lines]
    return towels, patterns


towels, patterns = loadtowelsandpatterns('input.txt')
towelset = set(towels)
tcounts = Counter(towels)

lengths = [len(towel) for towel in towelset]
maxtowel = max(lengths)

def isvalidpatternrec(pattern, towelset):
    if pattern == '':
        return True

    long = 0
    if maxtowel < len(pattern):
        long = maxtowel
    else:
        long = len(pattern)

    for i in range(long, 0, -1):
        if pattern[:i] in towels:
            if isvalidpatternrec(pattern[i:], towelset):
                return True
    return False

memo = {}
def countvalidpatternsrec(pattern, towelset):
    if pattern == '':
        return 1

    long = 0
    if maxtowel < len(pattern):
        long = maxtowel
    else:
        long = len(pattern)

    count = 0
    for i in range(long, 0, -1):
        if pattern[:i] in towels:
            if pattern[i:] in memo:
                count += memo[pattern[i:]]
            else:
                thiscount = countvalidpatternsrec(pattern[i:], towelset)
                memo[pattern[i:]] = thiscount
                count += thiscount
        
    return count



#print(towels)

print("Part 1\n\n")
valid = 0
total = 0
for pattern in patterns:
    valid += isvalidpatternrec(pattern, towelset)
    total += countvalidpatternsrec(pattern, towelset)
print(f'valid patterns: {valid}')
print(f'total options: {total}')
print("\n\n")
