import math
import sys

def countprime(r):
    r = int(r)
    primes = []
    for n in range(r + 1):
        if n in [2, 3]:
            primes.append(n)
        elif n > 3:
            prime = True
            sqrt = math.sqrt(n)
            if sqrt.is_integer():
                prime = False
            else:
                for i in range(2, int(sqrt) + 1):
                    if n % i == 0:
                        prime = False
                        break
            if prime:
                primes.append(n)
    return len(primes)

if __name__ == '__main__':
    print(countprime(sys.argv[1]))