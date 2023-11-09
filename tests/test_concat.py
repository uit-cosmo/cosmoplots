"""Test the `concat` module."""

import pathlib

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
    first_img = tmp_path / "out.png"
    assert first_img.exists()


def test_in_grid_not_specified(tmp_path: pathlib.Path) -> None:
    """Test error when `in_grid` has not been called."""
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
