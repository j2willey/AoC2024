import os
import copy

# Get the directory of the current script
filename = "test.txt"
filename = "input.txt"
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, filename)

lines = None
digits = None
with open(data_file_path) as f:
    digits = f.read()
    digits = digits.strip()

roommap = []
digarr = []
fsmap = []
# print("digits:", digits)

for i,d in enumerate(digits):
    d = int(d)
    digarr = [d for d in digits]
    if i % 2 == 0:
        block = [i//2] * d
        fsmap.extend(block)
    else:
        block = ["."] * d
        fsmap.extend(block)

#print("fsmap:", fsmap)
fsmap2 = copy.deepcopy(fsmap)

def printfsmap(fsmap = fsmap):
    fsmapstr = [str(i) for i in fsmap]
    print(f" fsmap: {"".join(fsmapstr)}")

def defrag(fsmap):
    i = 0
    j = len(fsmap) - 1

    while i < j:
        while i < j and fsmap[i] != ".":
            i += 1
        while i < j and fsmap[j] == ".":
            j -= 1
        if i < j:
            fsmap[i], fsmap[j] = fsmap[j], fsmap[i]
            i += 1
            j -= 1
    return fsmap

def defrag2(fsmap):
    i = 0
    j = len(fsmap) - 1

    freespace = []
    #print("freespace:", freespace)
    def findspace(fsmap):
        i = 0
        freespace = []
        while i < len(fsmap):
            #print("i:", i, freespace)
            while i < len(fsmap) and fsmap[i] != ".":
                i += 1
            j = 0
            while i + j < len(fsmap) and fsmap[i + j] == ".":
                j += 1
            if j > 0:
                freespace.append([i, j])
                i += j
            else:
                i += 1
        return freespace

    def findfiles(fsmap):
        i = 0
        files = []
        while i < len(fsmap):
            currentfile = fsmap[i]
            #print("i:", i, files)
            while i < len(fsmap) and fsmap[i] == ".":
                i += 1
            j = 0
            currentfile = fsmap[i]
            while i + j < len(fsmap) and fsmap[i + j] == currentfile:
                j += 1
            if j > 0:
                files.append([i, j, currentfile])
                i += j
            else:
                i += 1
        return files

    start = 0
    size = 1
    id = 2

    freespace = findspace(fsmap)
    files = findfiles(fsmap)
    #print("freespace:", freespace)
    #print("files:", files)
    curfile = len(files) -1

    while curfile >= 0 and files[curfile][start] > freespace[0][start]:
        #printfsmap(fsmap)
        frblk = 0
        while frblk < len(freespace) and \
               freespace[frblk][start] < files[curfile][start] and \
                   freespace[frblk][size] < files[curfile][size]:
            frblk += 1
        if frblk < len(freespace)and \
               freespace[frblk][start] < files[curfile][start]:
            # move file to freespace
            fsmap[freespace[frblk][start]:freespace[frblk][start] + files[curfile][size]] = [files[curfile][id]] * files[curfile][size]
            # write '.' to in place of file in fsmap
            fsmap[files[curfile][start]:files[curfile][start] + files[curfile][size]] = ["."] * files[curfile][size]
            files[curfile][start] = freespace[frblk][start]
            if freespace[frblk][size] == files[curfile][size]:
                freespace.pop(frblk)
            else:
                freespace[frblk][start] += files[curfile][size]
                freespace[frblk][size] -= files[curfile][size]
            files.sort(key=lambda x: x[start])
        else:
            curfile -= 1
    #printfsmap(fsmap)

    return fsmap

def checksum(fsmap):
    sum = 0
    for pos, id in enumerate(fsmap):
        if id != ".":
            sum += pos * id
    return sum

#printfsmap()
fsmap = defrag(fsmap)
fsmap2 = defrag2(fsmap2)
#printfsmap()
#print(fsmap)
print("Part 1 checksum:", checksum(fsmap))

#printfsmap(fsmap2)
print("Part 2 checksum:", checksum(fsmap2))
