import re

array = [[0, 0, 0, 0, 0, 0, 0, 0]]
elems = [0, 0, 0, 0, 0, 0, 0, 0]

for n in range(6560):
    copy = elems.copy()
    copy[-1] += 1
    while 3 in copy:
        i = copy.index(3)
        copy[i:] = [0] * (len(copy) - i)
        copy[i - 1] += 1
    array.append(copy)
    elems = copy

lines = []

Fillers = ('+', '-', '')

j = 0

while len(lines) < 6561:
    expression = ''
    i, k = 0, 0
    for n in range(17):
        if n % 2 == 0:
            i += 1
            expression += str(i)
        else:
            expression += Fillers[array[j][k]]
            k += 1
    lines.append(expression)
    j += 1

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