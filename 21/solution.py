import os


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

combos = loadCombos('test.txt')


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

def dirToNumericKeypad(move, sourcesofar = []):
    global pos, output
    posToNum = {
            (0, 0) : '7',
            (0, 1) : '8',
            (0, 2) : '9',
            (1, 0) : '4',
            (1, 1) : '5',
            (1, 2) : '6',
            (2, 0) : '1',
            (2, 1) : '2',
            (2, 2) : '3',
            (3, 0) : 'ERROR',
            (3, 1) : '0',
            (3, 2) : 'A',
            }

    moves = {
        '^' : (-1, 0),
        'v' : (1, 0),
        '<' : (0, -1),
        '>' : (0, 1)
    }
    if move in moves:
        newpos = (pos[0] + moves[move][0], pos[1] + moves[move][1])
        if newpos[0] >= 0 and newpos[0] <= 3 and newpos[1] >= 0 and newpos[1] <= 2:
            pos = newpos
            if pos == (3, 0):
                print("Invalid move over keyboard: 3,0")
        else:
            print(f"Invalid move: {move} from {pos} to {newpos}")
            print(f'source so far: {sourcesofar}')
            print(f"output so far: {"".join(output)}")
    else: # A pressed
        output.append(posToNum[pos])

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+            +---+---+
# | 4 | 5 | 6 |            | ^ | A |
# +---+---+---+   ==>  +---+---+---+
# | 1 | 2 | 3 |        | < | v | > |
# +---+---+---+        +---+---+---+
#     | 0 | A |
#     +---+---+

def numericToDirectionalKeypad(numericcode, start = 'A'):
    numpadToPos = {
            '7' : (0, 0),
            '8' : (0, 1),
            '9' : (0, 2),
            '4' : (1, 0),
            '5' : (1, 1),
            '6' : (1, 2),
            '1' : (2, 0),
            '2' : (2, 1),
            '3' : (2, 2),
            #'x' : (3, 0),
            '0' : (3, 1),
            'A' : (3, 2)
            }

    #print(f'numericcode: {numericcode} start: {start}')
    decoded = []
    pos = numpadToPos[start]
    for c in numericcode:
        dest = numpadToPos[c]
        #print(f'pos: {pos}, dest: {dest}')
        xmove = ''
        ymove = ''

        if dest[1] > pos[1]:   # moving right
            xmove = ('>' * (dest[1] - pos[1]))
        elif dest[1] < pos[1]: # moving left
            xmove = ('<' * (pos[1] - dest[1]))

        if dest[0] > pos[0]:   # moving down,
            ymove = ('v' * (dest[0] - pos[0]))
        elif dest[0] < pos[0]: # moving up
            ymove = ('^' * (pos[0] - dest[0]))

        if dest[1] > pos[1]:
            # moving down, there for move up before right or left.
            decoded.append(xmove)
            decoded.append(ymove)
        else:
            # moving up or just horizontally. move horizontal first.
            decoded.append(ymove)
            decoded.append(xmove)
        decoded.append('A')
        pos = dest
    return [ d for d in "".join(decoded) ]


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+            +---+---+
# | 4 | 5 | 6 |            | ^ | A |
# +---+---+---+   ==>  +---+---+---+
# | 1 | 2 | 3 |        | < | v | > |
# +---+---+---+        +---+---+---+
#     | 0 | A |
#     +---+---+

    #   v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    #      <   A ^ A >  ^^ A  vvv  A
    #   v<<A>>^A<A>A<AAv>A^Av<AAA>^A
    #      <   A ^ A ^^  > A  vvv  A
    #          0   2       9       A

    #     ^A
    #    <v>



def DirToDirKeypadDown(pos, move, sourcesofar = []):
    posToDirPad = {
        (0, 0) : 'E',
        (0, 1) : '^',
        (0, 2) : 'A',
        (1, 0) : '<',
        (1, 1) : 'v',
        (1, 2) : '>'
        }
    moves = {
        '^' : (-1, 0),
        'v' : (1, 0),
        '<' : (0, -1),
        '>' : (0, 1)
    }
    output = []
    if move in moves:
        newpos = (pos[0] + moves[move][0], pos[1] + moves[move][1])
        if newpos[0] >= 0 and newpos[0] <= 1 and newpos[1] >= 0 and newpos[1] <= 2:
            pos = newpos
            if pos == (3, 0):
                print("Invalid move over KEYBOARD: 3,0")
                print(f'source so far: {sourcesofar}')
                print(f"output so far: {output}")
        else:
            print(f"Invalid move:  {move} from {pos} to {newpos}")
            print(f'source so far: {sourcesofar}')
            print(f"output so far: {output}")
    elif move == 'A' : # A pressed
        output.append(posToDirPad[pos])


    return pos, output


