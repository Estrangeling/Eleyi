import sys
def headleg(h, l):
    if l > 4 * h or l < 2 * h:
        return "No Solution"
    elif l % 2 != 0:
        return "No Solution"
    else:
        x = (4 * h - l) // 2
        y = h - x
        return f"There are {x} chicken and {y} rabbits"

if __name__ == '__main__':
    h = int(sys.argv[1])
    l = int(sys.argv[2])
    print(headleg(h, l))
