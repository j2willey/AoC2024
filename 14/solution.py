import re
import os
#import time

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'test.txt')
m, n = 11, 7
data_file_path = os.path.join(script_dir, 'input.txt')
m, n = 101, 103
lines = None
with open(data_file_path) as f:
    lines = f.readlines()

# lines look like this:
# p=0,4 v=3,-3
# parse as position and velocity
# position is a tuple of 2 ints
# velocity is a tuple of 2 ints

def buildmap(robots):
    bmap = [[0 for i in range(m)] for j in range(n)]
    #print("".join([str(i%10) for i in range(m)]))
    symmetry = 0
    for r in robots:
        bmap[r[0][1]][r[0][0]] += 1
    for row in bmap:
        if row == row[::-1]:
            symmetry += 1
    return symmetry

def printmap(robots):
    bmap = [['.' for i in range(m)] for j in range(n)]
    #print("".join([str(i%10) for i in range(m)]))
    for r in robots:
        if bmap[r[0][1]][r[0][0]] == '.':
            bmap[r[0][1]][r[0][0]] = '0'
        bmap[r[0][1]][r[0][0]] = str(int(bmap[r[0][1]][r[0][0]]) + 1)
    for row in bmap:
        print("".join(row))


def parse_line(line):
    m = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
    return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))

robots = []
for line in lines:
    line = line.strip()
    robot = parse_line(line)
    #print(line, "r:", robot)
    robots.append(robot)

#printmap(robots)

def move_robot(robot, seconds):
    pos, vel = robot
    new_pos = (((pos[0] + (vel[0] * seconds)) % m), ((pos[1] + (vel[1] * seconds)) % n))
    return (new_pos, vel)

quads = [0] * 4
newrobots = []
for robot in robots:
    rpos, vel =  move_robot(robot, 100)
    newrobots.append((rpos, vel))

    # calculate quadradant of rpos based on dimensions m, n
    quad = 0
    if rpos[0] < m // 2:
        if rpos[1] < n // 2:
            quads[0] += 1
        elif rpos[1] > (n // 2) :
            quads[1] += 1
        # else:
        #     print("on the line y ", rpos[1])
    elif rpos[0] > ( m // 2):
        if rpos[1] < n // 2:
            quads[2] += 1
        elif rpos[1] > (n // 2) :
            quads[3] += 1
    #     else:
    #         print("on the line y ", rpos[1])
    # else:
    #     print("on the line x ", rpos[0], (m // 2) + 1)
    #print(rpos, quad)
print(quads)

#printmap(newrobots)

safteyFactor = 1
for q in quads:
    safteyFactor *= q

print("p1 Saftey Factor:", safteyFactor)

for seconds in range(1,10000):
    for i, robot in enumerate(robots):
        rpos, vel =  move_robot(robot, 1)
        robots[i] = (rpos, vel)

    symmetry = buildmap(robots)
    if symmetry > 5:
        print("\n\n")
        printmap(robots)
        print("Seconds:", seconds, "  Symmetery:", symmetry)
        #time.sleep(0.5)

# ................1....................................................................................
# ............1..........1111111111111111111111111111111...............................................
# .......................1.............................1...............................................
# .......................1.............................1...............................................
# .......................1.............................1...............................................
# .......................1.............................1...............................................
# .......................1..............1..............1...............................1...............
# .................1.....1.............111.............1...................1...........................
# .......................1............11111............1...............................................
# .......................1...........1111111...........1...............................................
# .......................1..........111111111..........1..............................1...1............
# .......................1............11111............1.......................1.......................
# .......................1...........1111111...........1...............................................
# .......................1..........111111111..........1..........................................1....
# .......................1.........11111111111.........1.....................1.........................
# .......................1........1111111111111........1...............................................
# .......................1..........111111111..........1...............................................
# .......................1.........11111111111.........1....................1........1...............1.
# ..1....................1........1111111111111........1...............................................
# .......................1.......111111111111111.......1...............................................
# .......................1......11111111111111111......1..........1....................................
# .......................1........1111111111111........1..............1................1...1...........
# .......................1.......111111111111111.......1...1......1....................................
# ........1........1.....1......11111111111111111......1...............................................
# .............11........1.....1111111111111111111.....1...............................................
# .......................1....111111111111111111111....1........................................1......
# .......................1.............111.............1....................1..........................
# .......................1.............111.............1............................1..................
# .......................1.............111.............1...............................................
# ..........1............1.............................1...............................................
# .......................1.............................1...............................................
# .......................1.............................1...................1............1..............
# ...1...................1.............................1...............................................
# .......................1111111111111111111111111111111.........................1............1........
# ....................................................................................1................

# Seconds: 8159

