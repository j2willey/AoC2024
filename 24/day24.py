import re
import os
from collections import defaultdict
import traceback


class gate:

    wiresdb = {}

    def __init__(self, input1, gateop, input2, output, gatename = None):
        self.input1 = input1
        self.gateop = gateop
        self.input2 = input2
        self.output = output
        self.input1State = None
        self.input2State = None
        self.updateName(gatename)
        if self.gateop == 'AND':
            self.gate = self.__AND__
        elif gateop == 'OR':
            self.gateop = 'OR '
            self.gate = self.__OR__
        elif gateop == 'XOR':
            self.gate = self.__XOR__
        else:
            raise ValueError(f"Invalid gate type:  gateop")

    def updateName(self, gatename = None):
        if gatename == None:
            gatename = self.input1 + '_' + self.gateop + '_' + self.input2 + '->' + self.output
        self.name = gatename
        return self.name

    def updateInput1(self, input1):
        self.input1 = input1
        return self.updateName()

    def updateInput2(self, input2):
        self.input2 = input2
        return self.updateName()

    def updateOutput(self, output):
        self.output = output
        return self.updateName()

    def inputs(self):
        return (self.input1, self.input2)

    def __OR__(self):
        return int( self.input1State == 1 or self.input2State == 1)

    def __AND__(self):
        if self.input1State == 1 and self.input2State == 1:
            return 1
        elif self.input1State == None or self.input2State == None:
            return None
        else:
            return 0

    def __XOR__(self):
        if self.input1State != self.input2State and self.input1State != None and self.input2State != None:
            return 1
        elif self.input1State == None or self.input2State == None:
            return None
        else:
            return 0

    def update(self, wire, state):
        if self.input1 == wire:
            self.input1State = state
        if self.input2 == wire:
            self.input2State = state
        if self.output != None:
            self.wiresdb[self.output].update(self.gate())           # Update the output wire

        return self.output

    def __str__(self):
        return f'{self.name} {self.input1}({self.input1State}) {self.gateop} {self.input2}({self.input2State}) -> {self.output}({self.gate()})'
        return f"{self.input1}({self.input1State}) {self.name} {self.input2}({self.input2State}) -> {self.output}({self.gate()})"

    def __repr__(self):
        return f"{self.input1}({self.input1State}) {self.name} {self.input2}({self.input2State}) -> {self.output}({self.gate()})"

class wire:
    gatesdb = None

    def __init__(self, name, state = None):
        self.name = name
        self.connections = []
        self.state = state

    def update(self, state):
        self.state = state
        for connection in self.connections:
            self.gatesdb[connection].update(self.name, state)

    def connect(self, gate):
        self.connections.append(gate)

    def __str__(self):
        return f"{self.name}: {self.state} {self.connections}"

    def __repr__(self):
        return f"{self.name}: {self.state} {self.connections}"

# ==========================
# Ynn XOR Xnn -> _A_
# Ynn AND Xnn -> _B_
# C-1 AND _A_ -> _D_
# _A_ XOR C-1 -> znn  Bit nn
# _B_ OR  _D_ -> _Cn  Carry
# ==========================
class adder:
    def __init__(self, input1 = None, input2 = None, output = None):
        self.bit = None             # Bit n
        self.input1 = input1        # x2
        self.input2 = input2        # x2

        self.abxor = None           # x2             A XOR B
        self.sum = None             # x1 Bit n Sum    (A XOR B) XOR Carry
        self.aband = None           # x1              (A AND B)
        self.c1aband = None         # x1              Carry n-1 AND (A XOR B)
        self.c = None               # (x1) Bit n Carry  c1absum OR carry
        self.expectedSum = None     #              expected Znn
        self.expectedC1Sum = None   #              expect Sum from Carry n-1 and A XOR B
        self.expectedC1aband = None #              expect Cn01 AND (A AND B) from Carry n-1
        self.expectedCnaband = None #              expect Carry from A AND B

    def cn(self):
        if self.c:
            return self.c[-3:]
        return None

    def __str__(self):
        def gateName(gate):
            if gate:
                return f"{gate[-3:]}    {gate}"
            return None
        allGood = True

        selfstr = f"Adder bit {self.bit} \n" + \
                  f"   AB    'absum'/XOR  abxor   {gateName(self.abxor)}\n" + \
                  f"   AB    'Carry'/AND  aband   {gateName(self.aband)}\n"
        if self.expectedC1aband != self.c1aband:
            selfstr = selfstr + f"         C1n Expected c1aband {gateName(self.expectedC1aband)}\n"
            allGood = False
        selfstr = selfstr + f"   abCn1 'sumtoC'/AND c1aband {gateName(self.c1aband)}\n"

        if self.expectedC1Sum != self.sum or self.sum == None:
            #selfstr = selfstr + f"         Znn Expected Sum     {gateName(self.expectedSum)}\n"
            selfstr = selfstr + f"         C1n Expected Sum     {gateName(self.expectedC1Sum)}\n"
            allGood = False
        selfstr = selfstr + f"   abC   'sum'/XOR    sum     {gateName(self.sum)}\n"

        if self.expectedCnaband != self.c:
            selfstr = selfstr + f"   A AND B Expected Carry     {gateName(self.expectedCnaband)}\n"
            allGood = False
        selfstr = selfstr + f"   C     'Carry'      c       {gateName(self.c)}"

        if allGood:
             selfstr = f"Adder bit {self.bit} adder looks good"
        return selfstr


    def __repr__(self):
        return f"{self.input1} + {self.input2} -> {self.sum}"


