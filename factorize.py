import math
import sys

def factorize(n):
    for f in range(2, int(math.sqrt(n)) + 1):
        while n % f == 0:
            yield f
            n = n // f
    if n > 1:
        yield n

if __name__ == '__main__':
    n = int(sys.argv[1])
    for i in factorize(n): print(i)
