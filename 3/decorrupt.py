import os
import re

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, 'corrupt.txt')

memory = None
with open(data_file_path) as f:
    memory = f.read()

def mul(a, b):
    return a * b

memory1 = re.findall(r'mul\(\d{1,3},\d{1,3}\)', memory)
memory2 = re.findall(r'(don\'t\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\))', memory)

print("sum: ",  sum([eval(m) for m in memory1]))

sum2 = 0
enabled = True
for m in memory2:
    if m == "don't()":
        enabled = False
    elif m == "do()":
        enabled = True
    elif enabled:
        sum2 += eval(m)
#print("memory2: ", memory2)
print("sum2: ", sum2)