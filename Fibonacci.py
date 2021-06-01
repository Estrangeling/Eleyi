import sys

def Fibonacci(n):
    a, b = 1, 1
    for i in range(n):
        yield a
        a, b = b, a + b

if __name__ == '__main__':
    for i in Fibonacci(int(sys.argv[1])): print(i)