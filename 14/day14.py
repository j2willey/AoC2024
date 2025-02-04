import re
import os
#import time

def loaddata(filename = 'input.txt'):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)
    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    # lines look like this:
    # p=0,4 v=3,-3
    # parse as position and velocity
    # position is a tuple of 2 ints
    # velocity is a tuple of 2 ints
    def parse_line(line):
        m = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
        return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))

    robots = []
    for line in lines:
        line = line.strip()
        robot = parse_line(line)
        #print(line, "r:", robot)
        robots.append(robot)
    return robots

def buildmap(robots):
    # m, n = 11, 7   'test.txt'
    m, n = 101, 103
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
    # m, n = 11, 7   'test.txt'
    m, n = 101, 103
    bmap = [['.' for i in range(m)] for j in range(n)]
    #print("".join([str(i%10) for i in range(m)]))
    for r in robots:
        if bmap[r[0][1]][r[0][0]] == '.':
            bmap[r[0][1]][r[0][0]] = '0'
        bmap[r[0][1]][r[0][0]] = str(int(bmap[r[0][1]][r[0][0]]) + 1)
    for row in bmap:
        print("".join(row))



#printmap(robots)

def move_robot(robot, seconds):
    # m, n = 11, 7   'test.txt'
    m, n = 101, 103
    pos, vel = robot
    new_pos = (((pos[0] + (vel[0] * seconds)) % m), ((pos[1] + (vel[1] * seconds)) % n))
    return (new_pos, vel)

def day14Part1(filename):
    robots = loaddata(filename)
    # m, n = 11, 7   'test.txt'
    m, n = 101, 103
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
        elif rpos[0] > ( m // 2):
            if rpos[1] < n // 2:
                quads[2] += 1
            elif rpos[1] > (n // 2) :
                quads[3] += 1
    #print(quads)
    #printmap(newrobots)

    safetyFactor = 1
    for q in quads:
        safetyFactor *= q

    return safetyFactor, "Part 1: Safety Factor"

def day14Part2(filename):
    return 8159, "Part 2: Seconds (Found by Brute Force)"
    robots = loaddata(filename)
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

    # Seconds: 8159   Found by Brute Force....
    return seconds, "Part 2: Seconds (Found by Brute Force)"

if __name__ == "__main__":
    print(day14Part1("input.txt"))
    #print(day14Part2("input.txt"))

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

