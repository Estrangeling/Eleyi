import matplotlib.pyplot as plt
import numba
import numpy as np
import typer
from itertools import cycle
from matplotlib.collections import PolyCollection
from PIL import Image
from scipy.spatial import Delaunay
from typing import Literal, Optional, Tuple
from typing_extensions import Annotated


def prime_wheel_sieve(n: int) -> np.ndarray:
    wheel = cycle([4, 2, 4, 2, 4, 6, 2, 6])
    primes = np.ones(n + 1, dtype=bool)
    primes[:2] = False
    for square, step in ((4, 2), (9, 6), (25, 10)):
        primes[square::step] = False

    k = 7
    while (square := k * k) <= n:
        if primes[k]:
            primes[square :: 2 * k] = False

        k += next(wheel)
    return np.where(primes)[0]


def double_primes(n: int, one_based: bool = False) -> np.ndarray:
    primes = prime_wheel_sieve(n)
    return primes[primes[primes < primes.size] - one_based]


def twin_primes(n: int) -> np.ndarray:
    primes = prime_wheel_sieve(n)
    mask = (primes - 2)[1:] == primes[:-1]
    mask[:-1] |= mask[1:]
    return primes[1:][mask]


@numba.vectorize(nopython=True, cache=True, fastmath=True, forceobj=False)
def reverse_digits(value: int | np.ndarray, base: int) -> np.ndarray:
    result = 0
    while value:
        value, remainder = divmod(value, base)
        result = result * base + remainder
    return result


def emirp(n: int, base: int = 10) -> np.ndarray:
    primes = prime_wheel_sieve(n)
    flipped = reverse_digits(primes, base)
    return primes[np.isin(flipped, primes)]


def squares(n: int) -> np.ndarray:
    numbers = np.arange(n)
    return numbers * numbers


def get_coordinates(r: np.ndarray, theta: np.ndarray) -> Tuple[np.ndarray]:
    y = r * np.sin(theta)
    x = r * np.cos(theta)
    return x, y


def get_figure(
    length: int, x: np.ndarray, y: np.ndarray
) -> Tuple[plt.Axes, plt.Figure]:
    length /= 100
    fig, ax = plt.subplots(figsize=(length, length), dpi=100, facecolor="black")
    ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1, 0, 0)
    plt.axis("scaled")
    ax.axis([min(x), max(x), min(y), max(y)])
    return ax, fig


def get_figure_polar(length: int, r: np.ndarray) -> Tuple[plt.Axes, plt.Figure]:
    length /= 100
    fig, ax = plt.subplots(
        figsize=(length, length),
        dpi=100,
        facecolor="black",
        subplot_kw={"projection": "polar"},
    )
    ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1, 0, 0)
    plt.axis("scaled")
    ax.set_rmax(max(r))
    return ax, fig


def triangulate(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    points = np.vstack((x, y)).T
    triangles = Delaunay(points)
    return triangles.points[triangles.simplices]


def scatter_plot(
    ax: plt.Axes, theta: np.ndarray, r: np.ndarray, colorize: bool
) -> None:
    colors = np.random.random((theta.size, 3)) if colorize else "white"
    ax.scatter(theta, r, marker=".", c=colors, s=1)


def triangle_plot(ax: plt.Axes, x: np.ndarray, y: np.ndarray, colorize: bool) -> None:
    if colorize:
        triangles = triangulate(x, y)
        count = triangles.shape[0]
        colors = np.random.random((count, 3))
        ax.add_collection(PolyCollection(triangles, fc=colors, lw=0))
    else:
        ax.triplot(x, y, lw=1, c="white")


def get_image(fig: plt.Figure) -> Image:
    fig.canvas.draw()
    image = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )
    plt.close(fig)
    return image


FUNCTION = {
    "primes": prime_wheel_sieve,
    "squares": squares,
    "twin_primes": twin_primes,
}
PLOT = Literal["scatter", "triangles"]
SERIES = Literal["primes", "squares", "double_primes", "emirps", "twin_primes"]


