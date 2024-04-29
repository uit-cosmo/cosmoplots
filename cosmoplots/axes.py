"""Module for modifying the axis properties of plots."""

from typing import List, Tuple, Union
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def _convert_scale_name(scale: str, axis: str) -> str:
    """Convert the scale name to a more readable format."""
    # All possible scale names:
    # ['asinh', 'function', 'functionlog', 'linear', 'log', 'logit', 'mercator', 'symlog']
    return f"{axis}axis" if scale == "log" else "none"


def _check_axes_scales(axes: plt.Axes) -> Tuple[List[str], str]:
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
    axes: plt.Axes, which: Union[str, None] = None, base: float = 10
) -> plt.Axes:
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

def multiple_rows_columns(rows, columns):
    # Changes the figsize so it is appropriate for 
    # (rows, columns) subfigures
    mpl.rcParams['figure.figsize'][0] = columns*3.37
    mpl.rcParams['figure.figsize'][1] = rows*2.08277
    mpl.rcParams['figure.subplot.left'] = 0.2 / columns
    mpl.rcParams['figure.subplot.right'] = 1 - 0.05 / columns
    mpl.rcParams['figure.subplot.bottom'] = 0.2 / rows
    mpl.rcParams['figure.subplot.top'] = 1 - 0.05 / rows
