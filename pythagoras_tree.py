import math
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from PIL import Image

def sin(d): return math.sin(math.radians(d))
def cos(d): return math.cos(math.radians(d))
def tan(d): return math.tan(math.radians(d))
def atan(d): return math.degrees(math.atan(d))

def spectrum_position(n, string=True):
    if not isinstance(n, int):
        raise TypeError('`n` should be an integer')
    if n < 0:
        raise ValueError('`n` must be non-negative')
    n %= 1530
    if 0 <= n < 255:
        return (255, n, 0) if not string else f'ff{n:02x}00'
    elif 255 <= n < 510:
        return (510-n, 255, 0) if not string else f'{510-n:02x}ff00'
    elif 510 <= n < 765:
        return (0, 255, n-510) if not string else f'00ff{n-510:02x}'
    elif 765 <= n < 1020:
        return (0, 1020-n, 255) if not string else f'00{1020-n:02x}ff'
    elif 1020 <= n < 1275:
        return (n-1020, 0, 255) if not string else f'{n-1020:02x}00ff'
    elif 1275 <= n < 1530:
        return (255, 0, 1530-n) if not string else f'ff00{1530-n:02x}'

def make_square(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    x3 = x1 - dy
    y3 = y1 + dx
    x4 = x3 + dx
    y4 = y3 + dy
    return [pos1, pos2, (x4, y4), (x3, y3)]

def pythagoras_tree(iterations, angle=30, unit=1, num_colors=12, color_start=None):
    assert 0 < angle < 90
    cosa = cos(angle)
    cosa2 = cosa * cosa
    cossina = cosa * sin(angle)
    
    def third_vertex(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx, dy = x2 - x1, y2 - y1
        x3 = dx * cosa2 - dy * cossina + x1
        y3 = dy * cosa2 + dx * cossina + y1
        return x3, y3
    
    if color_start is None:
        color_start = random.random() * 1530
    
    color_step = 1530 / num_colors
    color_values = ['#'+spectrum_position(round(color_start+color_step*i)) for i in range(num_colors)]
    colors = [color_values[0]]
    half = unit/2
    square = [(-half, half), (half, half), (half, -half), (-half, -half)]
    cur_vertices = [square[:2]]
    squares = [square]
    for i in range(1, iterations):
        next_vertices = []
        for pos1, pos2 in cur_vertices:
            other = third_vertex(pos1, pos2)
            square1 = make_square(pos1, other)
            square2 = make_square(other, pos2)
            squares.append(square1)
            squares.append(square2)
            colors.append(color_values[i%num_colors])
            colors.append(color_values[i%num_colors])
            next_vertices.append(square1[-2:][::-1])
            next_vertices.append(square2[-2:][::-1])
        
        cur_vertices = next_vertices
    
    return {'square': squares, 'colors': colors}

def plot_pythagoras_tree(iterations, angle=30, unit=1, num_colors=12, alpha=1, color_start=None, random_colors=False, width=1920, height=1080, show=True):
    fig = plt.figure(figsize=(width/100, height/100),
                     dpi=100, facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    squares, colors = pythagoras_tree(iterations, angle, unit, num_colors, color_start).values()
    colors = colors[::-1]
    if random_colors:
        colors = np.random.rand(len(squares), 3)
    collection = PolyCollection(squares[::-1], facecolors=colors, alpha=alpha)
    ax.add_collection(collection)
    plt.axis('scaled')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    fig.canvas.draw()
    image = Image.frombytes(
        'RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    if not show:
        plt.close(fig)
    else:
        plt.show()
    return image