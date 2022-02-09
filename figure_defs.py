#!/usr/bin/python
# -*- Encoding: UTF-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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


golden_ratio = 0.5 * (1.0 + np.sqrt(5.0))
fig_dpi = 300.0


def set_rcparams_aip(myParams, num_cols=1, ls="thin"):
    """
    Half column width figures for revtex, see
    http://publishing.aip.org/authors/preparing-graphics
    Input:
    =======
    myParams...: matplotlib.rcParams, the parameters from matplotlib
    num_cols...: int, number of columnes the figure spans.
                      1 column  = 3.37" by 2.08"
                      2 columns = 6.69" by 4.13"
    ls.........: string, either "thick" or "thin". Defaults to "thin"
    Output:
    =======
    None
    """

    assert ls in ["thick", "thin"]
    ls_dict = {"thick": 1.5, "thin": 0.5}

    assert num_cols in [1, 2]

    # Define axis size to be used
    if num_cols == 1:
        ax_x0, ax_y0 = 0.2, 0.2
        axes_size = [ax_x0, ax_y0, 0.95 - ax_x0, 0.95 - ax_y0]
    elif num_cols == 2:
        ax_x0, ax_y0 = 0.1, 0.2
        axes_size = [ax_x0, ax_y0, 0.95 - ax_x0, 0.95 - ax_y0]

    # Figure size in inch
    fig_width_in = num_cols * 3.37
    fig_height_in = 3.37 / golden_ratio
    # figure size in pts
    fig_width_pt = fig_width_in * fig_dpi
    fig_height_pt = fig_height_in * fig_dpi
    # print 'Figure size: %4.2f"" x %4.2f""' % (fig_width_in, fig_height_in)
    # print 'Figure resolution: %d dpi' % fig_dpi

    # myParams['font.family'] = 'Times'
    myParams["font.size"] = 8
    myParams["axes.linewidth"] = 0.5
    myParams["patch.linewidth"] = 0.5  # For legend box borders
    myParams["axes.labelsize"] = 8
    myParams["legend.fontsize"] = 8
    myParams["lines.markersize"] = 2.0 * ls_dict[ls]
    myParams["lines.linewidth"] = ls_dict[ls]
    myParams["figure.dpi"] = 300
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]
    myParams["text.usetex"] = True
    myParams["savefig.dpi"] = 300
    myParams["pdf.fonttype"] = 42

    # Enable minor ticks
    # myParams['ytick.minor.visible'] = True
    # myParams['xtick.minor.visible'] = True
    # Default ticks on both sides of the axes
    # myParams["xtick.top"] = True
    # myParams["xtick.bottom"] = True
    # myParams["ytick.left"] = True
    # myParams["ytick.right"] = True
    # All ticks point inward
    myParams["xtick.direction"] = "in"
    myParams["ytick.direction"] = "in"

    return axes_size


def set_rcparams_article_thickline(myParams):
    """
    One 8cm column for the TCV paper, thicker lines for visibility
    """
    # Figure size in inch
    fig_width_in = 3.37
    fig_height_in = fig_width_in / golden_ratio
    # figure size in pts
    fig_width_pt = fig_width_in * fig_dpi
    fig_height_pt = fig_height_in * fig_dpi
    # print 'Figure size: %4.2f"" x %4.2f""' % (fig_width_in, fig_height_in)
    # print 'Figure resolution: %d dpi' % fig_dpi

    # myParams['font.family'] = 'Time'
    myParams["font.size"] = 8
    myParams["axes.linewidth"] = 0.5
    myParams["axes.labelsize"] = 8
    myParams["legend.fontsize"] = 8
    # myParams['legend.handlelength'] = 3
    myParams["lines.markersize"] = 2
    myParams["lines.linewidth"] = 1.5
    myParams["figure.dpi"] = 300
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]
    myParams["text.usetex"] = True
    myParams["savefig.dpi"] = 300
    myParams["pdf.fonttype"] = 42
    myParams["patch.linewidth"] = 0.5  # For legend box borders

    # Enable minor ticks
    myParams["ytick.minor.visible"] = True
    myParams["xtick.minor.visible"] = True
    # All ticks point inward
    myParams["xtick.direction"] = "in"
    myParams["ytick.direction"] = "in"
    # Default ticks on both sides of the axes
    myParams["xtick.top"] = True
    myParams["xtick.bottom"] = True
    myParams["ytick.left"] = True
    myParams["ytick.right"] = True


def set_rcparams_poster(myParams):
    """
    Make 12.5cm wide figures used in posters
    """

    # Figure dimensions in inch
    fig_width_in = 4.92
    fig_height_in = fig_width_in / golden_ratio
    # Figure dimension in pts
    figure_width_pt = fig_width_in * fig_dpi
    figure_height_pt = fig_height_in * fig_dpi

    # print "Figure size: %4.2fx%4.2f, %3d dpi" % (fig_width_in,
    # fig_height_in, fig_dpi)

    myParams["figure.figsize"] = [fig_width_in, fig_height_in]

    # Set text parameters etc.
    myParams["font.size"] = 16
    myParams["axes.labelsize"] = 16
    myParams["legend.fontsize"] = 12

    myParams["axes.linewidth"] = 2
    myParams["patch.linewidth"] = 2  # For legend box borders
    myParams["lines.linewidth"] = 2
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]

    myParams["xtick.major.width"] = 2
    myParams["xtick.minor.width"] = 1
    myParams["ytick.major.width"] = 2
    myParams["ytick.minor.width"] = 1

    myParams["savefig.dpi"] = 300
    myParams["pdf.fonttype"] = 42
    myParams["text.usetex"] = True

    # Enable minor ticks
    myParams["ytick.minor.visible"] = True
    myParams["xtick.minor.visible"] = True
    # Default ticks on both sides of the axes
    myParams["xtick.top"] = True
    myParams["xtick.bottom"] = True
    myParams["ytick.left"] = True
    myParams["ytick.right"] = True


def set_rcparams_talk(myParams):
    """
    Matplotlib configuration for talk graphics.
    Use for 16:9 aspect ratio in beamer slides
    Slides are 16cm * 9cm, figure is 7.5cm wide
    """

    golden_ratio = 0.5 * (1.0 + np.sqrt(5.0))
    fig_width_in = 6
    fig_height_in = fig_width_in / golden_ratio

    myParams["font.size"] = 16
    myParams["axes.linewidth"] = 1.0
    myParams["legend.fontsize"] = 12
    myParams["text.usetex"] = True
    myParams["text.latex.unicode"] = True
    myParams["figure.figsize"] = [fig_width_in, fig_height_in]

    # Enable minor ticks
    myParams["ytick.minor.visible"] = True
    myParams["xtick.minor.visible"] = True
    # Default ticks on both sides of the axes
    myParams["xtick.top"] = True
    myParams["xtick.bottom"] = True
    myParams["ytick.left"] = True
    myParams["ytick.right"] = True

    return myParams


# End of file figure_defs.py
