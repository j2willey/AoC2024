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

# with the path as an array, find all pairs of cells that are not 
# adjacent in the path or distance 1 apart in the path, and are a 
# distance of 2 apart in the map (i.e. there is a wall between them)
# return the array of pairs of cells that are cheats and the distance
# between them on the path
def findallcheats(map, path, mincheat = 0):
    pathset = { p: i for i, p in enumerate(path)}
    #print("Pathset:", pathset)
    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)    
    cheats = []

    def checkdir( y, x , dy, dx):
        cheat = (y + 2*dy, x + 2*dx)
        if cheat in path and map[y + dy][x + dx] == '#':
            #print("Cheat:", cheat, "Path:", pathset[cheat], "Path:", pathset[(y, x)])
            return pathset[cheat] -pathset[(y, x)] -2
        return 0 

    for i in range(len(path)):
        cheat = checkdir(path[i][0], path[i][1], left[0], left[1])
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i][0], path[i][1], right[0], right[1]) 
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i][0], path[i][1], up[0], up[1]) 
        if cheat >= mincheat:
                cheats.append(cheat)
        cheat = checkdir(path[i][0], path[i][1], down[0], down[1])  
        if cheat >= mincheat:
                cheats.append(cheat )

    return cheats

# Example usage
maze = loadmap('input.txt')
printmap(maze)
start, end = findstartandend(maze)
print("Start:", start, "End:", end)
path = findShortestPath(maze, start, end)
print("Shortest Path:", path)
print("length path:", len(path))

cheats = findallcheats(maze, path, 100)

countedCheats = Counter(cheats)
print ("Cheats:", countedCheats)
cheatsCounted = [(c,s) for s, c in countedCheats.items()]
cheatsCounted.sort(key = lambda x: x[1])
print ("Cheats:" , cheatsCounted)
print(f"cheats: {len(cheats)}")
# 14 save  2 picoseconds.
# 14 save  4 picoseconds.
#  2 save  6 picoseconds.
#  4 save  8 picoseconds.
#  2 save 10 picoseconds.
#  3 save 12 picoseconds.
#  1 save 20 picoseconds.
#  1 save 36 picoseconds.
#  1 save 38 picoseconds.
#  1 save 40 picoseconds.
#  1 save 64 picoseconds.