import numpy as np
from colour import Color
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from typing import List


def make_color_swatch(color_list: list):
    """
    Generate plot of the desired color swatches. This is useful if you want to see what the swatches look like.
    This function is used in generate_hex_colors() where the plot of the swatches will show by default if used in Jupyter Notebook.

    Args:
        color_list: list
            List of colors from color map

    Return:
        color_swatch:
            A plot of the color swatches
    """

    color_swatch = LinearSegmentedColormap.from_list(
        "my_list", [Color(x).rgb for x in color_list]
    )

    plt.figure(figsize=(5, 3))
    plt.imshow(
        [list(np.arange(0, len(color_list), 1))],
        interpolation="nearest",
        origin="lower",
        cmap=color_swatch,
    )
    plt.xticks([])
    plt.yticks([])

    return color_swatch


def generate_hex_colors(
    number_data_points: int,
    color_map: str,
    show_swatch: bool = True,
    ascending: bool = True,
) -> List[str]:
    """
    Function to generate colors picked out of the matplolib color maps as hex numbers.
    If using this function in Jupyter Notebook, by default since show_swatch = True, a plot of the swatches will automatically appear.

    Args:
        number_data_points: int
            The number of data points
        color_map: str
            The name of the colour map from matplotlib. Grayscale friendly colors are:
            'viridis', 'plasma', 'inferno', 'magma', 'cubehelix', 'cividis'
            See more here: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        show_swatch: bool = True
            Show the color swatches based on the number of data points. 'True' means that a plot will show containing the swatches.
        ascending: bool = True
            Show the color swatches and list in ascending order, from light to dark. Set to True by default.

    Returns:
        color_list: List[str]
            List of hex numbers from the desired color map. Simply do print(color_list) to get this list.

    """

    cmap = cm.get_cmap(color_map, number_data_points)

    color_list = []

    for i in range(cmap.N):
        rgba = cmap(i)

        # rgb2hex accepts rgb or rgba
        color_list.append(colors.rgb2hex(rgba))

    # return light to darkest if ascending
    if ascending:
        if show_swatch:
            make_color_swatch(color_list[::-1])
        return color_list[::-1]
    else:
        if show_swatch:
            make_color_swatch(color_list)
        return color_list
