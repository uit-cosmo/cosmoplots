# cosmoplots
Routines to get a sane default configuration for production quality plots. Used by complex systems modelling group at UiT.

# Installation
```
pip install cosmoplots
```
# Use
Set your `rcparams` before plotting in your code, for example:
```Python
import cosmoplots

axes_size = cosmoplots.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")
```

## `change_log_axis_base`

```python
import matplotlib.pyplot as plt
import numpy as np
import cosmoplots

axes_size = cosmoplots.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")
a = np.exp(np.linspace(-3, 5, 100))
# 1 --- Semilogx
fig = plt.figure()
ax = fig.add_axes(axes_size)
base = 2  # Default is 10, but 2 works equally well
cosmoplots.change_log_axis_base(ax, "x", base=base)
# Do plotting ...
# If you use "plot", the change_log_axis_base can be called at the top (along with add_axes
# etc.), but using loglog, semilogx, semilogy will re-set, and the change_log_axis_base
# function must be called again.
ax.plot(a)
plt.show()

# 2 --- Semilogy
fig = plt.figure()
ax = fig.add_axes(axes_size)
cosmoplots.change_log_axis_base(ax, "y")
# Do plotting ...
# If you use "plot", the change_log_axis_base can be called at the top (along with add_axes
# etc.), but using loglog, semilogx, semilogy will re-set, and the change_log_axis_base
# function must be called again.
ax.semilogy(a)
cosmoplots.change_log_axis_base(ax, "y")  # Commenting out this result in the default base10 ticks
plt.show()
```