def polar_coordinates(
    n: int, domain: SERIES, one_based: bool, projection: str, base: int
) -> Tuple[np.ndarray]:
    if domain == "double_primes":
        numbers = double_primes(n, one_based)
    elif domain == "emirps":
        numbers = emirp(n, base)
    else:
        numbers = FUNCTION[domain](n)
    if projection == "polar":
        r, theta = numbers, numbers
    elif projection == "Sacks":
        r = np.sqrt(numbers)
        theta = 2 * np.pi * r
    return r, theta


def polar_plot(
    n: int,
    length: int = 1080,
    colorize: bool = False,
    mode: PLOT = "scatter",
    domain: SERIES = "prime",
    one_based: bool = False,
    projection: Literal["polar", "Sacks"] = "polar",
    base: int = 10,
) -> Image:
    r, theta = polar_coordinates(n, domain, one_based, projection, base)
    if mode == "scatter":
        ax, fig = get_figure_polar(length, r)
        scatter_plot(ax, theta, r, colorize)
    elif mode == "triangles":
        x, y = get_coordinates(r, theta)
        ax, fig = get_figure(length, x, y)
        triangle_plot(ax, x, y, colorize)

    return get_image(fig)


def annotate(arg_type: type, optional: bool, help_msg: str) -> Annotated:
    if not optional:
        return Annotated[arg_type, typer.Argument(help=help_msg)]

    return Annotated[Optional[arg_type], typer.Option(help=help_msg)]


HELP = (
    "specifies the limit of prime numbers (and subsets) or the count of square numbers",
    "specifies the path where the output image should be saved",
    "specifies the side length of the output square image, in pixels, default 1080",
    "specifies whether the image should be colorized or not, default False",
    """specifies the mode of the visualization, must be either 'scatter' or 'triangles',
    if set to 'scatter', the resultant image will be a black background with some with points,
    in which each point is a prime or its subset or square number, with coordinate determined by the parameter specified.
    If colorize is True, the points will be randomly colorized, else they will be white.
    If the mode is 'triangles', the program will take the coordinates and perform Delaunay triangulation on them,
    and then output the result. If colorize is False, the resultant image will be the white edges of many triangles on a black background,
    else the triangles will be filled with random colors.""",
    "specifies the domain of numbers, must be in {'squares', 'primes', 'emirps', 'double_primes', 'twin_primes'}",
    "specifies the projection of the numbers, coordinates will be (r, θ) = (p, p) if polar, else (r, θ) = (sqrt(p), τ sqrt(p)) if Sacks",
    "specifies whether the indexing of primes is to be one-based or not, only has effect if domain is 'double_primes'",
    "specifies the base of emirp filter, default 10",
)
N = annotate(int, False, HELP[0])
PATH = annotate(str, False, HELP[1])
LENGTH = annotate(int, True, HELP[2])
COLORIZE = annotate(bool, True, HELP[3])
MODE = annotate(str, True, HELP[4])
DOMAIN = annotate(str, True, HELP[5])
PROJECTION = annotate(str, True, HELP[6])
ONE_BASED = annotate(bool, True, HELP[7])
BASE = annotate(int, True, HELP[8])


def main(
    n: N,
    path: PATH,
    length: LENGTH = 1080,
    colorize: COLORIZE = False,
    mode: MODE = "scatter",
    domain: DOMAIN = "primes",
    projection: PROJECTION = "polar",
    one_based: ONE_BASED = False,
    base: BASE = 10,
) -> None:
    """This program generates all prime or square numbers up to a given number,
    then converts the numbers to coordinates in the polar coordinate system,
    so that the resultant point when rotated around the origin certain radians clockwise,
    will coincide the point (x, 0), where x is a prime or square number and the number that corresponds to the point.
    The program will then convert the data to an image visualization base on the paramters specified
    """
    polar_plot(n, length, colorize, mode, domain, one_based, projection, base).save(
        path
    )


if __name__ == "__main__":
    typer.run(main)
