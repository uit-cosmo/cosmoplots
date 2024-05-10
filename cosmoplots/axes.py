"""Module for modifying the axis properties of plots."""

from typing import List, Tuple, Union
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def _convert_scale_name(scale: str, axis: str) -> str:
    """Convert the scale name to a more readable format."""
    # All possible scale names:
    # ['asinh', 'function', 'functionlog', 'linear', 'log', 'logit', 'mercator', 'symlog']
    return f"{axis}axis" if scale == "log" else "none"


def _check_axes_scales(axes: Axes) -> Tuple[List[str], str]:
    xscale, yscale = axes.get_xscale(), axes.get_yscale()
    xs, ys = _convert_scale_name(xscale, "x"), _convert_scale_name(yscale, "y")
    if xs == "xaxis" and ys == "yaxis":
        scales = [xs, ys]
        pltype = "loglog"
    elif xs == "xaxis":
        scales = [xs]
        pltype = "semilogx"
    elif ys == "yaxis":
        scales = [ys]
        pltype = "semilogy"
    else:
        scales = []
        pltype = "linear"
    return scales, pltype


def change_log_axis_base(
    axes: Axes, which: Union[str, None] = None, base: float = 10
) -> Axes:
    """Change the tick formatter to not use powers 0 and 1 in logarithmic plots.

    Change the logarithmic axis `10^0 -> 1` and `10^1 -> 10` (or the given base), i.e.
    without power, otherwise use the base to some power. For more robust and less error
    prone results, the plotting type is also re-set with the same base ('loglog',
    'semilogx' and 'semilogy').

    Modified from: https://tinyurl.com/log-tick-formatting

    Parameters
    ----------
    axes : plt.Axes
        An axes object
    which : str | None, optional
        Whether to update both x and y axis, or just one of them ("both", "x" or "y").
        If no value is given, it defaults to None and the function will try to infer the
        axis from the current plotting type. If the axis are already linear, the
        function will return the axes object without any changes. Defaults to None.
    base : float
        The base of the logarithm. Defaults to base 10 (same as loglog, etc.)

    Returns
    -------
    plt.Axes
        The updated axes object.
    """
    if which == "both":
        axs, pltype = ["xaxis", "yaxis"], "loglog"
    elif which == "x":
        axs, pltype = ["xaxis"], "semilogx"
    elif which == "y":
        axs, pltype = ["yaxis"], "semilogy"
    else:
        axs, pltype = _check_axes_scales(axes)
    if not axs and pltype == "linear":
        # If both the axes are already linear, just return the axes object silently
        return axes
    getattr(axes, pltype)(base=base)
    for ax in axs:
        f = getattr(axes, ax)
        f.set_major_formatter(
            ticker.FuncFormatter(
                lambda x, _: (
                    r"${:g}$".format(x)
                    if np.log(x) / np.log(base) in [0, 1]
                    else r"$"
                    + str(base)
                    + "^{"
                    + "{:g}".format(np.log(x) / np.log(base))
                    + r"}$"
                )
            )
        )
    return axes

def figure_multiple_rows_columns(rows: int, columns: int, labels: List[str] | None = None) -> Tuple[Figure, List[Axes]]:
    """Returns a figure with axes which is appropriate for (rows, columns) subfigures.

    Parameters
    ----------
    rows : int
        The number of rows in the figure
    columns : int
        The number of columns in the figure
    labels : List[str] | None
        The labels to be applied to each subfigure. Defaults to (a), (b), (c), ...

    Returns
    -------
    plt.Figure
        The figure object
    plt.Axes
        A list of all the axes objects owned by the figure
    """
    fig = plt.figure(figsize = (columns*3.37, rows*2.08277))
    axes = []
    labels = labels or gen_labels(rows*columns)
    for c in range(columns):
        for r in range(rows):
            left = (0.2)/columns + c/columns
            bottom = (0.2)/rows + (rows-1-r)/rows # Start at the top
            width = 0.75/columns
            height = 0.75/rows
            axes.append(fig.add_axes((left, bottom, width, height)))
            axes[-1].text(-0.15, 1, labels[columns*r+c], horizontalalignment='center', verticalalignment='center', transform=axes[-1].transAxes)

    return fig, axes

def gen_labels(len_labels):
    return [r"$\mathrm({})$".format(chr(97+l)) for l in range(len_labels)]