def loadSchema(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    wiresdb = {}

    gatesdb = {}
    circuitinputs = []
    bits = []

    lines = None
    with open(data_file_path) as f:
        lines = f.readlines()

    for line in lines:
        wiresPattern = r"([xy]\d\d): (\d)"
        gatesPattern = r"([a-z\d]{3}) (AND|OR|XOR) ([a-z\d]{3}) -> ([a-z\d]{3})"
        match = re.match(wiresPattern, line)
        if match:
            wirename = match.group(1)
            state = int(match.group(2))
            wiresdb[wirename] = wire(wirename, state)
            circuitinputs.append(wirename)

        match = re.match(gatesPattern, line)
        if match:
            input1 = match.group(1)
            gateop = match.group(2)
            input2 = match.group(3)
            output = match.group(4)
            gatename = input1 + '_' + gateop + '_' + input2 + '->' + output
            gatesdb[gatename] = gate(input1, gateop, input2, output, gatename)
            if input1 not in wiresdb:
                wiresdb[input1] = wire(input1)
            if input2 not in wiresdb:
                wiresdb[input2] = wire(input2)
            if output not in wiresdb:
                wiresdb[output] = wire(output)
            wiresdb[input1].connect(gatename)
            wiresdb[input2].connect(gatename)

    otg = { g.output : g.name for g in gatesdb.values() }
    return wiresdb, gatesdb, circuitinputs, otg

def printGates(gatesdb):
    return
    for g in gatesdb.values():
        print(g)


def part1solution(inputs, wiresdb):
    for wire in inputs:
        wiresdb[wire].update(wiresdb[wire].state)

    zwires = [ (w.name, w.state)  for w in wiresdb.values() if w.name[0] == 'z' ]
    zwires.sort(key = lambda x: x[0], reverse = True)

    p1bin =  ''.join([ str(z[1]) for z in zwires])
    p1output = int(p1bin, 2)
    return p1output


def verifyAdders(gatesdb, wiresdb, outputs):
    adders = {}
    confused = []

    def gout(gate):
        if gate:
            return gatesdb[gate].output
        return None

    def prospect(wire, gatetype):
        matches = []
        if wire not in wiresdb:
            # print(f" ERROR: wire __{wire}__ not in wiresdb")
            return None
        for p in wiresdb[wire].connections:
            if gatesdb[p].gateop == gatetype:
                matches.append(p)
        if len(matches) != 1:
            #print(f" ERROR: found matches != 1 for  prospect({wire}, {gatetype})  {matches}")
            pass
        return "  [!= 1]  ".join(matches)

    wirePattern = r"([xy])(\d\d)"
    # First pass, Create Adders with AB inputs  aband and abxor from wiresdb
    for wire in wiresdb:
        match = re.match(wirePattern, wire)
        if match:
            bitstr = match.group(2)
            bit    = int(bitstr)
            if bit not in adders:
                adders[bit] = adder()
                adders[bit].bit = bitstr
            if wire[0] == 'x':
                adders[bit].input1 = wire
            elif wire[0] == 'y':
                adders[bit].input2 = wire

            # First pass, populate adder "abxor" and "aband" from AB inputs
            abxor = prospect(wire, 'XOR')
            if bit == 0:
                adders[bit].sum = abxor
            adders[bit].abxor = abxor
            aband = prospect(wire, 'AND')
            if bit == 0:
                adders[bit].c = aband
                adders[bit].expectedCnaband = aband
            adders[bit].aband = aband

    # populate adder  "sum"  from EXPECTED Z bits...
    for a in adders.values():
        expectedBitSum = "z" + a.bit
        # print(f"Bit {a.bit}  Expected Sum {expectedBitSum} 1[{outputs[expectedBitSum]}] gateop {gatesdb[outputs[expectedBitSum]].gateop}")
        a.expectedSum = gatesdb[outputs[expectedBitSum]].name
        if gatesdb[outputs[expectedBitSum]].gateop == 'XOR':
            a.sum = gatesdb[outputs[expectedBitSum]].name
        else:
            confused.append(expectedBitSum)
        if a.bit == '00':
            a.expectedC1Sum = gatesdb[outputs[expectedBitSum]].name

    # Lets see what we have
    #for a in adders:
    #    print(adders[a])
    # Second pass, follow through coordinating outputs of first pass...
    # print("\n===========================\nPass 2")
    # print("===========================\n")
    for bit in adders:
        if bit == 0:
            continue
        # print(f"Bit {bit}")

        expectedCin = adders[bit-1].cn()
        abCnxorprospect = prospect(expectedCin, 'XOR')
        if not abCnxorprospect:
            # print(f"Bit {bit} Expected Sum Prospect not found from 'Carry-in'... using {adders[bit].abxor}")
            abCnxorprospect = prospect(gout(adders[bit].abxor), 'XOR')
            confused.append(expectedCin)
        pg = gatesdb[abCnxorprospect]
        if pg.output[0] != 'z':
            confused.append(pg.output)
        adders[bit].expectedC1Sum = pg.name


        abandprospect = prospect(expectedCin, 'AND')
        if not abandprospect:
            # print(f"Bit {bit} Expected ABC1and Prospect not found from 'Carry-in'... using {adders[bit].abxor}")
            abandprospect = prospect(gout(adders[bit].abxor), 'AND')
            confused.append(expectedCin)
        #else: #if abandprospect:
        pg = gatesdb[abandprospect]
        adders[bit].expectedC1aband = pg.name
        if ( gout(adders[bit].abxor) in pg.inputs()):
            adders[bit].c1aband =  pg.name
        else:
            # print(f"No Matchy2!!! Bit {bit} [[[ {pg.input1} ]]] [[[{pg.input1}]]] {gout(adders[bit].abxor)} ")
            confused.append(gout(adders[bit].abxor))


        carryprospect = prospect(gout(adders[bit].aband), 'OR ')
        if not carryprospect:
            # print(f"Carry Prospect not found for bit {bit}  {adders[bit].aband}")
            confused.append(gout(adders[bit].aband))
            carryprospect = prospect(gout(adders[bit].c1aband), 'OR ')
        # carryn1axorboutput  = gout(adders[bit].c1aband)
        if carryprospect:
            pg = gatesdb[carryprospect]
            adders[bit].expectedCnaband = pg.name
            #if ( carryn1axorboutput in pg.inputs() ):
            adders[bit].c =  pg.name
            # else:
            #     print(f"No Matchy3!!! Bit {bit} [[[ {pg.input1} ]]] [[[ {pg.input1} ]]] {carryn1axorboutput} ")


    return adders, confused


wiresdb, gatesdb, inputs, outputs = loadSchema('input.txt')

gate.wiresdb = wiresdb
wire.gatesdb = gatesdb

def setup(filename):
    wiresdb, gatesdb, inputs, outputs = loadSchema(filename)
    gate.wiresdb = wiresdb
    wire.gatesdb = gatesdb
    return wiresdb, gatesdb, inputs, outputs

def day24Part1(filename = 'input.txt'):
    wiresdb, gatesdb, inputs, outputs = setup(filename)
    p1output = part1solution(inputs, wiresdb)
    #print(f'part 1:  {str(p1output)}')
    return p1output, "Part 1: output"


def day24Part2(filename = 'input.txt'):
    wiresdb, gatesdb, inputs, outputs = setup(filename)
    adders, confused = verifyAdders(gatesdb, wiresdb, outputs)

    # for a in adders:
    #     print(adders[a])

    confused = set(confused)
    confused.discard(None)
    confused = list(confused)
    confused.sort()

    # print(f"Confused: {confused}")
    # print(f"Confused: {",".join(confused)}")
    return ",".join(confused), "Part 2: confused gates"

if __name__ == "__main__":
    print(day24Part1('input.txt'))
    print(day24Part2('input.txt'))
