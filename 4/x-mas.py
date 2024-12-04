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

mas = {"M":"S", "S":"M"}

def checkA(x, y):
    global xwords
    right = x + 1 < len(xwords[0])
    down = y + 1 < len(xwords)
    left = x - 1 >= 0
    up = y - 1 >= 0

    if left and right and up and down and \
        xwords[y-1][x-1] in mas and xwords[y+1][x+1] == mas[xwords[y-1][x-1]] and \
        xwords[y-1][x+1] in mas and xwords[y+1][x-1] == mas[xwords[y-1][x+1]]:
        return 1
    return 0

for y in range(len(xwords)):
    for x in range(len(xwords[0])):
        if xwords[y][x] == "A":
            totalFound += checkA(x, y)

print("x-mas: ", totalFound)