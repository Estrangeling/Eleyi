
import re
import sys
from collections import namedtuple

# Simple data objects are handy as hell. Use more of them.

Month = namedtuple('Month', 'name number days')
Culture = namedtuple('Culture', 'format separator indexes regex')
Date = namedtuple('Date', 'year month day')

Months = (
    Month('January', 1, 31),
    Month('February', 2, 28),
    Month('March', 3, 31),
    Month('April', 4, 30),
    Month('May', 5, 31),
    Month('June', 6, 30),
    Month('July', 7, 31),
    Month('August', 8, 31),
    Month('September', 9, 30),
    Month('October', 10, 31),
    Month('November', 11, 30),
    Month('December', 12, 31),
)

Cultures = (
    Culture('yyyy-MM-dd',    '-', (0,1,2), '^\d{4}\-0?([2-9]|1[0-2]?)\-(0?(3[01]|[12][0-9]|[1-9]))$'),
    Culture('yyyy/MM/dd',    '/', (0,1,2), '^\d{4}\/0?([2-9]|1[0-2]?)\/(0?(3[01]|[12][0-9]|[1-9]))$'),
    Culture('MM/dd/yyyy',    '/', (2,0,1), '^0?([2-9]|1[0-2]?)\/(0?(3[01]|[12][0-9]|[1-9]))\/\d{4}$'),
    Culture('MMM dd, yyyy',  ' ', (2,0,1), '^[A-Za-z]{3} (0?(3[01]|[12][0-9]|[1-9])), \d{4}$'),
    Culture('dd MMM, yyyy',  ' ', (2,1,0), '^(0?(3[01]|[12][0-9]|[1-9])) [A-Za-z]{3}, \d{4}$'),
    Culture('MMMM dd, yyyy', ' ', (2,0,1), '^[A-Za-z]{3,9} (0?(3[01]|[12][0-9]|[1-9])), \d{4}$'),
    Culture('dd MMMM, yyyy', ' ', (2,1,0), '^(0?(3[01]|[12][0-9]|[1-9])) [A-Za-z]{3,9}, \d{4}$'),
    Culture('yyyy, MMM dd',  ' ', (0,1,2), '^\d{4}, [A-Za-z]{3} (0?(3[01]|[12][0-9]|[1-9]))$'),
    Culture('yyyy, MMMM dd', ' ', (0,1,2), '^\d{4}, [A-Za-z]{3,9} (0?(3[01]|[12][0-9]|[1-9]))$'),
)

# A purely stylistic point: organize modules the way you want to read them.
# Most humans like to read things top to bottom.

def main(args):
    start, end = args
    ddate = diffdate(start, end)
    print(ddate)

def diffdate(start, end):
    d1 = totaldays(parsedate(start))
    d2 = totaldays(parsedate(end))
    return d2 - d1

def totaldays(date):
    y = date.year
    if date.month <= 2:
        y -= 1
    leaps = y // 4 - y // 100 + y // 400
    m = sum(Months[b].days for b in range(date.month - 1))
    days = (date.year - 1) * 365 + m + date.day + leaps
    return days

def parsedate(date):
    for c in Cultures:
        if re.match(c.regex, date):
            parts = date.replace(',', '').split(c.separator)
            return Date(
                int(parts[c.indexes[0]]),
                parsemonth(parts[c.indexes[1]]),
                int(parts[c.indexes[2]]),
            )
    # Raise an error if we get here.

def parsemonth(month):
    if month.isdigit():
        return int(month)
    else:
        for m in Months:
            if m.name.lower().startswith(month.lower()):
                return m.number
    # Raise an error if we get here.

if __name__ == '__main__':
    main(sys.argv[1:])