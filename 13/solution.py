import re
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'test.txt')
data_file_path = os.path.join(script_dir, 'input.txt')

lines = None
with open(data_file_path) as f:
    lines = f.readlines()

# Machines have two buttons, A and B, and a prize location.
# Buttons A and B are pushed independently, starting at the origin (0, 0),
# trying to reach the prize location.. Each button press moves the machine
# in the corresponing X and Y units.
# Not all machines can reach the prize location.
# Lines are in the format:
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279
# Regex to parse the "Button.." lines to capture the values following the "X+" and "Y+" strings

buttonPattern = r"Button ([A-Z]): X\+(\d+), Y\+(\d+)"
prizePattern = r"Prize: X=(\d+), Y=(\d+)"

machines = []
nextmachine = {}
for line in lines:
    if line.strip() == '':
        continue
    if line.startswith('Button'):
        match = re.match(buttonPattern, line)
        if match:
            button = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))
            # print(f'Button {button} at ({x}, {y})')
            nextmachine[button] = (x, y)
    elif line.startswith('Prize'):
        match = re.match(prizePattern, line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            # print(f'Prize at ({x}, {y})')
            nextmachine['P'] = (x, y)
            machines.append(nextmachine)
            nextmachine = {}

# Linear search for the winning moves,  too slow for the large input
def winning_moves(prize, A, B):
    prize_x, prize_y = prize
    A_x, A_y = A
    B_x, B_y = B

    i = 0
    j = (prize_y // B_y + 1)
    axprd = A_x * i
    bxprd = B_x * j
    ayprd = A_y * i
    byprd = B_y * j
    # linear search for the winning moves
    while i < (prize_x // A_x + 1) + 1 and j > 0:
        if axprd + bxprd == prize_x and ayprd + byprd == prize_y:
            print (f'Winning moves: A {i}  B {j}')
            return 3 * i + j
        if axprd + bxprd > prize_x:
            j -= 1
            bxprd -= B_x
            byprd -= B_y
        elif axprd + bxprd < prize_x:
            i += 1
            axprd += A_x
            ayprd += A_y
        else:
            j -= 1
            i += 1
            bxprd -= B_x
            byprd -= B_y
            axprd += A_x
            ayprd += A_y
    return 0

# Math solution, two equations, two unknowns, solve for B and then plug for A
def winning_moves2(prize, A, B):
    xp, yp = prize
    xa, ya = A
    xb, yb = B

    Bn = (xp * ya - xa * yp) / (xb * ya - xa * yb)
    An = (xp - Bn * xb) / xa

    if An >= 0 and Bn >= 0 and An.is_integer() and Bn.is_integer():
        #print (f'Winning moves: A {An}  B {Bn} for prize {prize}')
        return 3 * int(An) + int(Bn)
    return 0


p1minimum_cost = 0
p2minimum_cost = 0
conversionfactor = 10000000000000
for machine in machines:
    A = machine['A']
    B = machine['B']
    Prize = machine['P']
    Prize2 = (Prize[0] + conversionfactor, Prize[1] + conversionfactor)
    moves = winning_moves2(Prize, A, B)
    #moves = binary_search_for_winning_moves(Prize, A, B)
    p1minimum_cost += moves
    moves = winning_moves2(Prize2, A, B)
    #moves = binary_search_for_winning_moves(Prize2, A, B)
    p2minimum_cost += moves

print("Part 1: test.txt  = 480")
print("Part 2: test.txt  = ???")
print("Part 1: input.txt = 36870")
print("Part 2: input.txt = 78101482023732")

print("Part 1: minimum cost:", p1minimum_cost)
print("Part 2: minimum cost:", p2minimum_cost)