# Day 5
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'data.txt')

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

xwords = []
for line in lines:
    row = []
    for l in line:
        row.append(l)
    xwords.append(row)

totalFound = 0

def checkDXDY(x,y, dx, dy):
    global xwords
    if xwords[y+dy][x+dx] == "M" and xwords[y+2*dy][x+2*dx] == "A" and xwords[y+3*dy][x+3*dx] == "S":
        return 1
    return 0

def checkX(x, y):
    global xwords
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

for y in range(len(xwords)):
    for x in range(len(xwords[0])):
        if xwords[y][x] == "X":
            totalFound += checkX(x, y)

print("xmas: ", totalFound)