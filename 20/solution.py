import os
from collections import deque

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

# with the path as an array, find all pairs of cells that are not 
# adjacent in the path or distance 1 apart in the path, and are a 
# distance of 2 apart in the map (i.e. there is a wall between them)
# return the array of pairs of cells that are cheats and the distance
# between them on the path
def findallcheats(map, path):
    cheats = []
    for i in range(len(path)):
        for j in range(i+2, len(path)):
            if abs(path[i][0] - path[j][0]) + abs(path[i][1] - path[j][1]) == 2:
                if map[path[i][0]][path[j][1]] == '#' and map[path[j][0]][path[i][1]] == '#':
                    cheats.append((path[i], path[j], j-i))
    return cheats

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

# Example usage
maze = loadmap('test.txt')
printmap(maze)
start, end = findstartandend(maze)
print("Start:", start, "End:", end)
path = findShortestPath(maze, start, end)
print("Shortest Path:", path)
cheats = findallcheats(maze, path)

print ("Cheats:")

for cheat in cheats:
    print("Cheat:", cheat)