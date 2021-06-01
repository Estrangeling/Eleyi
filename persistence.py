import math, sys

def persistence(n):
    if n < 10: return 0
    else:
        chars = str(n)
        i = 0
        result = math.prod([int(y) for y in chars])
        while result > 10:
            i += 1
            result = math.prod([int(y) for y in chars])
            chars = str(result)
        return i

if __name__ == '__main__':
    print(persistence(int(sys.argv[1])))