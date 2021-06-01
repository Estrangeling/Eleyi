import sys
import math

def findlcm(numbers):
    numbers = list(map(int, numbers))
    factors = []
    for n in numbers:
        c = 0
        for f in range(2, int(math.sqrt(n)) + 1):
            while n % f == 0:
                c += 1
                n = n // f
                if factors.count(f) < c: factors.append(f)
            c = 0
        if n not in factors: factors.append(n)
    return math.prod(factors)


if __name__ == '__main__':
    numbers = sys.argv[1:]
    print(findlcm(numbers))
