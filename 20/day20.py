import os
from collections import deque, Counter

def loadmap(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    omap = []
    for line in lines:
        row = []
        for l in line.strip():
            row.append(l)
        omap.append(row)
    return omap

def printmap(map):
    print("____________")
    for row in map:
        print(''.join(row))
    print("^^^^^^^^^^^^")

def findstartandend(map):
    start = None
    end = None
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'S':
                start = (i, j)
            if map[i][j] == 'E':
                end = (i, j)
    return start, end

# find shortest path from start to end
# use bfs to find shortest path
def findShortestPath(map, start, end):
    rows, cols = len(map), len(map[0])
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (current, path) = queue.popleft()
        if current == end:
            return path

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            if 0 <= next_row < rows and 0 <= next_col < cols and map[next_row][next_col] != '#' and (next_row, next_col) not in visited:
                queue.append(((next_row, next_col), path + [(next_row, next_col)]))
                visited.add((next_row, next_col))

    return None

# original Part 1 implementation
def findallcheatsof2(map, path, mincheat = 0):
    pathset = { p: i for i, p in enumerate(path)}
    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)
    cheats = []

    def checkdir( position , direction):
        y, x = position
        dy, dx = direction
        cheat = (y + 2*dy, x + 2*dx)
        if cheat in path:
            return pathset[cheat] - pathset[(y, x)] - 2
        return 0

    for i in range(len(path)):
        cheat = checkdir(path[i], left)
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i], right)
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i], up)
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i], down)
        if cheat >= mincheat:
                cheats.append(cheat )

    return cheats

def findallcheatsofn(map, path, maxcheat, mincheat = 0):
    maxcheat = maxcheat + 1
    pathset = { p: i for i, p in enumerate(path)}
    #print("Pathset:", pathset)
    cheats = []

    def checkdir( pos , dy, dx):
        y, x = pos
        cheat = (y + dy, x + dx)
        if cheat in path:
            return pathset[cheat] - pathset[pos] - abs(dy) - abs(dx)
        return 0

    for i in range(len(path) - 1):
        for dx in range(maxcheat ):
            for dy in range(maxcheat - dx):
                if dx + dy <= 1 or (dx == 1 and dy == 1):
                    continue
                #print(f'  path[{i}] = {path[i]}, dx = {dx}, dy = {dy}')
                cheat = checkdir(path[i], dy, dx)
                if cheat >= mincheat:
                    cheats.append(cheat)
                if dx > 0:
                    cheat = checkdir(path[i], dy, -dx)
                    if cheat >= mincheat:
                        cheats.append(cheat)
                if dy > 0:
                    cheat = checkdir(path[i], -dy, dx)
                    if cheat >= mincheat:
                        cheats.append(cheat)
                if dx > 0 and dy > 0:
                    cheat = checkdir(path[i], -dy, -dx)
                    if cheat >= mincheat:
                        cheats.append(cheat )
    return cheats

def day20Part1(filename):
    maze = loadmap(filename)
    start, end = findstartandend(maze)
    # print("Start:", start, "End:", end)
    path = findShortestPath(maze, start, end)
    # First implementation for Part 1
    #cheats = findallcheatsof2(maze, path, 2)
    # reimplementation for Part 2 also solving Part 1
    cheats = findallcheatsofn(maze, path, 2, 100)
    # print("length path:", len(path))
    return len(cheats), f"Part 1:  Cheats: "

def day20Part2(filename):
    maze = loadmap(filename)
    start, end = findstartandend(maze)
    path = findShortestPath(maze, start, end)
    # print("Part 2: Cheats of 20 upto picoseconds")
    minsave = 100
    cheats = findallcheatsofn(maze, path, 20, minsave)

    # print(f"cheats: {len(cheats)} saving more than {minsave} picoseconds" )

    # Part 2  cheats: 1033983 saving more than 100 picoseconds
    return len(cheats), f"Part 2:  Cheats: "

if __name__ == "__main__":
    print("Advent of Code 2020 - Day 20")
    print(day20Part1('input.txt'))
    print(day20Part2('input.txt'))