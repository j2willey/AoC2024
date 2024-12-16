import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'test2.txt')
data_file_path = os.path.join(script_dir, 'input.txt')

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

inMap = True
omap = []
moves = []
for line in lines:
    row = []
    if line.strip() == "":
        inMap = False
        continue
    if inMap:
        for l in line.strip():
            row.append(l)
        omap.append(row)
    else:
        moves.append(line.strip())
moves = "".join(moves)

def printmap(map = omap):
    print("____________")
    for row in map:
        print(''.join(row))
    print("^^^^^^^^^^^^")

def printmoves(moves):
    print(f"moves: \"{moves}\"")

dir = { '^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1) }

def findRobot(amap):
    for j in range(len(amap)):
        for i in range(len(amap[j])):
            if amap[j][i] in ['@']:
                return (i, j)

# moveRobot, the robot can push any and all boxes 'O' in the direction it is moving...
# replacing empty spaces '.' with the with the boxes or robot '@', until a wall '#'
# is encountered. move the robot and boxes it would push n space in the directions
# specified, return the updated map after the robot has moved.
def moveRobot(x, y, dx, dy, rmap, n = 1):
    if n == 0:
        return rmap, x, y
    if rmap[y + dy][x + dx] == '#':
        return rmap, x, y
    if rmap[y + dy][x + dx] == '.':
        rmap[y + dy][x + dx] = '@'
        rmap[y][x] = '.'
        return moveRobot(x + dx, y + dy, dx, dy, rmap, n - 1)
    i, j = dx, dy
    while rmap[y + j][x + i] == 'O':
        i += dx
        j += dy
    if rmap[y + j][x + i] == '#':
        return rmap, x, y
    # else  rmap[x + i][y + j] == '.'
    rmap[y + j][x + i] = 'O'
    rmap[y + dy][x + dx] = '@'
    rmap[y][x] = '.'
    return moveRobot(x + dx, y + dy, dx, dy, rmap, n - 1)

def sumGPS(omap):
    sum = 0
    for j in range(1, len(omap) -1):
        for i in range(1, len(omap[0]) -1):
            if omap[j][i] =='O':

                sum += (100 * j) + i
    return sum



printmap(omap)
printmoves(moves)

x, y = findRobot(omap)

for d in moves:
    dy, dx = dir[d]
    #print(f"\nd, dx, dy: '{d}'  {dx}, {dy}")
    omap, x, y = moveRobot(x, y, dx, dy, omap)
    #printmap(omap)

printmap(omap)

# Part1 solution  1426855
print(f"Part1 solution  {sumGPS(omap)}")


# test1.txt
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
# test1.txt
# In the smaller example, the sum is 2028.

# test2.txt
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

# test2.txt
# Part1 test2 solution  10092
