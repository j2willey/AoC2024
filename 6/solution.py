import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'input.txt')

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

roommap = []
for line in lines:
    row = []
    for l in line.strip():
        row.append(l)
    roommap.append(row)

def printmap():
    print("____________")
    for row in roommap:
        print(''.join(row))
    print("^^^^^^^^^^^^")



right = {
    (-1, 0) : [0, 1],
    (0, 1) : [1, 0],
    (1, 0) : [0, -1],
    (0, -1) : [-1, 0]
}

def findStart():
    for i in range(len(roommap)):
        if '^' in roommap[i]:
            return i, roommap[i].index('^')

def patrolfwd(startx, starty, dx, dy):
    x = startx
    y = starty
    dp = 1   
    m = len(roommap[0])
    n = len(roommap)
    while True:
        #print(x, y, dx, dy)
        if x < 0 or y < 0 or x >= m or y >= n:
            break
        if roommap[x][y] == '.' or roommap[x][y] == 'X' or roommap[x][y] == '^':
            if roommap[x][y] == '.':
                dp += 1
            roommap[x][y] = 'X'
            if 0 <= x +dx < m and 0 <= y + dy < n and roommap[x + dx][y + dy] == '#':
                dx, dy = right[(dx, dy)]
            x += dx
            y += dy
        else: # roommap[x][y] == '#':
            print("Error: ", x, y, roommap[x][y])

    return dp


#printmap()
startx, starty = findStart()
dp =  patrolfwd(startx, starty, -1, 0)
#printmap()
# 5534
print("distinct positions: ",dp)
