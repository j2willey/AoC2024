import os

def loaddata(filename = "input.txt"):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

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

    return omap, moves

def xxmap(amap):
    nmap = []
    for j in range(len(amap)):
        row = []
        for x in amap[j]:
            if x == "#":
                row.extend(["#","#"])
            elif x == "O":
                row.extend(["[","]"])
            elif x == "@":
                row.extend(["@","."])
            else:  # x == "."
                row.extend([".","."])
        nmap.append(row)
    return nmap


def printmap(amap):
    print("____________")
    for row in amap:
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

# Part 2
def moveRobotX(x, y, dx, rmap, n = 1):
    if n == 0:
        return rmap, x, y
    if rmap[y][x + dx] == '#':
        return rmap, x, y
    if rmap[y][x + dx] == '.':
        rmap[y][x + dx] = '@'
        rmap[y][x] = '.'
        return moveRobotX(x + dx, y, dx, rmap, n - 1)
    i = dx
    while rmap[y][x + i] in '[]':
        i += dx
    if rmap[y][x + i] == '#':
        return rmap, x, y
    # else  rmap[y][x + i] == '.'
    while i != 0:
        rmap[y][x + i] = rmap[y][x + i - dx]
        i -= dx
    rmap[y][x] = '.'
    return moveRobotX(x + dx, y, dx, rmap, n - 1)

# In moveRobotY, the "push" is source on the first row is from one x.  But the
# boxes are 2 spaces wide, either x-1 and x, or x and x+1.  A box is now represented
# by two characters, '[' and ']', occupying 1x and 2 y coordinates.
# Need to check that the robot can freely move the boxes above or below it.
# Using Recursion to find, check and move the boxes in the direction of the push.

# x, y represent the left '[' of the box, dx, dy represent the direction of the push.]
def isBoxFreeToMoveY(x, y, dy, rmap):
    if rmap[y + dy][x] == '#' or rmap[y + dy][x + 1] == '#':
        return False
    if rmap[y + dy][x] == '.' and rmap[y + dy][x + 1] == '.':
        return True
    if rmap[y + dy][x] == '[':
        return isBoxFreeToMoveY(x, y + dy, dy, rmap)
    free = True
    if rmap[y + dy][x] == ']':
        free = isBoxFreeToMoveY(x - 1, y + dy, dy, rmap)
    if rmap[y + dy][x + 1] == '[':
        free &= isBoxFreeToMoveY(x + 1, y + dy, dy, rmap)
    return free

def moveBoxY(x, y, dy, rmap, n = 1):
    # We should already know that the box can move in the direction dy.
    # Don't need to look for wall or space. Just look for the next box(es)
    # and move them as well. If no box(es) just move this box.
    if rmap[y + dy][x] == '[':
        rmap = moveBoxY(x, y + dy, dy, rmap)
    if rmap[y + dy][x] == ']':
        rmap = moveBoxY(x - 1, y + dy, dy, rmap)
    if rmap[y + dy][x + 1] == '[':
        rmap = moveBoxY(x + 1, y + dy, dy, rmap)
    rmap[y + dy][x] = '['
    rmap[y + dy][x + 1] = ']'
    rmap[y][x] = '.'
    rmap[y][x + 1] = '.'
    return rmap


def moveRobotY(x, y, dy, rmap, n = 1):
    if n == 0 or rmap[y + dy][x] == '#':
        return rmap, x, y
    while n > 0:
        if rmap[y + dy][x] == '.':
            rmap[y + dy][x] = '@'
            rmap[y][x] = '.'
            return rmap, x, y + dy
        if rmap[y + dy][x] == "[":
            if isBoxFreeToMoveY(x, y + dy, dy, rmap):
                rmap = moveBoxY(x, y + dy, dy, rmap)
                rmap[y + dy][x] = '@'
                rmap[y][x] = '.'
                return rmap, x, y + dy
        elif rmap[y + dy][x] == "]":
            if isBoxFreeToMoveY(x - 1, y + dy, dy, rmap):
                rmap = moveBoxY(x - 1, y + dy , dy, rmap)
                rmap[y + dy][x] = '@'
                rmap[y][x] = '.'
                return rmap, x, y + dy
        n -= 1
    return rmap, x, y


def sumGPS(omap, symbol):
    sum = 0
    for j in range(1, len(omap) -1):
        for i in range(1, len(omap[0]) -1):
            if omap[j][i] == symbol:

                sum += (100 * j) + i
    return sum


def day15Part1(filename = "input.txt"):
    omap, moves = loaddata()
    x, y = findRobot(omap)

    for d in moves:
        dy, dx = dir[d]
        #print(f"\nd, dx, dy: '{d}'  {dx}, {dy}")
        omap, x, y = moveRobot(x, y, dx, dy, omap)

    # Part1 solution  1426855
    return sumGPS(omap, 'O'), "Part1 solution"

def day15Part2(filename = "input.txt"):
    omap, moves = loaddata()
    omap = xxmap(omap)

    x, y = findRobot(omap)

    for d in moves:
        dy, dx = dir[d]
        #print(f"\n ({x}, {y}) move: '{d}'    {dx}, {dy}")
        if dx != 0:
            omap, x, y = moveRobotX(x, y, dx, omap)
        else:
            omap, x, y = moveRobotY(x, y, dy, omap)

    # Part2 solution  1404917
    return sumGPS(omap, '['), "Part2 solution"

if __name__ == "__main__":
    print(day15Part1())
    print(day15Part2())

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
