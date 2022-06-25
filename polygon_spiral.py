import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.patches import Arc
from PIL import Image

def sin(d: float): return np.sin(np.radians(d))
def cos(d: float): return np.cos(np.radians(d))
def tan(d: float): return np.tan(np.radians(d))
def atan2(x, y): return np.rad2deg(np.arctan2(y, x))

def rotate(pos, angle, center=(0, 0)):
    cx, cy = center
    px, py = pos
    diff_x, diff_y = (px - cx), (py - cy)
    cosa, sina = cos(angle), sin(angle)
    px1 = cosa * diff_x - sina * diff_y + cx
    py1 = sina * diff_x + cosa * diff_y + cy
    return (px1, py1)

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
    
def increment_rotate(pos1, pos2, rotation):
    x1, y1 = pos1
    x2, y2 = pos2
    side = ((x2-x1)**2+(y2-y1)**2)**.5
    angle = atan2((x2 - x1), (y2 - y1))
    new_x, new_y = x2+side*cos(angle), y2+side*sin(angle)
    new_x, new_y = rotate((new_x, new_y), rotation, (x2, y2))
    return new_x, new_y

def make_polygon(pos1, pos2, sides):
    assert sides >= 3
    unit_rotation = 360/sides
    x1, y1 = pos1
    x2, y2 = pos2
    side = ((x2-x1)**2+(y2-y1)**2)**.5
    positions = [pos1]
    prev_pos = pos2
    cur_pos = pos1
    for i in range(sides-2):
        new_pos = increment_rotate(prev_pos, cur_pos, unit_rotation)
        positions.append(new_pos)
        prev_pos = cur_pos
        cur_pos = new_pos
    
    positions.append(pos2)
    return positions                                                                              

def mid(pos1, pos2):
    (x1, y1), (x2, y2) = [pos1, pos2]
    if x1 > x2:
        x1, x2 = x2, x1
    
    if y1 > y2:
        y1, y2 = y2, y1
    
    return (x1 + (x2 - x1)/2, y1 + (y2 - y1)/2)

def polygon_spiral(unit, iterations, num_colors=12):
    step = 1530/num_colors
    palette = ['#'+spectrum_position(round(step*i), 1) for i in range(num_colors)]
    colors = [palette[0]]
    radius = unit*cos(30)/1.5
    y1 = -radius/2
    x1 = -unit/2
    x2 = unit/2
    points = [(0, radius), (x2, y1), (x1, y1)]
    polygons = [points]
    lines = [[(0, 0), (x1/2, radius/4)], [(0, 0), (0, y1)], [(0, 0), (x2/2, radius/4)]]
    side = 4
    left_start, left_end = points[0], points[2]
    down_start, down_end = points[2], points[1]
    right_start, right_end = points[1], points[0]
    for i in range(iterations):
        left = make_polygon(left_start, left_end, side)
        down = make_polygon(down_start, down_end, side)
        right = make_polygon(right_start, right_end, side)
        polygons.append(left)
        polygons.append(down)
        polygons.append(right)
        colors.extend([palette[(i+1)%num_colors]]*3)
        half = (side/2).__ceil__()
        left_start, left_end = left[half-1:half+1]
        lines[0].append(mid(left_start, left_end))
        down_start, down_end = down[half-1:half+1]
        lines[1].append(mid(down_start, down_end))
        right_start, right_end = right[half-1:half+1]
        lines[2].append(mid(right_start, right_end))
        side += 1

    indices = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    arcs = []
    for i in range(iterations+1, 0, -1):
        points = [lines[j][i] for j in range(3)]
        (x0, y0), (x1, y1), (x2, y2) = points
        dx = x1 - x0
        dy = y1 - y0
        r = (dx*dx + dy*dy)**.5
        
        for k, v in indices.items():
            a, b = points[k]
            thetas = []
            for h in v:
                c, d = points[h]
                angle = atan2(c - a, d - b)
                if angle < 0:
                    angle += 360
                thetas.append(angle)
            theta1, theta2 = thetas
            if theta1 > theta2:
                theta1, theta2 = theta2, theta1
            if not np.isclose(theta2 - theta1, 60):
                theta1, theta2 = theta2 - 360, theta1
            arcs.append([(a, b), r, theta1, theta2])
    
    (x0, y0), (x1, y1), (x2, y2) = [lines[i][-1] for i in range(3)]
    dx = x1 - x0
    dy = y1 - y0
    r = (dx*dx + dy*dy)**.5
    x_values = sorted([x0, x1, x2])
    y_values = sorted([y0, y1, y2])
    x_axis = dict(zip(['min', 'mid', 'max'], x_values))
    y_axis = dict(zip(['min', 'mid', 'max'], y_values))

    inv_indices = {v: k for k, v in indices.items()}
    if np.isclose(x_axis['max'] - x_axis['min'], r):
        x_max, x_min = x_axis['max'], x_axis['min']
    else:
        dx = {abs(x_values[b] - x_values[a]): (a, b) for (a, b) in inv_indices}
        ex = x_values[inv_indices[dx[min(dx)]]]
        if x_axis['min'] == ex:
            x_min = ex
            x_max = x_min + r
        else:
            x_max = ex
            x_min = x_max - r
    
    if np.isclose(y_axis['max'] - y_axis['min'], r):
        y_max, y_min = y_axis['max'], y_axis['min']
    else:
        dy = {abs(y_values[b] - y_values[a]): (a, b) for (a, b) in inv_indices}
        ey = y_values[inv_indices[dy[min(dy)]]]
        if y_axis['min'] == ey:
            y_min = ey
            y_max = y_min + r
        else:
            y_max = ey
            y_min = y_max - r
    
    
    return {'polygons': polygons, 'lines': lines, 'arcs': arcs, 'colors': colors, 'edges': [x_min, x_max, y_min, y_max]}

def plot_polygon_spiral(iterations, unit=1, width=1920, height=1080, lw=2, alpha=1, num_colors=12, arms=True, show=True):
    polygons, lines, arcs, colors, edges = polygon_spiral(unit, iterations, num_colors).values()
    fig = plt.figure(figsize=(width/100, height/100),
                 dpi=100, facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    if arms:
        collection = PolyCollection(polygons, facecolors=colors, lw=lw, alpha=alpha, edgecolor='w')
    else:
        for center, r, theta1, theta2 in arcs:
            ax.add_patch(Arc(center, 2*r, 2*r, theta1=theta1, theta2=theta2, lw=lw, alpha=alpha, edgecolor='w'))
        collection = LineCollection(lines, lw=lw, alpha=alpha, edgecolor='w')
    ax.add_collection(collection)
        
    plt.axis('scaled')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.axis(edges)
    fig.canvas.draw()
    image = Image.frombytes(
        'RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    if not show:
        plt.close(fig)
    else:
        plt.show()
    return image