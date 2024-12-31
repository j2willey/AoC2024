import os
import copy


def loaddata(filename = "input.txt"):
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
    return roommap

def printmap(thismap):
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

def findStart(roommap):
    for i in range(len(roommap)):
        if '^' in roommap[i]:
            return roommap[i].index('^'), i

# tracked through Part one to narrow search for loops

def patrolfwd(x, y, dx, dy, roommap):
    path = []
    m = len(roommap[0])
    n = len(roommap)
    stats = {'moves': 0,  'cells': 0,  'turns': 0}
    loopchk = set()
    visited = set()
    while True:
        if  not (0 <= x < m and  0 <= y < n):
            stats['result'] = "Exit"
            return stats, path  # Exit room
        if (x, y, dx, dy) in loopchk:
            stats['loopstart'] = path.index((x, y, dx, dy))
            stats['loopsize'] = len(path) - stats['loopstart']
            stats['result'] = "Loop"
            return stats, path  # Loop detected
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


def day6Part1(filename = "input.txt"):
    roommap = loaddata(filename)
    #printmap()
    m = len(roommap[0])
    n = len(roommap)
    startx, starty = findStart(roommap)
    #print(f"size:  {m:3} x {n:3}")
    #print(f"start: ({startx}, {starty})")
    stats, _ =  patrolfwd(startx, starty, 0, -1, roommap)
    #print("Part 1\nstats: ", stats)
    #printmap()
    #origmap = copy.deepcopy(roommap)
    return stats['cells'], "distinct positions visited"

def day6Part2(filename = "input.txt"):
    roommap = loaddata(filename)
    m = len(roommap[0])
    n = len(roommap)
    startx, starty = findStart(roommap)
    obstacles = set()
    _, p1path =  patrolfwd(startx, starty, 0, -1, roommap)

    for i, p in enumerate(p1path):
        # if i % 10 == 0:
        #     print(f"Path : {i:4} ", end = "\r", flush=True)
        (x, y, dx, dy) = p
        nx, ny = x + dx, y + dy
        if not (0 <= nx < m and 0 <= ny < n):
            #print(f"Exit at {nx:2},{ny:2}")
            break
        if (roommap[ny][nx] == '#'or (nx,ny) in obstacles or (nx,ny) == (startx, starty) ):
            continue
        roommap[ny][nx] = 'O'
        newstats, _ = patrolfwd(startx, starty, 0, -1, roommap)
        roommap[ny][nx] = '.'
        if newstats['result'] == "Loop":
            obstacles.add((nx,ny))

    return len(obstacles), "distinct loops detected"

    # Part 1: 5534 is correct for input.txt
    # Part 2: 2262 is correct for input.tx

if __name__ == "__main__":
    part1, desc1 = day6Part1("input.txt")
    print(f"Part 1:  {part1:4}  # {desc1}")
    part2, desc2 = day6Part2("input.txt")
    print(f"Part 2:  {part2:4}  # {desc2}")

