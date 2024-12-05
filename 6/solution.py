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
