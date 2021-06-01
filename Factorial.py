import sys
def factorial(n):
    n = int(n)
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f

if __name__ == '__main__':
    n = sys.argv[1]
    print(factorial(n))
