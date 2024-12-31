import os
import copy
from collections import Counter
from itertools import permutations

def loaddata(data_file_path):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'input.txt')

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    antmap = []
    allnodes = []
    for line in lines:
        row = []
        allnodes.extend(line.strip('\n'))
        for l in line.strip():
            row.append(l)
        antmap.append(row)

    counts = Counter(allnodes)
    del counts['.']
    counts = { k: v for k, v in counts.items() if v > 1}

    return antmap, counts

def printmap(mp):
    m = len(mp[0])
    n = len(mp)
    print(f"Map {m}x{n}")
    print("____________")
    for row in mp:
        print(''.join(row))
    print("^^^^^^^^^^^^")


def getAllLocations(antmap, c):
    m, n = len(antmap[0]),  len(antmap)
    locations = []
    for i in range(n):
        for j in range(m):
            if antmap[i][j] == c:
                locations.append((i, j))
    return locations

antinodes = None

def day8Part1(filename = 'input.txt'):
    global antinodes
    antinodes = set()
    antmap, counts = loaddata(filename)
    m, n = len(antmap[0]),  len(antmap)
    itnamap = copy.deepcopy(antmap)
    for k in counts.keys():
        locations = getAllLocations(antmap, k)
        for p1, p2 in permutations(locations, 2):
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            a1 = p2[0] + dx, p2[1] + dy
            if 0 <= a1[0] < m and 0 <= a1[1] < n:
                antinodes.add(a1)
                itnamap[a1[0]][a1[1]] = '#'
            a2 = p1[0] - dx, p1[1] - dy
            if 0 <= a2[0] < m and 0 <= a2[1] < n:
                antinodes.add(a2)
                itnamap[a2[0]][a2[1]] = '#'
    return len(antinodes), "Part 1 Antinodes"

def day8Part2(filename = 'input.txt'):
    global antinodes
    if not antinodes:
        day8Part1()

    antmap, counts = loaddata(filename)
    m, n = len(antmap[0]),  len(antmap)
    itnamap = copy.deepcopy(antmap)
    for k in counts.keys():
        locations = getAllLocations(antmap, k)
        for p1, p2 in permutations(locations, 2):
            antinodes.add(p1)
            antinodes.add(p2)
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            a1 = p2[0] + dx, p2[1] + dy
            while 0 <= a1[0] < m and 0 <= a1[1] < n:
                antinodes.add(a1)
                itnamap[a1[0]][a1[1]] = '#'
                a1 = a1[0] + dx, a1[1] + dy
            a2 = p1[0] - dx, p1[1] - dy
            while 0 <= a2[0] < m and 0 <= a2[1] < n:
                antinodes.add(a2)
                itnamap[a2[0]][a2[1]] = '#'
                a2 = a2[0] - dx, a2[1] - dy

    return len(antinodes), "Part 2 Antinodes"

if __name__ == '__main__':
    anodes, desc1 = day8Part1()
    print(f"{desc1}:  {anodes}   ")
    anodes, desc2 = day8Part2()
    print(f"{desc2}:  {anodes}   ")

