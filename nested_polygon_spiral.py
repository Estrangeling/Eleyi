import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection, PolyCollection
from PIL import Image

def sin(d): return np.sin(np.radians(d))
def cos(d): return np.cos(np.radians(d))
def tan(d): return np.tan(np.radians(d))
def cot(d): return 1/tan(d)
def atan2(y, x): return np.rad2deg(np.arctan2(y, x))

def spectrum_position(n, string=False):
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

def rotate(pos, angle, center=(0, 0)):
    cx, cy = center
    px, py = pos
    diff_x, diff_y = (px - cx), (py - cy)
    cosa, sina = cos(angle), sin(angle)
    px1 = cosa * diff_x - sina * diff_y + cx
    py1 = sina * diff_x + cosa * diff_y + cy
    return (px1, py1)

def initial_position(unit, sides):
    assert sides >= 3
    half = unit/2
    angle = 180/sides
    return (half, -half/tan(angle))

def make_polygon(init_pos, sides):
    assert sides >= 3
    angle = 360/sides
    points = [init_pos]
    for i in range(1, sides):
        points.append(rotate(init_pos,angle*i))
    
    return points

def displace_ratio(beta, angle):
    return 1 / (1 + cos(beta) + sin(beta) * cot(angle))

def displace(pos1, pos2, d):
    x1, y1 = pos1
    x2, y2 = pos2
    angle = atan2((y2 - y1), (x2 - x1))
    return (x1 + d*cos(angle), y1 + d*sin(angle))

def nested_polygon_spiral(sides, angle, iterations, unit=1, num_colors=12):
    assert sides >= 3
    assert iterations > 1
    beta = 180 * (sides - 2) / sides
    ratio = displace_ratio(beta, angle)
    step = 1530/num_colors
    color_values = ['#'+spectrum_position(round(step*i), 1) for i in range(num_colors)]
    polygons = []
    colors = ['#ff0000']
    init_pos = initial_position(unit, sides)
    first_polygon = make_polygon(init_pos, sides)
    polygons.append(first_polygon)
    second_pos = first_polygon[1]
    for i in range(1, iterations):
        init_pos = displace(init_pos, second_pos, unit*ratio)
        polygon = make_polygon(init_pos, sides)
        polygons.append(polygon)
        second_pos = polygon[1]
        x1, y1 = init_pos
        x2, y2 = second_pos
        unit = ((x2 - x1)**2 + (y2 - y1)**2)**.5
        colors.append(color_values[i % num_colors])
    return {'polygons': polygons, 'colors': colors}

def plot_nested_polygon_spiral(sides, angle, iterations, unit=1, width=1920, height=1080, lw=2, alpha=1, num_colors=12, show=True):
    assert sides >= 3
    fig = plt.figure(figsize=(width/100, height/100), dpi=100, facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    data = nested_polygon_spiral(sides, angle, iterations, unit, num_colors)
    polygons, colors = data.values()
    ax.add_collection(PolyCollection(polygons, facecolors=colors, lw=lw, alpha=alpha, edgecolor='w'))
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
