"""Module for modifying the axis properties of plots."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def change_log_axis_base(axes: plt.Axes, which: str, base: float = 10) -> plt.Axes:
    """Change the tick formatter to not use powers 0 and 1 in logarithmic plots.

    Change the logarithmic axes `10^0 -> 1` and `10^1 -> 10` (or the given base), i.e.
    without power, otherwise use the base to some power. For more robust and less error
    prone results, the plotting type is also re-set with the same base ('loglog',
    'semilogx' and 'semilogy').

    Modified from: https://tinyurl.com/log-tick-formatting

    Parameters
    ----------
    axes: plt.Axes
        An axes object
    which: str
        Whether to update both x and y axis, or just one of them.
    base: float
        The base of the logarithm. Defaults to base 10 (same as loglog, etc.)

    Returns
    -------
    plt.Axes
        The updated axes object.

    Raises
    ------
    ValueError
        If the axes given in `which` is not `x`, `y` or `both`.
    """
    if which == "both":
        axs, pltype = ["xaxis", "yaxis"], "loglog"
    elif which == "x":
        axs, pltype = ["xaxis"], "semilogx"
    elif which == "y":
        axs, pltype = ["yaxis"], "semilogy"
    else:
        raise ValueError(
            "No valid axis found. 'which' must be either of 'both', 'x' or 'y'."
        )
    getattr(axes, pltype)(base=base)
    for ax in axs:
        f = getattr(axes, ax)
        f.set_major_formatter(
            ticker.FuncFormatter(
                lambda x, _: r"${:g}$".format(x)
                if np.log(x) / np.log(base) in [0, 1]
                else r"$"
                + str(base)
                + "^{"
                + "{:g}".format(np.log(x) / np.log(base))
                + r"}$"
            )
        )
    return axes
