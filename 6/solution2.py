import os
import copy

# Get the directory of the current script
filename = "test.txt"
filename = "input.txt"
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, filename)

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

roommap = []
for line in lines:
    row = []
    for l in line.strip():
        row.append(l)
    roommap.append(row)

cleanmap = copy.deepcopy(roommap)

m = len(roommap[0])
n = len(roommap)

def printmap(thismap = roommap):
    print("____________")
    print("    x ", "".join([str(i%10) for i in range(len(thismap[0]))]))
    for i, row in enumerate(thismap):
        print(f"y{i:3}: ", ''.join(row))
    print("^^^^^^^^^^^^")

right = {
    (0, -1) : [1, 0],
    (1, 0) : [0, 1],
    (0, 1) : [-1, 0],
    (-1, 0) : [0, -1]
}

# for debugging, visualizing the path
dir = {
    (0, -1) : '^',
    (1, 0) : '>',
    (0, 1) : 'v',
    (-1, 0) : '<'
}

def findStart():
    for i in range(len(roommap)):
        if '^' in roommap[i]:
            return roommap[i].index('^'), i

# tracked through Part one to narrow search for loops
path = []

def patrolfwd(x, y, dx, dy):
    stats = {'moves': 0,  'cells': 0,  'turns': 0}
    loopchk = set()
    visited = set()
    while True:
        if  not (0 <= x < m and  0 <= y < n):
            stats['result'] = "Exit"
            return stats  # Exit room
        if (x, y, dx, dy) in loopchk:
            stats['loopstart'] = path.index((x, y, dx, dy))
            stats['loopsize'] = len(path) - stats['loopstart']
            stats['result'] = "Loop"
            return stats  # Loop detected
        if (x,y) not in visited:
            stats['cells'] += 1
        path.append((x, y, dx, dy))
        visited.add((x, y))
        loopchk.add((x, y, dx, dy))
        stats['moves'] += 1
        if roommap[y][x] == '.':  # not (x == startx and y == starty):
            roommap[y][x] = dir[(dx,dy)]  # only for debugging, visualizing the path
        else:
            roommap[y][x] = '+'
        nx, ny = x + dx, y + dy
        while 0 <= nx < m and 0 <= ny < n and (roommap[ny][nx] == '#' or roommap[ny][nx] == 'O'):
            dx, dy = right[(dx, dy)]
            nx, ny = x + dx, y + dy
            path.append((x, y, dx, dy))
            stats['turns'] += 1
        x += dx
        y += dy


#printmap()
startx, starty = findStart()
print(f"size:  {m:3} x {n:3}")
print(f"start: ({startx}, {starty})")
stats =  patrolfwd(startx, starty, 0, -1)
print("Part 1\nstats: ", stats)
#printmap()
origmap = copy.deepcopy(roommap)


obstacles = set()
p1path = path
# for p in p1path:
#     (x, y, dx, dy) = p
    # print(f"({x}, {y})")
#print(path)

for i, p in enumerate(p1path):
    #if i % 1000 == 0:
    #    print(f"Path : {i:4} ", end = "\r", flush=True)
    (x, y, dx, dy) = p
    nx, ny = x + dx, y + dy
    if not (0 <= nx < m and 0 <= ny < n):
        print(f"Exit at {nx:2},{ny:2}")
        break
    if (roommap[ny][nx] == '#'or (nx,ny) in obstacles or (nx,ny) == (startx, starty) ):
        continue
    roommap[ny][nx] = 'O'
    path = []
    newstats = patrolfwd(startx, starty, 0, -1)
    roommap[ny][nx] = '.'
    if newstats['result'] == "Loop":
        obstacles.add((nx,ny))

# for o in sorted(obstacles):
#     origmap[o[1]][o[0]] = 'O'
#     print(f"{o}")
# printmap(origmap)

# Part 1: 5534 is correct for input.txt
# Part 2: 2262 is correct for input.txt
if filename == "test.txt":
    print("test.txt:   part 1     41\n            part 2     6")
else:
    print("input.txt:  part 1   5534    part 2   2262")
print("")
print(f"p1 distinct positions: {stats['cells']:4}         moves: {stats['moves']}  turns: {stats['turns']}")

print("p2 distinct loops: ", len(obstacles))