def DirToDirKeypadUp(dircode, start = 'A', map1 = True):
    dirdirpad = {
        ('^','A') : '>A',   # xxx  XXXXXX  simple right
        ('^','^') : 'A',    #        no move
        ('^','v') : 'vA',   #        simple down
        ('^','<') : 'v<A',  #        !! MUST go down before left
        ('^','>') : 'v>A',  #        '>v'     OPTIONS down/right or right/down

        ('<','A') : '>>^A', # xx   XXX  ? >>^   OPTIONS right/right/up or right/up/right
        ('<','^') : '>^A',  # x    X  !! MUST go right before up
        ('<','v') : '>A',   # x    XXXX  simple right
        ('<','<') : 'A',    # x      no move
        ('<','>') : '>>A',  #        Simple two rights.

        ('v','A') : '>^A',  # xx   XXXX  OPTIONS  right/up  up/right
        ('v','^') : '^A',   #        simple up
        ('v','v') : 'A',    #        no move
        ('v','<') : '<A',   # x    XX  simple left
        ('v','>') : '>A',   #        simple right

        ('>','A') : '^A',   # xx   X  simple up
        ('>','^') : '<^A',  # xx   XXXX  OPTIONS left/up  up/left
        ('>','v') : '<A',   #        simple left
        ('>','<') : '<<A',  #        simple two lefts
        ('>','>') : 'A',    # x    XX  no move

        ('A','A') : 'A',    # xxx  XX  no move
        ('A','^') : '<A',   #      X  simple left
        ('A','v') : '<vA',  # xx   XX  OPTIONS v<
        ('A','<') : 'v<<A', # xxx  XXXXXX  OPTIONS !!!  down/right/right  right/down/right '<v<'
        ('A','>') : 'vA',   # xxxx XXXXXX  simple down
        }
#029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A  >AAvA^A<v<A>A>^AAAvA<^A>A  68
#      v<<A>>^A<A> AvA<^AA>A<vAAA>^A

#      <A^A>^^AvvvA

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
    dirdir2 = {
        ('^','<') : 'v<A',  #!!
        ('^','>') : 'v>A',  # '>v'
        ('<','^') : '>^A',  #!!
        ('<','A') : '>>^A',  #? >>^
        ('<','>') : '>>A',  # '>v'
        ('v','A') : '>^A',  # '^>'
        ('>','^') : '<^A',  # '^<'
        ('>','<') : '<<A',
        ('A','<') : '<v<A', # !!!  '<<v'
        ('A','v') : '<vA',  # 'v<
        }
    if not map1:
        dirdirpad.update(dirdir2)

    #print(f'dircode: {dircode} start: {start}')
    decoded = []
    pos = start
    for c in dircode:
        dest = c
        decoded.append(dirdirpad[(pos, dest)])
        pos = dest
    return [ d for d in "".join(decoded) ]

def decode(combo):
    l0up = combo
    l1up = "".join(numericToDirectionalKeypad(l0up, 'A'))
    l2up = "".join(DirToDirKeypadUp(l1up, 'A'))
    l3   = "".join(DirToDirKeypadUp(l2up, 'A', False))
    print(f" l0: {combo} ")
    print(f" l1: {l1up}  len: {len(l1up)}")
    print(f" l2: {l2up}  len: {len(l2up)}")
    print(f" l3: {l3}  len: {len(l3)}")
    return l0up, l1up, l2up, l3

def verify(l3):
    global pos, output
    pos = (0,2)
    cmdarr = []
    print(f" l3: {"".join(l3)}  len: {len(l3)}")

    sourcesofar = []
    for c in l3:
        sourcesofar.append(c)
        pos, output  = DirToDirKeypadDown(pos, c, sourcesofar)
        cmdarr.extend(output)
    l2down = "".join(cmdarr)

    print(f" l2: {l2down}")

    pos = (0,2)
    cmdarr = []
    sourcesofar = []
    for c in l2down:
        sourcesofar.append(c)
        pos, output  = DirToDirKeypadDown(pos, c, sourcesofar)
        cmdarr.extend(output)
    l1down = "".join(cmdarr)

    print(f" l1: {l1down}")

    pos = (3,2)
    output = []
    sourcesofar = []
    for c in l1down:
        sourcesofar.append(c)
        finaloutput = dirToNumericKeypad(c, sourcesofar)
    print(f" l0: {"".join(output)}")
    l0down = "".join(output)

    return l0down, l1down, l2down

combos = loadCombos('test.txt')
cumcombos = 0
for combo in combos:
    #print(f"combo: {combo}")
    num = 0
    for d in combo:
        if d.isdigit():
            num = num * 10 + int(d)

    l0up, l1up, l2up, l3 = decode(combo)

    cumcombos += num * len(l3)
    print(" ==============================")
    print("  verify in reverse")

    l0down, l1down, l2down = verify(l3)

    if l0up == l0down:
        print(f"YEAH: {combo} == {l0down}")
    else:
        print(f"ERROR: {combo} != {l0down}")
    if l1up == l1down:
        print(f"YEAH: l1up == l1down")
    else:
        print(f"ERROR: l1up != l1down\n  up{l1up}\n {l1down}")
    if l2up == l2down:
        print(f"YEAH: l2up == l2down")
    else:
        print(f"ERROR: l2up != l2down\n  up{l2up}\n {l2down}")


print(f"cumcombos: {cumcombos}")

t379A = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
l0down, l1down, l2down = verify(t379A)
print(f"l0down: {l0down}")
print(f"l1down: {l1down}")
print(f"l2down: {l2down}")
print(f"t379A:  {t379A}")



# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A

#<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
#  v <<   A >>  ^ A   <   A > A  v  A   <  ^ AA > A   < v  AAA >  ^ A
#         <       A       ^   A     >        ^^   A        vvv      A
#                 0           2                   9                 A

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+            +---+---+            +---+---+
# | 4 | 5 | 6 |            | ^ | A |            | ^ | A |
# +---+---+---+   ==>  +---+---+---+   ==>  +---+---+---+
# | 1 | 2 | 3 |        | < | v | > |        | < | v | > |
# +---+---+---+        +---+---+---+        +---+---+---+
#     | 0 | A |
#     +---+---+

# 379A: <v<A>>^AvA ^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
#        <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
