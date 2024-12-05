import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'test.txt')

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
print(rules[:5]) 
print(updates[:5])

ruledict = {}
reversedict = {}
for rule in rules:
    if rule[0] in ruledict:
        ruledict[rule[0]].append(rule[1])
    else:
        ruledict[rule[0]] = [rule[1]]

sortedrules = sorted(ruledict.keys(), key=lambda x: len(ruledict[x]))
print("sortedrules: ",sortedrules[:5])
order = []
while sortedrules:
    page = sortedrules[0]
    order.append(page)
    del ruledict[page]

    for key, value in ruledict.items():
        if page in value:
            value.remove(page)
    sortedrules = sorted(ruledict.keys(), key=lambda x: len(ruledict[x]))

print("order: ", order) 
#print(updates[:5])
for update in updates:
    uporder = sorted([ [order.index(i), i] for i in update],key=lambda x: x[0])
    #print(uporder)
    update = [ i[1] for i in uporder]

#print(order[:5])
#print(updates[:5])
#  8934 is NOT correct
mids = [ i[len(i)//2] for i in updates]

print("sum of mids of sorted updates", sum(mids))
