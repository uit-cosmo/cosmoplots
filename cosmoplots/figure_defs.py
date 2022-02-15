#!/usr/bin/python
# -*- Encoding: UTF-8 -*-

from typing import List
import numpy as np
import matplotlib as mpl

"""
Definitions for figures and plots.
Use the set_rcparams_.... routines to get a sane default configuration
for production quality plots.
Some guidelines when creating plots
As of matplotlib2.0, use the vega 3 color palette
https://github.com/vega/vega/wiki/Scales#scale-range-literals
For density scans, use the following plot styles
Density    Symbol    Color
High         ^         C0 #1f77b4
 ^           s         C1 #ff7f0e
 |           o         C2 #2ca02c
 v           d         C3 #d62728
Low          v         C4 #d9467bd
Color are robust on both, screen, print, projector.
"""

# For 5 symbols in a plot
symbol_list_5 = ["^", "s", "o", "d", "v"]

# For 4 symbols in a plot and below, avoid red and green (colorblindness) if possible
symbol_list_4 = ["^", "s", "d", "v"]

# 3 symbols in a plot
symbol_list_3 = ["^", "o", "v"]

# 2 symbols in a plot
symbol_list_2 = ["^", "v"]

# 1 symbol
symbol_list_1 = ["o"]


def set_rcparams_dynamo(
    myParams: mpl.RcParams, num_cols: int = 1, ls: str = "thin"
) -> List[float]:
    """Half column width figures for revtex.

    See http://publishing.aip.org/authors/preparing-graphics

    Parameters
    ----------
    myParams: matplotlib.RcParams
        The parameters from matplotlib
    num_cols: int
        Number of columns the figure spans.
        1 column  = 3.37" by 2.08"
        2 columns = 6.69" by 4.13"
    ls: str
        Either 'thick' or 'thin'. Defaults to 'thin'
    fonts: str
        Either 'small' or 'large'.

    Returns
    -------
    List[float]
        The size of the axes.

    Raises
    ------
    ValueError
        If the number of columns is not 1 or 2.
    """

    golden_ratio = 0.5 * (1.0 + np.sqrt(5.0))
    fig_dpi = 300.0
    fontsize = 8

    linewidth = 0.75
    if ls == "thick":
        linewidth *= 2

    # Define axis size to be used
    if num_cols == 1:
        ax_x0, ax_y0 = 0.2, 0.2
        axes_size = [ax_x0, ax_y0, 0.95 - ax_x0, 0.95 - ax_y0]
    elif num_cols == 2:
        ax_x0, ax_y0 = 0.1, 0.2
        axes_size = [ax_x0, ax_y0, 0.975 - ax_x0, 0.95 - ax_y0]
    else:
        raise ValueError("num_cols must be 1 or 2")

    # Figure size in inch
    fig_width_in = num_cols * 3.37
    fig_height_in = 3.37 / golden_ratio

    # Figure size and dpi
    myParams["figure.dpi"] = fig_dpi
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]
    myParams["savefig.dpi"] = fig_dpi

    # Figure legend
    myParams["legend.framealpha"] = 1.0
    myParams["legend.fancybox"] = False
    myParams["legend.edgecolor"] = "k"
    myParams["patch.linewidth"] = 0.5  # For legend box borders
    myParams["legend.handlelength"] = 1.45  # Show nice, even
    # numbers for different line styles

    # Font and text
    myParams["text.usetex"] = True
    myParams["pdf.fonttype"] = 42
    myParams["font.family"] = "Times"
    myParams["font.size"] = fontsize
    myParams["axes.labelsize"] = fontsize
    myParams["legend.fontsize"] = fontsize

    # Line size and marker size
    myParams["lines.markersize"] = 3.0 * linewidth
    myParams["lines.linewidth"] = linewidth

    # Axes thickness
    myParams["axes.linewidth"] = 0.5
    # Enable minor ticks
    myParams["ytick.minor.visible"] = True
    myParams["xtick.minor.visible"] = True
    # Default ticks on both sides of the axes
    myParams["xtick.top"] = True
    myParams["xtick.bottom"] = True
    myParams["ytick.left"] = True
    myParams["ytick.right"] = True
    # All ticks point inward
    myParams["xtick.direction"] = "in"
    myParams["ytick.direction"] = "in"

    return axes_size


def set_rcparams_article_thickline(myParams: mpl.RcParams) -> None:
    """
    One 8cm column for the TCV paper, thicker lines for visibility
    """
    set_rcparams_dynamo(myParams, ls="thick")

    # Re-sets:
    myParams["lines.markersize"] = 2


def set_rcparams_poster(myParams: mpl.RcParams) -> None:
    """
    Make 12.5cm wide figures used in posters
    """
    set_rcparams_dynamo(myParams, ls="thick")
    golden_ratio = 0.5 * (1.0 + np.sqrt(5.0))
    fontsize = 8

    # Re-sets: (in alphabetical order)
    fig_width_in = 4.92
    fig_height_in = fig_width_in / golden_ratio
    myParams["axes.labelsize"] = fontsize * 2
    myParams["axes.linewidth"] = 2
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]
    myParams["font.size"] = fontsize * 2
    myParams["legend.fontsize"] = 12
    myParams["lines.linewidth"] = 2
    myParams["patch.linewidth"] = 2  # For legend box borders

    # New settings:
    myParams["savefig.dpi"] = 300
    myParams["xtick.major.width"] = 2
    myParams["xtick.minor.width"] = 1
    myParams["ytick.major.width"] = 2
    myParams["ytick.minor.width"] = 1


def set_rcparams_talk(myParams: mpl.RcParams) -> mpl.RcParams:
    """
    Matplotlib configuration for talk graphics.
    Use for 16:9 aspect ratio in beamer slides
    Slides are 16cm * 9cm, figure is 7.5cm wide
    """
    set_rcparams_dynamo(myParams, ls="thick")
    golden_ratio = 0.5 * (1.0 + np.sqrt(5.0))

    # Re-sets: (in alphabetical order)
    fig_width_in = 6
    fig_height_in = fig_width_in / golden_ratio
    myParams["axes.linewidth"] = 1.0
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]
    myParams["font.size"] = 16
    myParams["legend.fontsize"] = 12

    # New settings:
    myParams["text.latex.unicode"] = True

    return myParams


# End of file figure_defs.py
