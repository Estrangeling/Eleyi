import math
import sys

def factorise(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for f in range(3, int(math.sqrt(n)) + 1, 2):
        while n % f == 0:
            factors.append(f)
            n = n // f
    if n > 1: factors.append(n)
    return factors


if __name__ == '__main__':
    n = sys.argv[1]
    if n.isdigit() and int(n) > 2:
        n = int(n)
        print(factorise(n))
    else:
        print('\x1b[30;3;41m' + 'Error: Inputted string is not an integer greater than two, process will now stop!' + '\x1b[0m')
