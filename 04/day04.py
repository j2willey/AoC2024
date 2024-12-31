# Day 5
import os

def loaddata(filename = "input.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    xwords = []
    for line in lines:
        row = []
        for l in line:
            row.append(l)
        xwords.append(row)
    return xwords

def day4Part1(filename = "input.txt"):

    def checkDXDY(x,y, dx, dy):
        if xwords[y+dy][x+dx] == "M" and xwords[y+2*dy][x+2*dx] == "A" and xwords[y+3*dy][x+3*dx] == "S":
            return 1
        return 0

    def checkX(x, y):
        found = 0
        right = x + 3 < len(xwords[0])
        down = y + 3 < len(xwords)
        left = x - 3 >= 0
        up = y - 3 >= 0

        if left:
            found += checkDXDY(x, y, -1, 0)  # Left
        if left and up:
            found += checkDXDY(x, y, -1, -1)  # Up-left
        if up:
            found += checkDXDY(x, y, 0, -1)  # Up
        if up and right:
            found += checkDXDY(x, y, 1, -1)  # Up-right
        if right:
            found += checkDXDY(x, y, 1, 0)  # Right
        if right and down:
            found += checkDXDY(x, y, 1, 1)  # Down-right
        if down:
            found += checkDXDY(x, y, 0, 1)  # Down
        if down and left:
            found += checkDXDY(x, y, -1, 1)  # Down-left
        return found

    totalFound = 0
    xwords = loaddata(filename)
    for y in range(len(xwords)):
        for x in range(len(xwords[0])):
            if xwords[y][x] == "X":
                totalFound += checkX(x, y)
    return totalFound, "xmas"


def checkA(x, y, xwords):
    mas = {"M":"S", "S":"M"}
    right = x + 1 < len(xwords[0])
    down = y + 1 < len(xwords)
    left = x - 1 >= 0
    up = y - 1 >= 0

    if left and right and up and down and \
        xwords[y-1][x-1] in mas and xwords[y+1][x+1] == mas[xwords[y-1][x-1]] and \
        xwords[y-1][x+1] in mas and xwords[y+1][x-1] == mas[xwords[y-1][x+1]]:
        return 1
    return 0

def day4Part2(filename = "input.txt"):
    xwords = loaddata(filename)
    totalFound = 0
    for y in range(len(xwords)):
        for x in range(len(xwords[0])):
            if xwords[y][x] == "A":
                totalFound += checkA(x, y, xwords)
    return totalFound, "x-mas"


if __name__ == "__main__":
    totalFound, description = day4Part1("input.txt")
    print(f"Part 1:  {totalFound} # {description}")

    totalFound, description = day4Part2("input.txt")
    print(f"Part 2:  {totalFound} # {description}")