import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'input.txt')

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

def checkordered(update):
    for i, num in enumerate(update):
        for j in range(i):
            if num in ruledict and update[j] in ruledict[num]:
                #print("out of order: ", update)
                return False
    return True

def fixupdate(update):
    for i, num in enumerate(update):
        for j in range(i):
            if num in ruledict and update[j] in ruledict[num]:
                update[i], update[j] = update[j], update[i]
    return update

mids = []
fmids = []
for update in updates:
    if checkordered(update):
        mids.append(update[len(update)//2])
    else:
        update = fixupdate(update)
        fmids.append(update[len(update)//2])

print("sum of mids of sorted updates", sum(mids))
print("sum of mids of fixed  updates", sum(fmids))
