import sys

def TriNum(a):
    a = int(a)
    b = 0
    for i in range(a):
        b = b + i
        yield b

if __name__ == '__main__':
    for i in TriNum(sys.argv[1]): print(i)