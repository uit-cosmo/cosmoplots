"""Test the `concat` module."""

import pathlib
from sys import platform

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest

import cosmoplots

mpl.style.use("default")


def plot() -> None:
    """Create a simple plot."""
    a = np.exp(np.linspace(-3, 5, 100))
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.semilogy(a)


def test_help(capfd) -> None:
    """Test the `help` method."""
    cosmoplots.Combine().help()
    out, err = capfd.readouterr()
    help = (
        "To create images with labels:\n"
        "    convert in-a.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 10.0,10.0 '(a)'\" a.png\n"
        "    convert in-b.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 10.0,10.0 '(b)'\" b.png\n"
        "    convert in-c.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 10.0,10.0 '(c)'\" c.png\n"
        "    convert in-d.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 10.0,10.0 '(d)'\" d.png\n"
        "Then to combine them horizontally:\n"
        "    convert +append a.png b.png ab.png\n"
        "    convert +append c.png d.png cd.png\n"
        "And finally stack them vertically:\n"
        "    convert -append ab.png cd.png out.png\n"
        "Optionally delete all temporary files:\n"
        "    rm a.png b.png c.png d.png ab.png cd.png\n"
    )
    assert out == help


def test_combine(tmp_path: pathlib.Path) -> None:
    """Test that the `combine` function works."""

    def _combine() -> None:
        plot()
        plt.savefig(tmp_path / "test1.png")
        plot()
        plt.savefig(tmp_path / "test2.png")
        plot()
        plt.savefig(tmp_path / "test3.png")
        plot()
        plt.savefig(tmp_path / "test4.png")
        cosmoplots.combine(
            tmp_path / "test1.png",
            tmp_path / "test2.png",
            tmp_path / "test3.png",
            tmp_path / "test4.png",
        ).in_grid(w=2, h=2).save(tmp_path / "out.png")

    if platform == "win32":
        with pytest.raises(ChildProcessError):
            _combine()
    else:
        _combine()
        first_img = tmp_path / "out.png"
        assert first_img.exists()


def test_in_grid_not_specified(tmp_path: pathlib.Path) -> None:
    """Test error when `in_grid` has not been called."""

    def _grid() -> None:
        plot()
        plt.savefig(tmp_path / "test1.png")
        plot()
        plt.savefig(tmp_path / "test2.png")
        plot()
        plt.savefig(tmp_path / "test3.png")
        plot()
        plt.savefig(tmp_path / "test4.png")
        with pytest.raises(ValueError):
            cosmoplots.combine(
                tmp_path / "test1.png",
                tmp_path / "test2.png",
                tmp_path / "test3.png",
                tmp_path / "test4.png",
            ).save(tmp_path / "out.png")

    if platform == "win32":
        with pytest.raises(ChildProcessError):
            _grid()
    else:
        _grid()


def test_output_not_found(tmp_path: pathlib.Path) -> None:
    """Test the output file."""
    plot()
    plt.savefig(tmp_path / "test1.png")
    plot()
    plt.savefig(tmp_path / "test2.png")
    plot()
    plt.savefig(tmp_path / "test3.png")
    plot()
    plt.savefig(tmp_path / "test4.png")
    with pytest.raises(FileNotFoundError):
        cosmoplots.combine(
            tmp_path / "test1.png",
            tmp_path / "test2.png",
            tmp_path / "test3.png",
            tmp_path / "test4.png",
        ).in_grid(w=2, h=2).save(tmp_path / "second_level" / "out.png")


def test_input_not_found() -> None:
    """Test the input files."""
    with pytest.raises(FileNotFoundError):
        cosmoplots.combine("does_not_exist")


def test_wrong_number_of_labels(tmp_path: pathlib.Path) -> None:
    """Test that incorrect labelling errors out."""
    plot()
    plt.savefig(tmp_path / "test1.png")
    plot()
    plt.savefig(tmp_path / "test2.png")
    plot()
    plt.savefig(tmp_path / "test3.png")
    plot()
    plt.savefig(tmp_path / "test4.png")
    with pytest.raises(ValueError):
        cosmoplots.combine(
            tmp_path / "test1.png",
            tmp_path / "test2.png",
            tmp_path / "test3.png",
            tmp_path / "test4.png",
        ).in_grid(w=2, h=2).with_labels("only one").save(tmp_path / "out.png")


# fmt: off
_LABELS = {
    1: "(a)", 2: "(b)", 3: "(c)", 4: "(d)", 5: "(e)", 6: "(f)", 7: "(g)", 8: "(h)",
    9: "(i)", 10: "(j)", 11: "(k)", 12: "(l)", 13: "(m)", 14: "(n)", 15: "(o)",
    16: "(p)", 17: "(q)", 18: "(r)", 19: "(s)", 20: "(t)", 21: "(u)", 22: "(v)",
    23: "(w)", 24: "(x)", 25: "(y)", 26: "(z)", 27: "(aa)", 28: "(ab)", 29: "(ac)",
    30: "(ad)", 31: "(ae)", 32: "(af)", 33: "(ag)", 34: "(ah)", 35: "(ai)", 36: "(aj)",
    37: "(ak)", 38: "(al)", 39: "(am)", 40: "(an)", 41: "(ao)", 42: "(ap)", 43: "(aq)",
    44: "(ar)", 45: "(as)", 46: "(at)", 47: "(au)", 48: "(av)", 49: "(aw)", 50: "(ax)",
    51: "(ay)", 52: "(az)", 53: "(ba)", 54: "(bb)", 55: "(bc)", 56: "(bd)", 57: "(be)",
    58: "(bf)", 59: "(bg)", 60: "(bh)", 61: "(bi)", 62: "(bj)", 63: "(bk)", 64: "(bl)",
    65: "(bm)", 66: "(bn)", 67: "(bo)", 68: "(bp)", 69: "(bq)", 70: "(br)", 71: "(bs)",
    72: "(bt)", 73: "(bu)", 74: "(bv)", 75: "(bw)", 76: "(bx)", 77: "(by)", 78: "(bz)",
    79: "(ca)", 80: "(cb)", 81: "(cc)", 82: "(cd)", 83: "(ce)", 84: "(cf)", 85: "(cg)",
    86: "(ch)", 87: "(ci)", 88: "(cj)", 89: "(ck)", 90: "(cl)", 91: "(cm)", 92: "(cn)",
    93: "(co)", 94: "(cp)", 95: "(cq)", 96: "(cr)", 97: "(cs)", 98: "(ct)", 99: "(cu)",
    100: "(cv)",
}
# fmt: on


def test_generate_labels() -> None:
    """Test that the auto-generated labels are correct up the 100th label."""
    combiner = cosmoplots.Combine()
    combiner._files = [pathlib.Path(f"file-{i}.png") for i in range(100)]
    labels = combiner._create_labels()
    for i, label in enumerate(labels):
        assert label == _LABELS[i + 1]
