import random, re

lines = []

Fillers = ('+', '-', '')

while len(lines) < 6561:
    expression = ''
    n = 0
    for i in range(17):
        if i % 2 == 0:
            n += 1
            expression += str(n)
        else: expression += Fillers[random.randrange(3)]
    if expression not in lines: lines.append(expression)

lines.remove('123456789')

result = []

for line in lines:
    array = re.split('(\-|\+)', line)
    ops = 'add'
    num = 0
    for a in array:
        if a.isdigit():
            if ops == 'add':
                num += int(a)
            else:
                num  -= int(a)
        elif a in Fillers:
            if a == '+':
                ops = 'add'
            else:
                ops = 'sub'
    if num == 100: result.append(line)

result.sort()

print(*result, sep='\n')
