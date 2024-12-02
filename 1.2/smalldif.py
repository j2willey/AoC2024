import os
from collections import Counter 

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'data.txt')

with open(data_file_path) as f:
    lines = f.readlines()

l1 = []
l2 = []

for line in lines:
    nums = line.split()
    l1.append(int(nums[0]))
    l2.append(int(nums[1]))

l1.sort()
l2.sort()
l2counts = Counter(l2)

simscore = 0

for i in range(len(l1)):
    if l1[i] in l2counts:
        simscore +=  l2counts[l1[i]] * l1[i]
    print(l1[i], l2[i])

print(simscore)  
