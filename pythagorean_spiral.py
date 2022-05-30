import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection, PolyCollection
from PIL import Image
from scipy.interpolate import splprep, splev

def sin(d: float): return np.sin(np.radians(d))
def cos(d: float): return np.cos(np.radians(d))
def tan(d: float): return np.tan(np.radians(d))
def atan2(x, y): return np.rad2deg(np.arctan2(y, x))

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

def fibonacci(limit):
    a, b = 0, 1
    numbers = set()
    while a <= limit:
        numbers.add(a)
        a, b = b, a + b
    
    return numbers

def squares(limit):
    return {i for i in range(limit+1) if (i**.5).is_integer()}


def primes(limit):
    a = [True] * limit                       
    a[0] = a[1] = False
    numbers = set()
    for (i, isprime) in enumerate(a):
        if isprime:
            numbers.add(i)
            for n in range(i*i, limit, i):
                a[n] = False
    
    return numbers

def squared_primes(limit):
    prime = sorted(primes(limit))
    numbers = set()
    for i in prime:
        numbers.add(i*i)
        if i*i >= limit:
            break
    
    return numbers

def prime_fibonacci(limit):
    fibnum = fibonacci(limit)
    prime = primes(limit)
    return prime & fibnum

def triple_spiral(limit):
    arms = dict()
    for i in range(limit+1):
        root = i**.5
        if root.is_integer():
            arms[i] = int(root%3)
    
    return arms

filters = {fibonacci, squares, primes, prime_fibonacci, squared_primes, triple_spiral}        

def pythogorean_spiral(iterations, mode='rim', num_colors=12, condition=None):
    assert mode in ('rim', 'radial', 'triangles')
    if condition:
        assert condition in filters
        filtered = condition(iterations)
    step = 1530/num_colors
    color_values = ['#'+spectrum_position(round(step*i), 1) for i in range(num_colors)]
    vertices = []
    if condition != triple_spiral:
        colors = ['#ff0000']
        collection = []
    else:
        arms = [[], [], []]
        cur_arms = [(1, 0), None, None]
        colors = [[], [], []]
        cur_arm_indices = [0, 0, 0]
        arm_vertices = [[(1, 0)], [], []]
    
    if not condition or 0 in filtered:
        vertices.append((1, 0))
        if condition != triple_spiral:
            if mode == 'rim':
                collection.append([(1, 0), (1, 1)])
            
            if mode == 'radial':
                collection.append([(0, 0), (1, 0)])
            
            elif mode == 'triangles':
                collection.append([(0, 0), (1, 0), (1, 1)])
    
    cur_x, cur_y = 1, 1
    for i in range(1, iterations):
        radius = (cur_x ** 2 + cur_y ** 2) ** .5
        new_radius = radius + 1
        angle = atan2(cur_x, cur_y)
        new_x, new_y = new_radius*cos(angle), new_radius*sin(angle)
        new_x, new_y = rotate((new_x, new_y), 90, (cur_x, cur_y))
        if not condition or i in filtered:
            vertices.append((cur_x, cur_y))
            if condition != triple_spiral:
                color = color_values[i % num_colors]
                colors.append(color)
                if mode  == 'rim':
                    collection.append([(cur_x, cur_y), (new_x, new_y)])
                    
                if mode == 'radial':
                    collection.append([(0, 0), (cur_x, cur_y)])
                
                elif mode == 'triangles':
                    collection.append([(0, 0), (cur_x, cur_y), (new_x, new_y)])
            else:
                index = filtered[i]
                cur_pos = (cur_x, cur_y)
                arm_vertices[index].append(cur_pos)
                start = cur_arms[index]
                if not start:
                    cur_arms[index] = cur_pos
                else:
                    arms[index].append([start, cur_pos])
                    colors[index].append(color_values[cur_arm_indices[index] % num_colors])
                    cur_arm_indices[index] += 1
                    cur_arms[index] = cur_pos
        
        cur_x, cur_y = new_x, new_y
    
    result = {'colors': colors, 'vertices': vertices}
    if condition != triple_spiral:
        if mode  == 'rim':
            result['rim'] = collection
        
        if mode == 'radial':
            result['radial'] = collection
        
        elif mode == 'triangles':
            result['triangles'] = collection
    else:
        result['arms'] = arms
        result['arm_vertices'] = arm_vertices
    
    if condition:
        result['numbers'] = sorted(filtered)
    
    else:
        result['numbers'] = range(iterations)
    
    return result

def find_squares(number):
    square = sorted(squares(number))
    points = [b for a, b in pythogorean_spiral(number, condition=squares, mode='radial')['radial']]
    return dict(zip(square, points))

def plot_pythogorean_spiral(width=1920, height=1080, iterations=1024, mode='radial', lw=2, alpha=1, num_colors=12, show=True, condition=None, art=True, smooth=False):
    assert mode in ('rim', 'radial', 'triangles')
    if condition:
        assert condition in filters
    
    fig_back = 'white'
    if art: fig_back = 'black'
    fig = plt.figure(figsize=(width/100, height/100),
                     dpi=100, facecolor=fig_back)
    ax = fig.add_subplot(111)
    if art:
        ax.set_axis_off()
    data = pythogorean_spiral(iterations, mode=mode, num_colors=num_colors, condition=condition)
    if condition != triple_spiral:
        if mode  == 'rim':
            rim = LineCollection(data['rim'], colors=data['colors'], lw=lw, alpha=alpha)
            ax.add_collection(rim)
        
        elif mode == 'radial':
            radial = LineCollection(data['radial'], colors=data['colors'], lw=lw, alpha=alpha)
            ax.add_collection(radial)
        
        elif mode == 'triangles':
            triangles = PolyCollection(data['triangles'][::-1], facecolors=data['colors'][::-1], lw=lw, alpha=alpha, edgecolor='w')
            ax.add_collection(triangles)
    else:
        if not smooth:
            for i in range(3):
                ax.add_collection(LineCollection(data['arms'][i], colors=data['colors'][i], lw=lw, alpha=alpha))
        else:
            arm_0, arm_1, arm_2 = data['arm_vertices']
            x_arm_0, y_arm_0 = zip(*arm_0)
            x_arm_1, y_arm_1 = zip(*arm_1)
            x_arm_2, y_arm_2 = zip(*arm_2)
            tck, u = splprep([x_arm_0, y_arm_0], s=0)
            x0, y0 = splev(np.linspace(0, 1, 100), tck, der = 0)
            ax.plot(x0, y0, 'red')
            tck, u = splprep([x_arm_1, y_arm_1], s=0)
            x1, y1 = splev(np.linspace(0, 1, 100), tck, der = 0)
            ax.plot(x1, y1, 'green')
            tck, u = splprep([x_arm_2, y_arm_2], s=0)
            x2, y2 = splev(np.linspace(0, 1, 100), tck, der = 0)
            ax.plot(x2, y2, 'blue')
            
    if not art:
        plt.grid(True)
        for n, point in zip(data['numbers'], data['vertices']):
            x, y = zip(*data['vertices'])
            ax.scatter(x, y, marker='.')
            ax.annotate(str(n), point)
    
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
