# cosmoplots
Routines to get a sane default configuration for production quality plots. Used by complex systems modelling group at UiT.

# Installation
```
pip install cosmoplots
```
# Use
Set your `rcparams` before plotting in your code, for example:
```Python
from cosmoplots import figure_defs

axes_size = figure_defs.set_rcparams_aip(plt.rcParams, num_cols=1, ls="thin")
```