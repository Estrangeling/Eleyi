import re
import sys

NIBBLES = (
    ('0000', 0,  '0'),
    ('0001', 1,  '1'),
    ('0010', 2,  '2'),
    ('0011', 3,  '3'),
    ('0100', 4,  '4'),
    ('0101', 5,  '5'),
    ('0110', 6,  '6'),
    ('0111', 7,  '7'),
    ('1000', 8,  '8'),
    ('1001', 9,  '9'),
    ('1010', 10, 'a'),
    ('1011', 11, 'b'),
    ('1100', 12, 'c'),
    ('1101', 13, 'd'),
    ('1110', 14, 'e'),
    ('1111', 15, 'f')
)

TYPES = (
    ('binary number', '0b' + '1' * 32),
    ('decimal natural number', 4294967295),
    ('hexadecimal number', '0x' + 'f' * 8),
    ('IPv4 address', '255.255.255.255'),
    ('octal number', '0o' + '3' + '7' * 10)
)

ERR = (
    "InvalidData: The inputted string isn't a valid {0}, process will now stop.",
    "LimitsExceeded: The value of the inputted {0} exceeds the maximum IPv4 value possible, process will now stop.(maximum value allowed: {1})"
)

HEADERS = ('0b', '0d', '0x', 'ip', '0o')


def splitter(regex, inv):
    return list(filter(''.__ne__, re.split(regex, inv)))


def translator(inv, task):
    a, b = task
    outv = []
    for i in inv:
        for j in NIBBLES:
            if j[a] == i:
                outv.append(j[b])
    if b == 1:
        outv.reverse()
    return outv


def worker(inv, bits, task):
    outv = []
    for bit in bits:
        if inv >= bit:
            n = inv // bit
            inv = inv % bit
            if task in (0, 2):
                for i in NIBBLES:
                    if i[1] == n:
                        outv.append(i[task])
            elif task in (3, 4):
                outv.append(str(n))
        elif inv < bit and task in (0, 2):
            outv.append(NIBBLES[0][task])
        elif inv < bit and task in (3, 4):
            outv.append('0')
    return outv


def converter(inv, task, base):
    bits = []
    if task == 1:
        decv = 0
        for p, n in enumerate(inv):
            decv += n * base ** p
        return decv
    elif task in (0, 2, 4):
        i = 1
        while i <= inv:
            bits.append(i)
            i *= base
        bits.reverse()
        return HEADERS[task] + ''.join(worker(inv, bits, task)).lstrip('0')
    elif task == 3:
        for i in range(3, -1, -1):
            bits.append(base ** i)
        return '.'.join(worker(inv, bits, 3))


def binsub(binv, task):
    if re.match('^(0b)?[01]+$', binv):
        binv = binv.replace('0b', '')
        if task in (1, 2):
            if len(binv) % 4 > 0:
                binv = binv.zfill(4 * (len(binv) // 4 + 1))
            bits = translator(splitter('([01]{4})', binv), (0, task))
            if task == 1:
                return converter(bits, 1, 16)
            elif task == 2:
                return '0x' + ''.join(bits).lstrip('0')
        elif task == 4:
            bits = translator(splitter('([01]{4})', binv), (0, 1))
            return decsub(converter(bits, 1, 16), 4)
        elif task == 3:
            if re.match('^[01]{1,32}$', binv):
                return converter(binsub(binv, 1), 3, 256)
            else:
                print('\x1b[30;3;41m' + ERR[1].format(TYPES[0][0], TYPES[0][1]) + '\x1b[0m')
    else:
        print('\x1b[30;3;41m' + ERR[0].format(TYPES[0][0]) + '\x1b[0m')


def decsub(decv, task):
    if str(decv).isdigit():
        decv = int(decv)
        if task in (0, 2):
            return converter(decv, task, 16)
        elif task == 4:
            return converter(decv, 4, 8)
        elif task == 3:
            if decv <= 4294967295:
                return converter(decv, 3, 256)
            else:
                print('\x1b[30;3;41m' + ERR[1].format(TYPES[1][0], TYPES[1][1]) + '\x1b[0m')
    else:
        print('\x1b[30;3;41m' + ERR[0].format(TYPES[1][0]) + '\x1b[0m')


def hexsub(hexv, task):
    hexv = hexv.lower()
    if re.match('^(0x)?[0-9a-f]+$', hexv):
        hexv = hexv.replace('0x', '')
        if task in (0, 1):
            bits = translator(splitter('([0-9a-f])', hexv), (2, task))
            if task == 0:
                return '0b' + ''.join(bits).lstrip('0')
            elif task == 1:
                return converter(bits, 1, 16)
        elif task == 4:
            bits = translator(splitter('([0-9a-f])', hexv), (2, 1))
            return decsub(converter(bits, 1, 16), 4)
        elif task == 3:
            if re.match('^[0-9a-f]{1,8}$', hexv):
                return converter(hexsub(hexv, 1), 3, 256)
            else:
                print('\x1b[30;3;41m' + ERR[1].format(TYPES[2][0], TYPES[2][1]) + '\x1b[0m')
    else:
        print('\x1b[30;3;41m' + ERR[0].format(TYPES[2][0]) + '\x1b[0m')


def ip4sub(ipv, task):
    if re.match('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', ipv):
        segs = list(map(int, ipv.split('.')))
        segs.reverse()
        decv = converter(segs, 1, 256)
        if task == 1:
            return decv
        elif task in (0, 2, 4):
            return decsub(decv, task)
    else:
        print('\x1b[30;3;41m' + ERR[0].format(TYPES[3][0]) + '\x1b[0m')


def octsub(octv, task):
    if re.match('^(0o)?[0-7]+$', octv):
        octv = octv.replace('0o', '')
        bits = list(map(int, splitter('([0-7])', octv)))
        bits.reverse()
        decv = converter(bits, 1, 8)
        if task == 1:
            return decv
        elif task in (0, 2):
            return decsub(decv, task)
        elif task == 3:
            if decv <= 4294967295:
                return decsub(decv, 3)
            else:
                print('\x1b[30;3;41m' + ERR[1].format(TYPES[4][0], TYPES[4][1]) + '\x1b[0m')
    else:
        print('\x1b[30;3;41m' + ERR[0].format(TYPES[4][0]) + '\x1b[0m')


def main(inv, task):
    a, b = task
    tasks = {'b': 0, 'd': 1, 'h': 2, 'i': 3, 'o': 4}
    if {a, b}.issubset(tasks.keys()) and a != b:
        if a == 'b':
            print(binsub(inv, tasks[b]))
        elif a == 'd':
            print(decsub(inv, tasks[b]))
        elif a == 'h':
            print(hexsub(inv, tasks[b]))
        elif a == 'i':
            print(ip4sub(inv, tasks[b]))
        elif a == 'o':
            print(octsub(inv, tasks[b]))
    else:
        print('\x1b[30;3;41m' + 'InvalidOperation: The operation specified is undefined, process will now stop.' + '\x1b[0m')


if __name__ == '__main__':
    inv, task = sys.argv[1:]
    main(inv, task)
