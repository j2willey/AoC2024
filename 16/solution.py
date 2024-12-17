import os
import copy
import heapq

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

def loadmap(data_file_path):
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


def updatemap(map, paths = set()):
    for p in paths:
        y, x = p
        map[y][x] = 'O'
    return map

def findSE(spot, map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == spot:
                return (i, j)
    return None


dir = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
left = {'>': '^', '<': 'v', '^': '<', 'v': '>'}
right = {'>': 'v', '<': '^', '^': '>', 'v': '<'}
reverse = {'>': '<', '<': '>', '^': 'v', 'v': '^'}

# return the cost of the shortest path from start to end.
def findShortestPath(map, start, startdir, end):
    visited = set()
    queue = [(start, startdir, 0)]
    while len(queue) > 0:
        start, direction, cost = queue.pop(0)
        if (start, direction) in visited:
            continue
        visited.add((start, direction))
        if start == end:
            return cost
        # move straight
        dy, dx = dir[direction]
        next = (start[0] + dy, start[1] + dx)
        if map[ next[0] ][ next[1] ] != '#':
            queue.append(( next, direction, cost + 1 ))
        # turn
        queue.append(( start, left[direction], cost + 1000) )
        queue.append(( start, right[direction], cost + 1000) )
        # sort the queue by cost
        queue = sorted(queue, key=lambda x: x[2])

# return the coordinates of all cells on all paths where cost == target.
def findAllShortestPaths(map, start, startdir, end, target):
    visited = {}
    paths = {start}
    turns, steps = target // 1000, target % 1000
    queue = [(0, start, startdir, {start})] # Use a priority queue (min-heap)
    heapq.heapify(queue)
    while queue:
        cost, loc, direction, thispath = heapq.heappop(queue)
        #print("cost, loc, direction, thispath", cost, loc, direction, thispath)
        if  ((loc, direction) in visited and visited[(loc, direction)] < cost) or (cost // 1000) > turns or cost % 1000 > steps:
            continue
        thispath.add(loc)
        visited[(loc, direction)] = cost
        visited[(loc, reverse[direction])] = cost
        if loc == end and cost == target:
            paths.update(thispath)
            continue
        # move straight
        dy, dx = dir[direction]
        next = (loc[0] + dy, loc[1] + dx)
        if map[next[0]][next[1]] != '#':
            heapq.heappush(queue, (cost + 1, next, direction, copy.deepcopy(thispath)))
        # turn
        heapq.heappush(queue, (cost + 1000, loc, left[direction], copy.deepcopy(thispath)))
        heapq.heappush(queue, (cost + 1000, loc, right[direction], copy.deepcopy(thispath)))
        # sort the queue by cost
    return paths


def findSolutions(filename):
    data_file_path = os.path.join(script_dir, filename)
    omap = loadmap(data_file_path)
    start = findSE('S', omap)
    startdir = '>'
    end = findSE('E', omap)
    #printmap()
    cost = findShortestPath(omap, start, startdir, end)
    #printmap()
    print("Part 1: Cost of shortest path is", cost)
    allpaths = findAllShortestPaths(omap, start, startdir, end, cost)
    #print("All paths", allpaths)
    omap = updatemap(omap, allpaths)
    #printmap(omap)
    print("Part 2: Number of cells in all shortest paths", len(allpaths))


print("\ntest.txt")
print("  expect Part 1: Cost = 7036\n         Part 2: best spots = 45")
findSolutions('test.txt')

print("\ntest2.txt")
print("  expect Part 1: Cost = 11048\n         Part 2: best spots = 64")
findSolutions('test2.txt')

print("\ninput.txt")
print("  expect Part 1: Cost = 93436\n         Part 2: best spots = 486")
findSolutions('input.txt')


