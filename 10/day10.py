import os

def loaddata(filename = 'input.txt'):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    topo = []
    for line in lines:
        row = [ int(s) for s in line.strip()]
        topo.append(row)

    return topo


def printmap(thismap):
    print("____________")
    print("    x ", "".join([str(i%10) for i in range(len(thismap[0]))]))
    for i, row in enumerate(thismap):
        print(f"y{i:3}: ", ''.join(str(x) for x in row))
    print("^^^^^^^^^^^^")

def findAllTrailheads(topo):
    trailheads = []
    for i in range(len(topo)):
        for j in range(len(topo[i])):
            if topo[i][j] == 0:
                trailheads.append([j, i])
    return trailheads

def findAllPeaks(x, y, topo):
    m, n = len(topo[0]), len(topo)
    peaks = []
    if topo[y][x] == 9:
        return [ (x, y) ]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < m and ny >= 0 and ny < n:
            if topo[ny][nx] ==  topo[y][x] + 1:
                peaks.extend( findAllPeaks(nx, ny, topo) )
    return peaks

def findAllPeaksRatings(x, y, topo):
    m, n = len(topo[0]), len(topo)
    peaks = 0
    if topo[y][x] == 9:
        return 1
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < m and ny >= 0 and ny < n:
            if topo[ny][nx] ==  topo[y][x] + 1:
                peaks +=  findAllPeaksRatings(nx, ny, topo)
    return peaks

def day10Part1(filename = 'input.txt'):
    topo = loaddata(filename)
    trailheads = findAllTrailheads(topo)
    totalTrails = 0
    for x, y in trailheads:
        trails = findAllPeaks(x, y, topo)
        trails = len(set(trails))
        totalTrails += trails
    return totalTrails, "Part 1 - totalTrails"

def day10Part2(filename):
    topo = loaddata(filename)
    trailheads = findAllTrailheads(topo)
    totalRatings = 0
    for x, y in trailheads:
        totalRatings += findAllPeaksRatings(x, y, topo)
    return totalRatings, "Part 2 - totalRatings"

if __name__ == "__main__":
    topo = loaddata()
    #printmap(topo)
    totalTrails, _ = day10Part1("input.txt")
    totalRatings, _ = day10Part2("input.txt")
    print("Part 1 - totalTrails:", totalTrails)
    # Part 1 - totalTrails: 820
    print("Part 2 - totalRatings:", totalRatings)
    # Part 2 - totalRatings: 1786

