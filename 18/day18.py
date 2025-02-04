import os

def loadcorruptbytes(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    corruptbytes = []
    updates = []

    with open(data_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if ',' in line:
                corruptbytes.append( tuple(int(i) for i in line.strip().split(",")) )
    return corruptbytes

def buildmap(corruptbytes, maptype = 'test', cap = None):
    size = 71
    mmap = []
    if maptype == 'test':
        size = 7
    for i in range(size):
        row = []
        for j in range(size):
            row.append('.')
        mmap.append(row)

    if cap:
        corruptbytes = corruptbytes[:cap]
    for byte in corruptbytes:
        #print(byte)
        mmap[byte[1]][byte[0]] = '#'
    return mmap

def corruptmap(byte, mmap):
    mmap[byte[1]][byte[0]] = '#'
    return mmap

def updatemapwithpath(mmap, path):
    for (x, y) in path:
        mmap[y][x] = '0'
    return mmap

def printbytes(corruptbytes):
    for byte in corruptbytes:
        print(byte)

def printmmap(map):
    print("____________")
    for row in map:
        print(''.join(row))
    print("^^^^^^^^^^^^")

# bfs seach for shortest path
# start at 0,0 and end at len(mmap) - 1, len(mmap) - 1
# keep track of the shortest path reach the end
# return number of steps to reach end
def findshortestpath(mmap):
    start = (0, 0)
    end = (len(mmap) - 1, len(mmap) - 1)
    queue = [[start, [start]]]
    visited = set()

    while queue:
        (loc, path) = queue.pop(0)
        x, y = loc

        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if nx < 0 or nx >= len(mmap) or ny < 0 or ny >= len(mmap) or mmap[ny][nx] == '#':
                continue
            queue.append([(nx, ny), path + [(nx, ny)]])
    return [(0,0)]

def day18Part1(filename = 'input.txt'):
    corruptbytes = loadcorruptbytes(filename)
    #printbytes(corruptbytes)
    mmap = buildmap(corruptbytes, 'nottest', 1024)
    #printmmap(mmap)
    path = findshortestpath(mmap)
    return len(path) - 1, "Part 1: shortest path:"

def day18Part2(filename = 'input.txt'):
    corruptbytes = loadcorruptbytes(filename)
    #printbytes(corruptbytes)
    mmap = buildmap(corruptbytes, 'nottest', 1024)
    for c in range(1024, len(corruptbytes)):
        byte = corruptbytes[c]
        mmap[byte[1]][byte[0]] = '#'
        #printmmap(mmap)
        path = findshortestpath(mmap)
        if path[-1] != (70, 70):
            # print(f" failed path for {c} bytes")
            # print(f"last corrupt byte: {corruptbytes[c]}")
            break
        else:
            # if c % 100 == 0:
            #     print(f" successful path for {c} bytes")
            continue
    return ",".join([ str(b) for b in corruptbytes[c]]), "Part 2: last corrupt byte:"

if __name__ == "__main__":
    print(day18Part1())
    print(day18Part2())

#print(f"shortest path: {len(path) - 1}")
#print(path)
#updatemapwithpath(mmap, path)
#printmmap(mmap)

