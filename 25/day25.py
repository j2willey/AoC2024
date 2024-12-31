import os

def loadLocksAndKeys(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    locks = []
    keys = []

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    keylocksize = len(lines[0]) -1
    device = None
    tumblers = [-1] * keylocksize
    for line in lines:
        line = line.strip()
        if device == None and all([c == '#' for c in line]):
            device = 'lock'
            #continue
        if device == None and all([c == '.' for c in line]):
            device = 'key'
            #continue
        if device != None and line == '':
            if device == 'lock':
                locks.append(tumblers)
            else:
                keys.append(tumblers)
            tumblers = [-1] * keylocksize
            device = None
            continue
        for i, t in enumerate(line.strip()):
            if t == '#':
                tumblers[i] += 1
    if device != None:
        if device == 'lock':
            locks.append(tumblers)
        else:
            keys.append(tumblers)

    return locks, keys

def printlocksandkeys(locks, keys):
    print("Locks")
    for lock in locks:
        print(''.join([str(t) for t in lock]))
    print("\nKeys")
    for key in keys:
        print(''.join([str(t) for t in key]))


def possibleFits(locks, keys):
    possiblefits = 0
    maxt = 5
    for key in keys:
        for lock in locks:
            comb = [ (k + l) <= maxt for k, l in zip(key, lock)]
            if all(comb):
                possiblefits +=1
    return possiblefits

def day25Part1(filename = "input.txt"):
    locks, keys = loadLocksAndKeys(filename)
    return possibleFits(locks, keys), "Part 1: possible fits"

def day25Part2(filename = "input.txt"):
    return "*", "Part 2:  Completed LAST Challenge 8-)"

if __name__ == "__main__":
    print(day25Part1())
    print(day25Part2())

