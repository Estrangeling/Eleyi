import sys
from collections import namedtuple

Month = namedtuple('Month', 'name number days')

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

def BlackFriday(start, end):
    start = int(start)
    end = int(end)
    years = range(start, end + 1)
    blackfriday = []
    for year in years:
        for i in range(1, 13):
            m = sum(Months[a].days for a in range(i - 1))
            ye = year
            if i <= 2: ye -= 1
            l = ye // 4 - ye // 100 + ye // 400
            d = (year - 1) * 365 + m + 13 + l
            if d % 7 == 5:
                name = Months[i - 1].name
                blackfriday.append(f"{year}, {name} 13, Friday")
    return blackfriday

if __name__ == '__main__':
    start = sys.argv[1]
    end = sys.argv[2]
    print(*BlackFriday(start, end), sep="\n")
