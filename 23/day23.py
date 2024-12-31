import os
from itertools import combinations
from itertools import permutations

def loadConnections(filename = 'test.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    connections = []

    with open(data_file_path) as f:
        lines = f.readlines()
        for line in lines:
            connections.append( tuple(m for m in sorted(line.strip().split("-"))) )
    return connections

def findAllTTripples(connected):
    triples = set()
    for c0 in connected:
        if c0[0] == 't':
            for c1, c2 in combinations(connected[c0], 2):
                if c2 in connected[c1]:
                    triples.add(tuple(sorted((c0,c1,c2))))
    return triples


def setupConnections(filename = 'input.txt'):
    cxns = loadConnections('input.txt')
    connected = {}
    for c in cxns:
        if c[0] not in connected:
            connected[c[0]] = set()
        if c[1] not in connected:
            connected[c[1]] = set()
        connected[c[0]].add(c[1])
        connected[c[1]].add(c[0])
    return cxns, connected

# find and return the largets set of fully interconnected parties
def findLargestFullyInterConnectedGroup(cxns, connected):
    fullyConnected = set([ c[0] for c in cxns])
    largestGroup = set()
    visited = set()

    def connectionCheck(groupsofar, tocheck):
        if len(tocheck) == 0:
            return
        for m in tocheck:
            tmpgroup = tuple(sorted( groupsofar + (m,) ))
            if tmpgroup in fullyConnected:
                continue
            else:
                for n in groupsofar:
                    if m not in connected[n]:
                        break
                else:
                    fullyConnected.add(tmpgroup)
                    nexttocheck = tocheck.copy()
                    nexttocheck.remove(m)
                    connectionCheck(tmpgroup, nexttocheck)

    for k, v in connected.items():
        connectionCheck((k,), v)

    largestGroup = max(fullyConnected, key=len)

    return largestGroup


def day23Part1(filename = 'input.txt'):
    cxns, connected = setupConnections(filename)
    triples = findAllTTripples(connected)
    return len(triples), "Part 1: Triples with atleast one 't.' connection:"


def day23Part2(filename = 'input.txt'):
    cxns, connected = setupConnections(filename)
    largestGroup = findLargestFullyInterConnectedGroup(cxns, connected)
    # Expect  av,ax,dg,di,dw,fa,ge,kh,ki,ot,qw,vz,yw
    return ",".join(sorted(largestGroup)), "Part 2:  largest group/password:"


if __name__ == "__main__":
    print(day23Part1())
    print(day23Part2())
