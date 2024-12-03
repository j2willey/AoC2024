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

memory = re.findall(r'mul\(\d{1,3},\d{1,3}\)', memory)

print("sum: ",  sum([eval(m) for m in memory]))