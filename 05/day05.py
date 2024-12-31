import os

def loaddata(filename = "input.txt"):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, filename)

    rules = []
    updates = []

    with open(data_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if '|' in line:
                rules.append([ int(i) for i in line.strip().split("|")])
            else:
                updates.append(line.strip().split(","))

    updates = [[int(i) for i in j] for j in updates[1:]]

    #create a dictionary of rules
    ruledict = {}
    for rule in rules:
        if rule[0] in ruledict:
            ruledict[rule[0]].append(rule[1])
        else:
            ruledict[rule[0]] = [rule[1]]

    #print("ruledict: ", ruledict)
    return updates, ruledict

def checkordered(update, rulesdict):
    for i, num in enumerate(update):
        for j in range(i):
            if num in rulesdict and update[j] in rulesdict[num]:
                #print("out of order: ", update)
                return False
    return True

def fixupdate(update, rulesdict):
    for i, num in enumerate(update):
        for j in range(i):
            if num in rulesdict and update[j] in rulesdict[num]:
                update[i], update[j] = update[j], update[i]
    return update

def findMids(updates, rulesdict):
    mids = []
    fmids = []
    for update in updates:
        if checkordered(update, rulesdict):
            mids.append(update[len(update)//2])
        else:
            update = fixupdate(update, rulesdict)
            fmids.append(update[len(update)//2])
    return mids, fmids

def day5Part1(filename = "input.txt"):
    updates, rulesdict = loaddata(filename)
    mids, _ = findMids(updates, rulesdict)
    return sum(mids), "sum of mids of sorted updates"

def day5Part2(filename = "input.txt"):
    updates, rulesdict = loaddata(filename)
    _, fmids = findMids(updates, rulesdict)
    return sum(fmids), "sum of mids of fixed  updates"

if __name__ == "__main__":
    #mids, fmids = findMids(updates)
    midssum,  desc1 = day5Part1()
    fmidssum, desc2 = day5Part2()
    print(desc1, midssum)
    print(desc2, fmidssum)
