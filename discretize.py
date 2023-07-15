import random
from typing import Any, List, Tuple


def get_unique_numbers(num: int, lim: int) -> List[int]:
    numbers = range(lim)
    choices = set(random.choices(numbers, k=num))
    remaining = list(set(numbers) - choices)
    while len(choices) != num:
        choice = random.choice(remaining)
        remaining.remove(choice)
        choices.add(choice)
    return sorted(choices)


def take_ends(ranges: List[List[int]], stack: List[List[int]], top: List[int]) -> None:
    ranges.append([top[0], top[-1]])
    stack.append(top[1:-1])


def take_middle(
    l: int, ranges: List[List[int]], stack: List[List[int]], top: List[int]
) -> None:
    n = l // 3
    n += n % 2
    index = random.randrange(n, 2 * n, 2)
    ranges.append(top[index : index + 2])
    stack.extend([top[:index], top[index + 2 :]])


def split(l: int, stack: List[List[int]], top: List[int]) -> None:
    index = random.randrange(2, l - 2, 2)
    stack.extend([top[:index], top[index:]])


def handle_choices(
    l: int, ranges: List[List[int]], stack: List[List[int]], top: List[int]
) -> None:
    choice = random.randrange(3)
    if not choice:
        take_ends(ranges, stack, top)
    elif choice == 1:
        take_middle(l, ranges, stack, top)
    else:
        split(l, stack, top)


def make_sample(num: int, lim: int, dat: int) -> List[Tuple[int]]:
    num *= 2
    if num > lim:
        lim = num * random.randrange(1, 6)

    stack = [get_unique_numbers(num, lim)]
    ranges = []
    while stack:
        top = stack.pop(0)
        if (l := len(top)) == 2:
            ranges.append(top)
        elif l == 4:
            ranges.extend([top[:2], top[2:]])
        else:
            handle_choices(l, ranges, stack, top)
    return [
        (a, b, random.randrange(dat))
        for a, b in sorted(ranges, key=lambda x: (x[0], -x[1]))
    ]


def get_nodes(ranges: List[Tuple[int, int, Any]]) -> List[Tuple[int, int, Any]]:
    nodes = []
    for ini, fin, data in ranges:
        nodes.extend([(ini, False, data), (fin, True, data)])
    return sorted(nodes)


def merge_ranges(data: List[List[int | Any]], range: List[int | Any]) -> None:
    if not data or range[2] != (last := data[-1])[2] or range[0] > last[1] + 1:
        data.append(range)
    else:
        last[1] = range[1]


def discretize_narrow(ranges):
    nodes = get_nodes(ranges)
    output = []
    stack = []
    actions = []
    for node, end, data in nodes:
        if not end:
            action = False
            if not stack or data != stack[-1]:
                if stack and start < node:
                    merge_ranges(output, [start, node - 1, stack[-1]])
                stack.append(data)
                start = node
                action = True
            actions.append(action)
        elif actions.pop(-1):
            if start <= node:
                merge_ranges(output, [start, node, stack.pop(-1)])
                start = node + 1
            else:
                stack.pop(-1)
    return output

def get_quadruples(ranges):
    nodes = []
    for ini, fin, data in ranges:
        nodes.extend([(ini, False, -fin, data), (fin, True, ini, data)])
    return sorted(nodes)



def brute_force_discretize(ranges):
    numbers = {}
    ranges.sort(key=lambda x: (x[0], -x[1]))
    for start, end, data in ranges:
        numbers |= {n: data for n in range(start, end + 1)}
    numbers = list(numbers.items())
    l = len(numbers)
    i = 0
    output = []
    while i < l:
        di = 0
        curn, curv = numbers[i]
        while i != l and curn + di == numbers[i][0] and curv == numbers[i][1]:
            i += 1
            di += 1
        output.append((curn, numbers[i-1][0], curv))
    return output

def compare_output(ranges):
    return list(map(tuple, discretize_narrow(ranges))) == brute_force_discretize(ranges)

if __name__ == '__main__':
    print(discretize_narrow([(0, 10, 'A'), (0, 1, 'B'), (2, 5, 'C'), (3, 4, 'C'), (6, 7, 'C'), (8, 8, 'D'), (110, 150, 'E'), (250, 300, 'C'), (256, 270, 'D'), (295, 300, 'E'), (500, 600, 'F')]))
    print(discretize_narrow([(0, 100, 'A'), (10, 25, 'B'), (15, 25, 'C'), (20, 25, 'D'), (30, 50, 'E'), (40, 50, 'F'), (60, 80, 'G'), (150, 180, 'H')]))
    for _ in range(256):
        assert compare_output(make_sample(256, 1024, 8))