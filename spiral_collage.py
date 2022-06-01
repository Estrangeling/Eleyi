import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from pathlib import Path
from PIL import Image, ImageFilter
from random import random, randbytes

def sin(d): return np.sin(np.radians(d))
def cos(d): return np.cos(np.radians(d))
def tan(d): return np.tan(np.radians(d))

def create_spiral(init_length, rotate_angle, iterations, base):
    y = init_length/(2 * tan(rotate_angle/2))
    x = init_length/2
    segments = []
    segments.append([(-x, -y), (x, -y)])
    cur_x, cur_y = x, -y
    for i in range(1, iterations):
        length = init_length * base ** i
        new_x = cur_x + length * cos(i * rotate_angle)
        new_y = cur_y + length * sin(i * rotate_angle)
        segments.append([(cur_x, cur_y), (new_x, new_y)])
        cur_x, cur_y = new_x, new_y
    
    return segments

def plot_spiral(init_length, rotate_angle, iterations, base):
    segments = create_spiral(init_length, rotate_angle, iterations, base)
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    for segment in segments:
        x, y = zip(*segment)
        ax.plot(x, y)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.axis('scaled')
    plt.box(False)
    plt.show()

def rotate(pos, angle, center=(0, 0)):
    cx, cy = center
    px, py = pos
    diff_x, diff_y = (px - cx), (py - cy)
    cosa, sina = cos(angle), sin(angle)
    px1 = cosa * diff_x - sina * diff_y + cx
    py1 = sina * diff_x + cosa * diff_y + cy
    return (px1, py1)

def spiralify(images, unit_length=1024, rotation=25, base=0.97, allow_vertical=False):
    assert 0 < base < 1
    y = -unit_length/(2 * tan(rotation/2))
    x = unit_length/2
    rectangles = []
    first_image = images[0]
    rot90 = False
    width, height = first_image
    if not allow_vertical and height > width:
        width, height = height, width
        rot90 = True
    
    h = height * unit_length / width
    x1, x2 = -x, x
    y1, y2 = y, y-h
    g_min_x, g_max_x = x1, x2
    g_min_y, g_max_y = y2, y1
    vertices = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
    size = (round(unit_length), round(h))
    bounding = {'min_x': x1, 'max_x': x2, 'min_y': y2, 'max_y': y1}
    rectangles.append({
        'size': size,
        'angle': 0,
        'vertices': vertices,
        'bounding': bounding,
        'rot90': rot90
    })
    cur_x, cur_y = x2, y1
    for i, image in enumerate(images[1:]):
        rot90 = False
        width, height = image
        if not allow_vertical and height > width:
            width, height = height, width
            rot90 = True
        
        length = unit_length * base**(i+1)
        h = height * length / width
        size = (round(length), round(h))
        angle = ((i+1) * rotation) % 360
        x1, x2 = cur_x, cur_x + length
        y1, y2 = cur_y, cur_y - h
        vertices = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        vertices = [rotate(pos, angle, center=(x1, y1)) for pos in vertices]
        cur_x, cur_y = vertices[1]
        x_coord, y_coord = zip(*vertices)
        min_x = min(x_coord)
        max_x = max(x_coord)
        min_y = min(y_coord)
        max_y = max(y_coord)
        if min_x < g_min_x:
            g_min_x = min_x
        if max_x > g_max_x:
            g_max_x = max_x
        if min_y < g_min_y:
            g_min_y = min_y
        if max_y > g_max_y:
            g_max_y = max_y
        bounding = {'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y}
        rectangles.append({
            'size': size,
            'angle': angle,
            'vertices': vertices,
            'bounding': bounding,
            'rot90': rot90
        })
    
    x_axis = round(g_max_x - g_min_x + 1)
    y_axis = round(g_max_y - g_min_y + 1)
    
    for i, rectangle in enumerate(rectangles):
        min_x, max_x, min_y, max_y = rectangle['bounding'].values()
        min_x = min_x - g_min_x
        max_x = max_x - g_min_x
        min_y = g_max_y - min_y
        max_y = g_max_y - max_y
        if min_y > max_y:
            min_y, max_y = max_y, min_y
        rectangles[i]['numpy_bounding'] = {'min_x': round(min_x), 'max_x': round(max_x), 'min_y': round(min_y), 'max_y': round(max_y)}
    
    return {'rectangles': rectangles, 'size': (x_axis, y_axis), 'min_x': g_min_x, 'min_y': g_min_y, 'max_x': g_max_x, 'max_y': g_max_y}


def flatten(image, color=(255, 255, 255)):
    if image.mode != 'RGBA':
        return image
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.getchannel('A'))
    return background

