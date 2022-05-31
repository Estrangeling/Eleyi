import math
import matplotlib.pyplot as plt
from random import random
from matplotlib.patches import Ellipse

def tan(d): return math.tan(math.radians(d))
def sin(d): return math.sin(math.radians(d))
def cos(d): return math.cos(math.radians(d))
def atan(n): return math.degrees(math.atan(n))

def random_point(a, b):
    d = random()*360
    return (a * cos(d) * random(), b * sin(d) * random())

SPECIAL = (-360, -270, -180, -90, 0, 90, 180, 270, 360)
SPECIAL_ANGLES = [tan(i) for i in SPECIAL]
NINTIES = ('HORIZONTAL', 'VERTICAL')

def make_ellipse(a, d):
    assert 0 < d < 45
    b = a * tan(d)
    return (a, b)

def make_line(pos, d):
    x, y = pos
    if d in SPECIAL:
        if d in (-270, -90, 90, 270):
            return ('VERTICAL', x)
        return ('HORIZONTAL', y)
    k = tan(d)
    c = -x*k + y
    return (k, c)

def intersection(k, c, a, b):
    assert c**2 < a**2 * k**2 + b**2
    n1 = a**2 * k**2 + b**2
    n2 = 2 * a**2 * k * c
    n3 = a**2 * (c**2 - b**2)
    n4 = (n2**2 - 4 * n1 * n3) ** .5
    x0 = (-n2 + n4) / (2 * n1)
    x1 = (-n2 - n4) / (2 * n1)
    y0 = k * x0 + c
    y1 = k * x1 + c
    return [(x0, y0), (x1, y1)]

def special_intersection(dimension, value, a, b):
    assert dimension in NINTIES
    if dimension == 'VERTICAL':
        x = value
        assert abs(x) < a
        y0 = (b**2 - x**2 * b**2 / a**2) ** .5
        return [(x, y0), (x, -y0)]
    y = value
    assert abs(y) < b
    x0 = (a**2 - y**2 * a**2 / b**2) ** .5
    return [(x0, y), (-x0, y)]
        

def tangent(x, y, a, b):
    assert math.isclose(x**2 / a**2 + y**2 / b**2, 1)
    k = -x * b**2 / (a**2 * y)
    if k not in SPECIAL_ANGLES:
        c = b**2 / y
        return (k, c)
    if SPECIAL_ANGLES.index(k) in (1, 3, 5, 7):
        return ('VERTICAL', x)
    return ('HORIZONTAL', y)

def perpendicular(k, x, y):
    k1 = -1/k
    c = y - k1*x
    return (k1, c)

def special_perpendicular(dimension, x, y):
    assert dimension in NINTIES
    if dimension == 'VERTICAL':
        return ('HORIZONTAL', y)
    return ('VERTICAL', x)

def reflect(k1, k2, x, y):
    a1 = atan(k1)
    a2 = atan(k2)
    diff_a = a2 - a1
    diff_a = (diff_a + 180) % 360 - 180
    a3 = a2 + diff_a
    if a3 not in SPECIAL:
        k = tan(a3)
        c = y - k * x
        return (k, c)
    if a3 in (-270, -90, 90, 270):
        return ('VERTICAL', x)
    return ('HORIZONTAL', y)

def special_reflect(dimension, k, x, y, reverse=False):
    assert dimension in NINTIES
    a = atan(k)
    if not reverse:
        diff_a = a - 90 if dimension == 'VERTICAL' else a - 180
    else:
        diff_a = 90 - a if dimension == 'VERTICAL' else 180 - a
    diff_a = (diff_a + 180) % 360 - 180
    a1 = a + diff_a
    k = tan(a1)
    c = y - k * x
    return (k, c)

def bounce(k1, x, y, a, b):
    tan_k, tan_c = tangent(x, y, a, b)
    if tan_k not in NINTIES:
        perp_func = perpendicular
    else:
        perp_func = special_perpendicular
    
    perp_k, perp_c = perp_func(tan_k, x, y)
    
    if perp_k not in NINTIES and k1 not in NINTIES:
        refl_k, refl_c = reflect(k1, perp_k, x, y)
    else:
        reverse = False
        if perp_k in NINTIES:
            reverse = True
        refl_k, refl_c = special_reflect(k1, perp_k, x, y, reverse)
    
    if refl_k not in NINTIES:
        inte_func = intersection
    else:
        inte_func = special_intersection
    
    intersects = inte_func(refl_k, refl_c, a, b)
    index = 1
    new_x, new_y = intersects[0]
    if not math.isclose(new_x, x) and not math.isclose(new_y, y):
        index = 0
    
    next_x, next_y = intersects[index]
    return (refl_k, refl_c, next_x, next_y)
        

def recursive_reflect(a, b, pos=None, angle=None, iterations=360):
    if pos:
        init_x, init_y = pos
        assert init_x**2 / a**2 + init_y**2 / b**2 <= 1
    else:
        pos = random_point(a, b)
        init_x, init_y = pos
    
    if not angle:
        angle = random()*360
    
    segments = []
    k, c = make_line(pos, angle)
    if k not in NINTIES:
        func = intersection
    else:
        func = special_intersection
    
    intersects = func(k, c, a, b)
    index = 1
    if 0 <= angle < 90 or 270 <= angle < 360:
        if intersects[0][0] >= init_x:
            index = 0
    
    elif intersects[0][0] <= init_x:
        index = 0
    
    sect_x, sect_y = intersects[index]
    
    segments.append([(init_x, init_y), (sect_x, sect_y)])
    
    start_x, start_y = sect_x, sect_y
    current_k = k
    for i in range(iterations):
        refl_k, refl_c, next_x, next_y = bounce(current_k, start_x, start_y, a, b)
        next_pos = (next_x, next_y)
        segments.append([(start_x, start_y), next_pos])
        
        start_x, start_y = next_x, next_y
        current_k = refl_k
    
    return segments

def plot_reflections(a=4, d=30, iterations=360):
    a, b = make_ellipse(a, d)
    segments = recursive_reflect(a, b, iterations=iterations)
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(1,1,1)
    ax.set_axis_off()
    ax.add_patch(Ellipse((0, 0), 2*a, 2*b, edgecolor='k', fc='None', lw=2))
    for segment in segments:
        x, y = zip(*segment)
        ax.plot(x, y)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.axis('scaled')
    plt.box(False)
    ax = plt.gca()
    ax.set_xlim([-a, a])
    ax.set_ylim([-b, b])
    plt.show()

plot_reflections()