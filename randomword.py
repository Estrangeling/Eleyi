import random
from collections import Counter
from string import ascii_lowercase

SAMPLE = Counter({
    'e': 1202,
    't': 910,
    'a': 812,
    'o': 768,
    'i': 731,
    'n': 695,
    's': 628,
    'r': 602,
    'h': 592,
    'd': 432,
    'l': 398,
    'u': 288,
    'c': 271,
    'm': 261,
    'f': 230,
    'y': 211,
    'w': 209,
    'g': 203,
    'p': 182,
    'b': 149,
    'v': 111,
    'k': 69,
    'x': 17,
    'q': 11,
    'j': 10,
    'z': 8
})

pool = list(SAMPLE.elements())
randpool = []

while len(pool) > 0:
    elem = random.choice(pool)
    randpool.append(elem)
    pool.remove(elem)

LETTERS = set(ascii_lowercase)
VOWELS = set('aeiouy')
CONSONANTS = LETTERS - VOWELS

TAILS = {
    'a': CONSONANTS,
    'b': 'bjlr',
    'c': 'chjklr',
    'd': 'dgjw',
    'e': CONSONANTS,
    'f': 'fjlr',
    'g': 'ghjlrw',
    'h': '',
    'i': CONSONANTS,
    'j': '',
    'k': 'hklrvw',
    'l': 'l',
    'm': 'cm',
    'n': 'gn',
    'o': CONSONANTS,
    'p': 'fhlprst',
    'q': '',
    'r': 'hrw',
    's': 'chjklmnpqstw',
    't': 'hjrstw',
    'u': CONSONANTS,
    'v': 'lv',
    'w': 'hr',
    'x': 'h',
    'y': 'sv',
    'z': 'hlvw'
}

# variables expanded:
# w: Word, r: Random Letter, sc: Serial Consonants count, sv: Serial Vowels Count, ss: Serial Same-letter count, lm: Max Length of tails, l: Length of tails

def randomword():
    count = random.randint(1, 4)
    heads = [random.choice(randpool) for i in range(count)]
    i = 0
    segments = []
    while count > 0:
        sc, ss, sv = 0, 0, 0 
        w = heads[i]
        if w in CONSONANTS: sc += 1
        else: sv += 1
        while True:
            r = random.choice(randpool)
            if r in TAILS[w] or r in VOWELS:
                if i == 0 and r == w: continue
                else:
                    if r in VOWELS:
                        sc = 0
                        sv += 1
                        break
                    else:
                        sv = 0
                        sc += 1
                        break
        w += r
        l = 1
        lm = random.randint(2, 5)
        while True:
            if l == lm:
                segments.append(w)
                count -= 1
                break
            f = r
            r = random.choice(randpool)
            if r in TAILS[f] or r in VOWELS:
                if r in VOWELS:
                    sc = 0
                    sv += 1
                elif r in CONSONANTS:
                    sv = 0
                    sc += 1
                if sv == 3 or sc == 3: continue
                if r != f: ss = 0
                if r == f and ss == 1: continue
                if r == f: ss += 1
                w += r
                l += 1
                if random.getrandbits(1):
                    segments.append(w)
                    count -= 1
                    break
        i += 1
    return ''.join(segments)

if __name__ == '__main__':
    print(randomword())
