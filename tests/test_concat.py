"""Test the `concat` module."""

import pathlib
import subprocess
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


def test_convert_help() -> None:
    """Test that ImageMagick's convert command is available."""
    result = subprocess.check_output(["convert", "--help"])
    out = "b'Version: ImageMagick'"
    assert str(result[:20]) == out


def test_help(capfd) -> None:
    """Test the `help` method."""
    # By default, the '.ttf' file is specified, but that's hard to test against.
    cosmoplots.Combine().using(font="Times-New-Roman").help()
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


def test_combine_ft(tmp_path: pathlib.Path) -> None:
    """Test the `combine` function with different file types."""

    def _combine() -> None:
        plot()
        plt.savefig(tmp_path / "test1.jpg")
        plot()
        plt.savefig(tmp_path / "test2.jpg")
        plot()
        plt.savefig(tmp_path / "test3.jpg")
        plot()
        plt.savefig(tmp_path / "test4.jpg")
        cosmoplots.combine(
            tmp_path / "test1.jpg",
            tmp_path / "test2.jpg",
            tmp_path / "test3.jpg",
            tmp_path / "test4.jpg",
        ).in_grid(w=2, h=2).save(tmp_path / "out.jpg")

    if platform == "win32":
        with pytest.raises(ChildProcessError):
            _combine()
    else:
        _combine()
        first_img = tmp_path / "out.jpg"
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


def test_using_update() -> None:
    """Test that the `using` method can be called multiple times."""
    c = cosmoplots.Combine().using(fontsize=12)
    c.using(gravity="southwest")
    assert c._fontsize == 12


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
    0: "(a)", 1: "(b)", 2: "(c)", 3: "(d)", 4: "(e)", 5: "(f)", 6: "(g)", 7: "(h)",
    8: "(i)", 9: "(j)", 10: "(k)", 11: "(l)", 12: "(m)", 13: "(n)", 14: "(o)",
    15: "(p)", 16: "(q)", 17: "(r)", 18: "(s)", 19: "(t)", 20: "(u)", 21: "(v)",
    22: "(w)", 23: "(x)", 24: "(y)", 25: "(z)", 26: "(aa)", 27: "(ab)", 28: "(ac)",
    29: "(ad)", 30: "(ae)", 31: "(af)", 32: "(ag)", 33: "(ah)", 34: "(ai)", 35: "(aj)",
    36: "(ak)", 37: "(al)", 38: "(am)", 39: "(an)", 40: "(ao)", 41: "(ap)", 42: "(aq)",
    43: "(ar)", 44: "(as)", 45: "(at)", 46: "(au)", 47: "(av)", 48: "(aw)", 49: "(ax)",
    50: "(ay)", 51: "(az)", 52: "(ba)", 53: "(bb)", 54: "(bc)", 55: "(bd)", 56: "(be)",
    57: "(bf)", 58: "(bg)", 59: "(bh)", 60: "(bi)", 61: "(bj)", 62: "(bk)", 63: "(bl)",
    64: "(bm)", 65: "(bn)", 66: "(bo)", 67: "(bp)", 68: "(bq)", 69: "(br)", 70: "(bs)",
    71: "(bt)", 72: "(bu)", 73: "(bv)", 74: "(bw)", 75: "(bx)", 76: "(by)", 77: "(bz)",
    78: "(ca)", 79: "(cb)", 80: "(cc)", 81: "(cd)", 82: "(ce)", 83: "(cf)", 84: "(cg)",
    85: "(ch)", 86: "(ci)", 87: "(cj)", 88: "(ck)", 89: "(cl)", 90: "(cm)", 91: "(cn)",
    92: "(co)", 93: "(cp)", 94: "(cq)", 95: "(cr)", 96: "(cs)", 97: "(ct)", 98: "(cu)",
    99: "(cv)",
}
# fmt: on


def test_generate_labels() -> None:
    """Test that the auto-generated labels are correct up the 100th label."""
    combiner = cosmoplots.Combine()
    combiner._files = [pathlib.Path(f"file-{i}.png") for i in range(100)]
    labels = combiner._create_labels()
    for i, label in enumerate(labels):
        assert label == _LABELS[i]
