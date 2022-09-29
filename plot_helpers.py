import string
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.axes import Axes
from scipy.stats import pearsonr, normaltest


def index_subplots(
    axs: Axes,
    font_size: float = 20,
    font_weight: str = "bold",
    font_family: str = rcParams["font.family"],
    x: float = -0.1,
    y: float = 1.1,
    uppercase: bool = False,
    prefix: str = "",
    suffix: str = "",
    offset: int = 0,
):
    int_to_char_map = string.ascii_lowercase
    if uppercase:
        int_to_char_map = string.ascii_uppercase

    for i, ax in enumerate(axs):
        ax.text(
            x,
            y,
            prefix + int_to_char_map[i + offset] + suffix,
            transform=ax.transAxes,
            size=font_size,
            weight=font_weight,
            fontfamily=font_family,
        )


def plot_reg(x, y, ax):
    x = x.to_numpy()
    y = y.to_numpy()
    m, b = np.polyfit(x, y, 1)
    r, p = pearsonr(x, y)
    y_pred = m * x + b
    ax.plot(x, y_pred, linewidth=1.0, linestyle="dashed", color="gray")
    ax.annotate(
        f"r={round(r, 3)}, p={round(p, 3)}",
        xy=(x[-1], y_pred[-1]),
        fontsize=7,
        ha="left",
        va="top",
        xytext=(-50, 0),
        textcoords="offset points",
        bbox=dict(boxstyle="square", ec="white", fc="white"),
    )
