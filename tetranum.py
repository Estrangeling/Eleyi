import sys

def tetranum(a):
    a = int(a)
    b, s = 0, 0
    for i in range(a):
        b = b + i
        s = s + b
        yield s

if __name__ == '__main__':
    for i in tetranum(sys.argv[1]): print(i)