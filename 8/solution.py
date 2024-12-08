import os
import copy
from collections import Counter
from itertools import permutations

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
print("counts:", counts)
del counts['.']
counts = { k: v for k, v in counts.items() if v > 1}
print("counts:", counts)

m = len(antmap[0])
n = len(antmap)

def printmap(mp = antmap):
    print(f"Map {m}x{n}")
    print("____________")
    for row in mp:
        print(''.join(row))
    print("^^^^^^^^^^^^")

printmap()
itnamap = copy.deepcopy(antmap)

def getAllLocations(c):
    locations = []
    for i in range(n):
        for j in range(m):
            # print(antmap[i][j], end = "")
            if antmap[i][j] == c:
                locations.append((i, j))
        # print()
    print(f"Locations for {c}: {locations}")
    return locations

antinodes = set()

def part1():
    for k in counts.keys():
        # print(f"Processing {k}")
        locations = getAllLocations(k)
        #print(f"{k}:  { locations}")
        for p1, p2 in permutations(locations, 2):
            # print(f"Checking for antinodes {k}  {p1} {p2}")
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            a1 = p2[0] + dx, p2[1] + dy
            if 0 <= a1[0] < m and 0 <= a1[1] < n:
                antinodes.add(a1)
                itnamap[a1[0]][a1[1]] = '#'
            a2 = p1[0] - dx, p1[1] - dy
            if 0 <= a2[0] < m and 0 <= a2[1] < n:
                antinodes.add(a2)
                itnamap[a2[0]][a2[1]] = '#'

def part2():
    for k in counts.keys():
        # print(f"Processing {k}")
        locations = getAllLocations(k)
        #print(f"{k}:  { locations}")
        for p1, p2 in permutations(locations, 2):
            # print(f"Checking for antinodes {k}  {p1} {p2}")
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


part1()
#printmap(itnamap)
print(f"part 1 Antinodes:  {len(antinodes)}   ", antinodes)
part2()
#printmap(itnamap)
print(f"part 2 Antinodes:  {len(antinodes)}   ", antinodes)