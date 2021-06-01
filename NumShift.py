import re
import sys
from collections import namedtuple

kind = namedtuple('kind', 'name header max regex slicer')

SWITCH = {'b': 0, 'd': 1, 'h': 2, 'i': 3, 'o': 4}

HEXD = (
    '0', '1', '2', '3',
    '4', '5', '6', '7',
    '8', '9', 'a', 'b',
    'c', 'd', 'e', 'f'
)

TYPES = (
    kind('binary number', '0b', '0b'+'1'*32, '^(0b)?[01]+$', '([01])'),
    kind('decimal natural', None, 4294967295, '^\d+$', None),
    kind('hexadecimal number', '0x', '0x'+'f' * 8, '^(0x)?[\da-f]+$', '([\da-f])'),
    kind('IPv4 address', None, '255.255.255.255', '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', '\.'),
    kind('octal number', '0o', '0o'+'3'+'7'*10, '^(0o)?[0-7]+$', '([0-7])')
)

ERR = (
    "InvalidData: The inputted string isn't a valid {0}, process will now stop.",
    "LimitsExceeded: The value of the inputted {0} exceeds the maximum IPv4 value possible, process will now stop.(maximum value allowed: {1})",
    'InvalidOperation: The operation specified is undefined, process will now stop.',
    "InvalidOperation: The number of arguments passed to the script isn't three, process will now stop"
)


def splitter(regex, val):
    return list(filter(''.__ne__, re.split(regex, val)))


def showerror(msg):
    return '\x1b[30;3;41m' + msg + '\x1b[0m'


def weights(val, base):
    expos = []
    a, b = 1, 0
    while a <= val:
        expos.append(b)
        a *= base
        b += 1
    expos.reverse()
    return expos


def converter(val, a, b):
    if b == 1:
        val.reverse()
        k = (1, None, 4, 8, 3)
        if a in (0, 3, 4):
            val = list(map(int, val))
        elif a == 2:
            val = [HEXD.index(i) for i in val]
        return sum([int(n) << k[a] * p for p, n in enumerate(val)])
    elif a == 1:
        c = ((2, 1), None, (16, 4), (256, 8), (8, 3))
        d, e = c[b]
        bits = []
        if b in (0, 2, 4):
            digits = weights(val, d)
        elif b == 3:
            digits = (3, 2, 1, 0)
        for f in digits:
            bit = (val >> e * f) % d
            if b in (0, 3, 4):
                bits.append(str(bit))
            elif b == 2:
                bits.append(HEXD[bit])
        if b in (0, 2, 4):
            return TYPES[b].header + ''.join(bits)
        elif b == 3:
            return '.'.join(bits)


def main(val, a, b):
    if re.match(TYPES[a].regex, val):
        if b != 3:
            if a == 1:
                val = int(val)
                return converter(val, 1, b)
            else:
                bits = splitter(TYPES[a].slicer, val.lstrip(TYPES[a].header))
                decv = converter(bits, a, 1)
                if b == 1:
                    return decv
                else:
                    return converter(decv, 1, b)
        else:
            if a == 1:
                decv = int(val)
            else:
                decv = main(val, a, 1)
            if decv <= 4294967295:
                return converter(decv, 1, 3)
            else:
                return showerror(ERR[1].format(TYPES[a].name, TYPES[a].max))
    else:
        return showerror(ERR[0].format(TYPES[a].name))


if __name__ == '__main__':
    if len(sys.argv[1:]) == 3:
        val, x, y = sys.argv[1:]
        if {x, y}.issubset(SWITCH.keys()) and x != y:
            x = SWITCH[x]
            y = SWITCH[y]
            print(main(val, x, y))
        else:
            print(showerror(ERR[2]))
    else:
        print(showerror(ERR[3]))
