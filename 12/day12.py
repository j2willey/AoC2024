import os


def loaddata(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'test.txt')
    data_file_path = os.path.join(script_dir, 'input.txt')

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    garden = []
    for line in lines:
        row = []
        for l in line.strip():
            row.append(l)
        garden.append(row)
    return garden

def printmap(map):
    print("____________")
    for row in roommap:
        print(''.join(row))
    print("^^^^^^^^^^^^")


direction = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1)
}


def findFenceCost(garden):
    m, n = len(garden[0]),  len(garden)
    regions = []
    visited = set()
    totalFencing = 0
    totalcorners = 0
    p1fenceCost = 0
    p2fenceCost = 0
    # def findRegions():
    def findConsecutiveRegion(y, x, R, region = None, boundary = None, corners = None):
        if region is None:
            region = []
        if boundary is None:
            boundary = 0
        if corners is None:
            corners = 0
        region.append((y, x))
        visited.add((y, x))
        # print("visited: ", visited)
        def checkNeighbor(y, x, R, region, boundary, corners):
            if 0 <= y < n and 0 <= x < m and garden[y][x] == R and (y, x) not in visited:
                return findConsecutiveRegion(y, x, R, region, boundary, corners)
            if not(0 <= y < n) or not(0 <= x < m) or garden[y][x] != R:
                boundary += 1
            return region, boundary, corners
        def isCorner(y, x, R, dir):
            # check if cell is an internal corner
            dy, dx = direction[dir]
            if ((0 <= y + dy < n and garden[y + dy][x] != R) or not(0 <= y + dy < n)) and \
                ((0 <= x + dx < m and garden[y][x + dx] != R) or not(0 <= x + dx < m)):
                return True
            # check if cell is an external corner
            if (0 <= y + dy < n and 0 <= x + dx < m and garden[y + dy][x] == R and \
                garden[y][x + dx] == R and garden[y + dy][x + dx] != R):
                return True
            return False
        region, boundary, corners = checkNeighbor(y + 1, x, R, region, boundary, corners)
        region, boundary, corners = checkNeighbor(y - 1, x, R, region, boundary, corners)
        region, boundary, corners = checkNeighbor(y, x + 1, R, region, boundary, corners)
        region, boundary, corners = checkNeighbor(y, x - 1, R, region, boundary, corners)
        corners += int(isCorner(y, x, R, "NE"))
        corners += int(isCorner(y, x, R, "NW"))
        corners += int(isCorner(y, x, R, "SE"))
        corners += int(isCorner(y, x, R, "SW"))
        return region, boundary, corners

    for j in range(len(garden)):
        for i in range(len(garden[j])):
            if (j, i) not in visited:
                r, b, c = findConsecutiveRegion(j,i, garden[j][i])
                totalFencing += b
                totalcorners += c
                regions.append((r, b))
                Area = len(r)
                p1fenceCost += Area * b
                p2fenceCost += Area * c
                #print("Region: ", garden[j][i], "   Area: ", Area, "   Fence: ", b)
                #print("Region: ", garden[j][i], "   Area: ", Area, "   Corners: ", c)
    # print("# Regions: ", len(regions))
    # print("boundary: ", totalFencing)
    # print("corners: ", totalcorners)
    return p1fenceCost, p2fenceCost

__FenceCost2 = None
def day12Part1(filename):
    global __FenceCost2
    garden = loaddata(filename)
    p1FenceCost, p2FenceCost = findFenceCost(garden)
    __FenceCost2 = p2FenceCost
    return p1FenceCost, "Part 1: Fence Cost"

def day12Part2(filename):
    if not __FenceCost2:
        day12Part1(filename)
    return __FenceCost2, "Part 2: Fence Cost"

if __name__ == "__main__":
    print(day12Part1("input.txt"))
    print(day12Part2("input.txt"))