def rotate_image(image, angle):
    cosa, sina = cos(angle), sin(angle)
    w, h = image.size
    coordinates = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
    coordinates = [rotate(pos, angle) for pos in coordinates]
    x, y = zip(*coordinates)
    min_x, min_y = min(x), min(y)
    matrix = np.array((
        # x col   y col  global col
        (cosa,   -sina,  -min_x),  # -> x' row
        (sina,   cosa,   -min_y),  # -> y' row
        (0,      0,           1),  # -> 1  row
    ))
    size_transform = np.abs(matrix[:2, :2])
    w1, h1 = (size_transform @ image.size).astype(int)
    matrix = np.linalg.inv(matrix)
    rotated = image.transform(
        size=(w1, h1),
        method=Image.AFFINE,
        data=matrix[:2, :].flatten(),
    )
    return rotated

def spiral_collage(images, unit_length=1024, rotation=25, base=0.97, allow_vertical=False):
    spiral_guide = spiralify([image.size for image in images], unit_length, rotation, base, allow_vertical)
    background = Image.new('RGB', spiral_guide['size'], (0, 0, 0))
    for guide, image in zip(spiral_guide['rectangles'][::-1], images[::-1]):
        if guide['rot90']:
            image = image.rotate(90, resample=Image.BILINEAR, expand=True)
        image = image.resize(guide['size'])
        mask = Image.new('L', guide['size'], 255)
        image = image.rotate(guide['angle'], expand=True)
        mask = mask.rotate(guide['angle'], expand=True)
        bounding = guide['numpy_bounding']
        min_x = bounding['min_x']
        min_y = bounding['min_y']
        background.paste(image, (min_x, min_y), mask)
    
    return background.filter(ImageFilter.GaussianBlur(radius=1))

def fade_color(color, strength):
    assert all(i in range(256) for i in color) and len(color) == 3
    assert 0 < strength <= 1
    return [round(i*strength) for i in color]

def spectrum_position(n):
    if not isinstance(n, int):
        raise TypeError('`n` should be an integer')
    if n < 0:
        raise ValueError('`n` must be non-negative')
    n %= 1530
    if 0 <= n < 255:
        return (255, n, 0)
    elif 255 <= n < 510:
        return (510-n, 255, 0)
    elif 510 <= n < 765:
        return (0, 255, n-510)
    elif 765 <= n < 1020:
        return (0, 1020-n, 255)
    elif 1020 <= n < 1275:
        return (n-1020, 0, 255)
    elif 1275 <= n < 1530:
        return (255, 0, 1530-n)

def spiral_image(unit_length, aspect_ratio, num_colors, num_rectangles, rotation=30, base=0.98, strength=0.96, allow_vertical=1, alpha=0.75):
    assert 0 < base < 1 and 0 < strength <= 1
    a, b = aspect_ratio
    unit_height = unit_length / a * b
    color_step = 1530 / num_colors
    colors = [spectrum_position(round(i*color_step)) for i in range(num_colors)]
    stub = [(unit_length, unit_height) for i in range(num_rectangles)]
    guides = spiralify(stub, unit_length=unit_length, rotation=rotation, base=base, allow_vertical=allow_vertical)
    width, height = guides['size']
    fig = plt.figure(frameon=False, figsize=(width/100, height/100), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    for i, guide in enumerate(guides['rectangles'][::-1]):
        I = num_rectangles - i - 1
        r, g, b = fade_color(colors[I % num_colors], strength**I)
        color = '#'+'{:06x}'.format((r<<16)+(g<<8)+b)
        c, d, e, f = guide['vertices']
        ax.add_patch(Polygon((c, d, f, e), facecolor=color, fill=True, antialiased=True, alpha=alpha))
    
    plt.xlim(guides['min_x'], guides['max_x'])
    plt.ylim(guides['min_y'], guides['max_y'])
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.axis('scaled')
    plt.box(False)
    fig.canvas.draw()
    img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())     
    plt.close(fig)
    img = np.array(img)
    mask = np.all(img == (255, 255, 255), axis=2)
    img[mask, :] = [0, 0, 0]
    return Image.fromarray(img).filter(ImageFilter.GaussianBlur(radius=2))
        

if __name__ == '__main__':
    files = list(Path('D:/Me').glob('*'))
    files = [str(i) for i in sorted(files, key=lambda x: -x.stat().st_mtime)]
    images = [flatten(Image.open(file)) for file in files]
    collage = spiral_collage(images, allow_vertical=1)
    collage.save('D:/images/collage_{}.png'.format(randbytes(6).hex()))
    img = spiral_image(450, (9, 16), 24, 120, base=0.97, strength=0.98, rotation=25)
    img.show()
    img.save('D:/test/{}.png'.format(randbytes(6).hex()))
