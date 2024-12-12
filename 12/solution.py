import os

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

m = len(garden[0])
n = len(garden)

def printmap(map = garden):
    print("____________")
    for row in roommap:
        print(''.join(row))
    print("^^^^^^^^^^^^")


dir = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1)
}


def findFenceCost():
    regions = []
    visited = set()
    totalFencing = 0
    fenceCost = 0
    # def findRegions():
    def findConsecutiveRegion(y, x, R, region = None, boundary = None):
        if region is None:
            region = []
        if boundary is None:
            boundary = 0
        region.append((y, x))
        visited.add((y, x))
        # print("visited: ", visited)
        def checkNeighbor(y, x, R, region, boundary):
            if 0 <= y < n and 0 <= x < m and garden[y][x] == R and (y, x) not in visited:
                return findConsecutiveRegion(y, x, R, region, boundary)
            if not(0 <= y < n) or not(0 <= x < m) or garden[y][x] != R:
                boundary += 1
            return region, boundary
        region, boundary = checkNeighbor(y + 1, x, R, region, boundary)
        region, boundary = checkNeighbor(y - 1, x, R, region, boundary)
        region, boundary = checkNeighbor(y, x + 1, R, region, boundary)
        region, boundary = checkNeighbor(y, x - 1, R, region, boundary)
        return region, boundary

    for j in range(len(garden)):
        for i in range(len(garden[j])):
            if (j, i) not in visited:
                r, b = findConsecutiveRegion(j,i, garden[j][i])
                totalFencing += b
                regions.append((r, b))
                Area = len(r)
                fenceCost += Area * b
                #print("Region: ", garden[j][i], "   Area: ", Area, "   Fence: ", b)
    print("# Regions: ", len(regions))
    print("boundary: ", totalFencing)
    return fenceCost

print("Part 1: FenceCost: ", findFenceCost())
    