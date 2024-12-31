import os
from collections import Counter

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


def day19Part1(filename):
    def isvalidpatternrec(pattern, towelset, maxtowel):
        if pattern == '':
            return True

        long = 0
        if maxtowel < len(pattern):
            long = maxtowel
        else:
            long = len(pattern)

        for i in range(long, 0, -1):
            if pattern[:i] in towels:
                if isvalidpatternrec(pattern[i:], towelset, maxtowel):
                    return True
        return False

    towels, patterns = loadtowelsandpatterns(filename)
    towelset = set(towels)
    maxtowel = max([len(towel) for towel in towelset])
    valid = 0
    for pattern in patterns:
        valid += isvalidpatternrec(pattern, towelset, maxtowel)
    return valid, f"Part 1:  valid patterns: "

def day19Part2(filename):
    memo = {}
    def countvalidpatternsrec(pattern, towelset, maxtowel):
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
                    thiscount = countvalidpatternsrec(pattern[i:], towelset, maxtowel)
                    memo[pattern[i:]] = thiscount
                    count += thiscount

        return count

    towels, patterns = loadtowelsandpatterns(filename)
    towelset = set(towels)
    maxtowel = max([len(towel) for towel in towelset])
    total = 0
    for pattern in patterns:
        total += countvalidpatternsrec(pattern, towelset, maxtowel)
    return total, f"Part 2:  total options: "


if __name__ == "__main__":
    print("Advent of Code 2019 - Day 19")
    print(day19Part1('input.txt'))
    print(day19Part2('input.txt'))
