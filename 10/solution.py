import os

# Get the directory of the current script
filename = "test.txt"
filename = "input.txt"
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, filename)

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

topo = []
for line in lines:
    row = [ int(s) for s in line.strip()]
    topo.append(row)

m = len(topo[0])
n = len(topo)


def printmap(thismap = topo):
    print("____________")
    print("    x ", "".join([str(i%10) for i in range(len(thismap[0]))]))
    for i, row in enumerate(thismap):
        print(f"y{i:3}: ", ''.join(str(x) for x in row))
    print("^^^^^^^^^^^^")

def findAllTrailheads():
    trailheads = []
    for i in range(len(topo)):
        for j in range(len(topo[i])):
            if topo[i][j] == 0:
                trailheads.append([j, i])
    return trailheads

def findAllPeaks(x, y):
    peaks = []
    if topo[y][x] == 9:
        return [ (x, y) ]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < m and ny >= 0 and ny < n:
            if topo[ny][nx] ==  topo[y][x] + 1:
                peaks.extend( findAllPeaks(nx, ny) )
    return peaks

def findAllPeaksRatings(x, y):
    peaks = 0
    if topo[y][x] == 9:
        return 1
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < m and ny >= 0 and ny < n:
            if topo[ny][nx] ==  topo[y][x] + 1:
                peaks +=  findAllPeaksRatings(nx, ny)
    return peaks

printmap(topo)
trailheads = findAllTrailheads()
#print("trailheads:", trailheads)

totalTrails = 0
for x, y in trailheads:
    trails = findAllPeaks(x, y)
    trails = len(set(trails))
    totalTrails += trails

totalRatings = 0
for x, y in trailheads:
    totalRatings += findAllPeaksRatings(x, y)

# 820 is correct
print("Part 1 - totalTrails:", totalTrails)
print("Part 2 - totalRatings:", totalRatings)

# Part 1 - totalTrails: 820
# Part 2 - totalRatings: 1786

# cleanmap = copy.deepcopy(roommap)