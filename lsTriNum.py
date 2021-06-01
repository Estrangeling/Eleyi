import sys

def lsTriNum(a):
    a = int(a)
    for i in range(2, a):
        yield (i ** 2 - i) // 2

if __name__ == '__main__':
    for i  in lsTriNum(sys.argv[1]): print(i)