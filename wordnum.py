import re
import sys

lt100 = {
    'Zero': 0,
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Eleven': 11,
    'Twelve': 12,
    'Thirteen': 13,
    'Fourteen': 14,
    'Fifteen': 15,
    'Sixteen': 16,
    'Seventeen': 17,
    'Eighteen': 18,
    'Nineteen': 19,
    'Twenty': 20,
    'Thirty': 30,
    'Forty': 40,
    'Fifty': 50,
    'Sixty': 60,
    'Seventy': 70,
    'Eighty': 80,
    'Ninety': 90
}

gt100 = {
    'Thousand': 1000,
    'Million': 1e6,
    'Billion': 1e9,
    'Trillion': 1e12,
    'Quadrillion': 1e15,
    'Quintillion': 1e18,
    'Sextillion': 1e21,
    'Septillion': 1e24,
    'Octillion': 1e27,
    'Nonillion': 1e30,
    'Decillion': 1e33,
    'Undecillion': 1e36,
    'Duodecillion': 1e39,
    'Tredecillion': 1e42,
    'Quattuordecillion': 1e45,
    'Quindecillion': 1e48,
    'Sexdecillion': 1e51,
    'Septendecillion': 1e54,
    'Octodecillion': 1e57,
    'Novemdecillion': 1e60,
    'Vigintillion': 1e63,
    'Googol': 1e100,
    'Centillion': 1e303
}

def wordnum(string):
    n = 0
    d = 0
    negative = False
    decimal = False
    string = string.title()
    if re.search('\-| And ', string):
        string = re.sub('\-| And ', ' ', string)
    if ',' in string:
        string = string.replace(',', '')
    words = string.split(' ')
    if words[0] == 'Negative':
        words.remove('Negative')
        negative = True
    if words[0] in gt100.keys() or words[0] == 'Hundred':
        words.insert(0, 'One')
    for i, w in enumerate(words):
        if not decimal:
            if w in lt100.keys():
                d += lt100[w]
            elif w == 'Hundred' and d != 0:
                d *= 100
            elif w in gt100.keys():
                n += d * gt100[w]
                d = 0
        if w == 'Point':
            decimal = True
            p = i
        if decimal and w in lt100.keys():
            n += lt100[w] * 10 ** -(i - p)
    n += d
    if negative:
        n = -n
    return n

if __name__ == '__main__':
    string = sys.argv[1]
    print(wordnum(string))