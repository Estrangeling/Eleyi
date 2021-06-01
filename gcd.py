import math
import sys

def factors(n):
    factors = {'1': 1}
    f = 2
    while f <= int(math.sqrt(n)):
        while n % f == 0:
            if f'{f}' in factors.keys():
                factors.update({f'{f}': factors[f'{f}'] + 1})
            else:
                factors[f'{f}'] = 1
            n = int(n / f)
        f += 1
    if n > 1: factors[f'{n}'] = 1
    return factors

def gcd(x, y):
    f1 = factors(x)
    f2 = factors(y)
    for f in f1.copy().keys():
        if f not in f2.keys():
            f1.pop(f)
        elif f1[f] > f2[f]:
            f1[f'{f}'] = f2[f]
    cd = 1
    for f in f1.keys():
        cd *= int(f) ** f1[f]
    return cd

def main(args):
    args = list(map(int, args))
    cd = gcd(args[0], args[1])
    if len(args) > 2:
        for i in args[2:]:
            cd = gcd(cd, i)
    print(cd)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
