import sys

def steps(base, num):
    array = [[0]]
    elems = [0]
    for n in range(num - 1):
        copy = elems.copy()
        copy[-1] += 1
        while base in copy:
            i = copy.index(base)
            copy[i:] = [0] * (len(copy) - i)
            if i != 0:
                copy[i - 1] += 1
            else:
                copy.insert(0, 1)
        array.append(copy)
        elems = copy
    return array

if __name__ == '__main__':
    base, num =  map(int, sys.argv[1:])
    print(*steps(base, num), sep='\n')