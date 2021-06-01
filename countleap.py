import sys
def countleap(y):
    a = y // 4
    b = y // 100
    c = y // 400
    l = a - b + c
    return l

if __name__ == '__main__':
    y = int(sys.argv[1])
    print(countleap(y))