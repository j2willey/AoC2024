import os
from functools import lru_cache


def loadCombos(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)
    lines = None
    combos = []
    with open(data_file_path) as f:
        lines = f.readlines()
    for line in lines:
        #combo = [ str(d) for d in line.strip() ]
        combos.append(line.strip())
    return combos


def inscope():
    numPad = {
                '7' : (0, 0),
                '8' : (0, 1),
                '9' : (0, 2),
                '4' : (1, 0),
                '5' : (1, 1),
                '6' : (1, 2),
                '1' : (2, 0),
                '2' : (2, 1),
                '3' : (2, 2),
                '#' : (3, 0),
                '0' : (3, 1),
                'A' : (3, 2)
            }

    dirPad = {
                '#' : (0, 0),
                '^' : (0, 1),
                'A' : (0, 2),
                '<' : (1, 0),
                'v' : (1, 1),
                '>' : (1, 2)
            }
    ridPad = { v : k for k, v in dirPad.items() }

    moves = {
        '^' : (-1, 0),
        'v' : (1, 0),
        '<' : (0, -1),
        '>' : (0, 1)
    }

    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+            +---+---+
    # | 4 | 5 | 6 |            | ^ | A |
    # +---+---+---+   ==>  +---+---+---+
    # | 1 | 2 | 3 |        | < | v | > |
    # +---+---+---+        +---+---+---+
    #     | 0 | A |
    #     +---+---+

    output = []
    pos = (3,2) # 'A'


    def makePaths(src, dest, pad):
        if src == dest:
            return ['A']
        else:
            ydir = { True : 'v', False : '^' }
            xdir = { True : '>', False : '<' }
            ny, nx = abs(src[0] - dest[0]), abs(src[1] - dest[1])
            dy =  ydir[src[0] < dest[0]] * ny
            dx =  xdir[src[1] < dest[1]] * nx
            paths = []
            dap = { v : k for k, v in pad.items() }
            #print(dap)
            for path in [dy + dx, dx + dy]:
                pos = pad[start]
                for dir in path:
                    #print(f"pos: {pos}   dir: {dir}   {moves[dir][0]}  {type(pos)}")
                    pos = (pos[0] + moves[dir][0], pos[1] + moves[dir][1])
                    if dap[pos] == '#':
                        path = 'INVALID'
                        #print(f"Invalid path: {path} {pad} {dap[pos]}")
                        continue
                if path != 'INVALID':
                    paths.append(path + 'A')
            return paths


    @lru_cache(maxsize=None)
    def pathlength(code, times = 0):
        if times == 0:
            return len(code)

        subpath = []
        tot = 0
        src='A'
        for dest in code:
            tot += min( pathlength( p , times - 1) for p in paths[(src, dest)])
            src = dest
        return tot

    paths = {}
    for pad in [numPad, dirPad]:
        destinations = pad.keys()
        for start in pad:
            for dest in destinations:
                if start == '#' or dest == '#':
                    continue
                paths[(start, dest)] = makePaths(pad[start], pad[dest], pad)


    #for p in paths:
    #    print(f"{p}  {paths[p]}")

    combos = loadCombos('input.txt')
    part1sum = 0
    part2sum = 0
    for combo in combos:
        num = 0
        for d in combo:
            if d.isdigit():
                num = num * 10 + int(d)
        pl = pathlength(combo, 3)
        print(f" {combo}  {pl}  {num}")
        part1sum += num * pl
        part2sum += num * pathlength(combo, 26)
    print(f" Part 1: ", part1sum)
    print(f" Part 2: ", part2sum)



inscope()