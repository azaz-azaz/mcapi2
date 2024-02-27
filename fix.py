"""replaces spaces with tabs"""


with open('main.py', 'r') as f:
    text = f.read()

with open('main.py', 'w') as f:
    f.write(text.replace('    ', '\t'))