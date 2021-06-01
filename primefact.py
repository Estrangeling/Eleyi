import math
import sys
def primefact(n):
    while n % 2 == 0:
        yield 2
        n = int(n / 2)
    j = 3
    while n > 1:
        for i in range(j, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                n = int(n / i); j = i
                yield i; break
        else:
            if n > 1:
                yield n; break

n = sys.argv[1]
if n.isdigit() and int(n) > 2:
    n = int(n)
    print(list(primefact(n)))
else:
    print('\x1b[30;3;41m' + 'Error: Inputted string is not an integer greater than two, process will now stop!' + '\x1b[0m')
