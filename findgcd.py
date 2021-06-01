import math
import sys
from collections import Counter
from functools import reduce

def factors(n):
    factors = Counter({1: 1})
    for f in range(2, int(math.sqrt(n)) + 1):
        while n % f == 0:
            factors[f] += 1
            n = n // f
    if n > 1: factors[n] += 1
    return factors

def gcd(x, y):
    return math.prod((factors(x) & factors(y)).elements())

if __name__ == '__main__':
    print(reduce(gcd, map(int, sys.argv[1:])))