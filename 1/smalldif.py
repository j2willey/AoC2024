import os

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

for i in range(5):  # len(l1)):
    print(l1[i], l2[i])

print(sum([abs(x-y) for x, y in zip(l1, l2)]))  
