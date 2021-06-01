import sys
def chira(h, l):
    if l > 4 * h or l < 2 * h:
        return "No Solution"
    elif l % 2 != 0:
        return "No Solution"
    else:
        for i in range(h + 1):
            r = h - i
            if 2 * i + 4 * r == l:
                break
        return "There are {0} chicken and {1} rabbits".format(i, r)

if __name__ == '__main__':
    h = int(sys.argv[1])
    l = int(sys.argv[2])
    print(chira(h, l))
