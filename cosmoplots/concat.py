"""Combine cosmoplots images in a subfigure layout."""

# `Self` was introduced in 3.11, but returning the class type works from 3.7 onwards.
from __future__ import annotations

import pathlib
import random
import subprocess
import tempfile


class Combine:
    """Combine images made with the cosmoplots mplstyle into a subfigure layout."""

    def __init__(self) -> None:
        self._gravity = "northwest"
        self._fontsize = 100
        self._pos = (10.0, 10.0)
        self._font = "Times-New-Roman"
        self._color = "black"
        self._output = pathlib.Path("output.png")
        self._files: list[pathlib.Path] = []
        self._labels: list[str] = []
        self._w: int | None = None
        self._h: int | None = None

    def combine(self, *files: str | pathlib.Path) -> Combine:
        """Give all files that should be combined.

        Parameters
        ----------
        files : str | pathlib.Path
            A file path that can be read by pathlib.Path.
        """
        for f in files:
            current_file = pathlib.Path(f)
            if current_file.exists():
                self._files.append(current_file)
            else:
                raise FileNotFoundError(f"The input file {current_file} was not found.")
        return self

    def using(
        self,
        gravity: str = "northwest",
        pos: tuple[float, float] = (10.0, 10.0),
        font: str = "Times-New-Roman",
        fontsize: int = 100,
        color: str = "black",
    ) -> Combine:
        """Set text properties.

        Parameters
        ----------
        gravity : str
            Where the position of the text is relative to in the subfigure. Default is
            `northwest`. Possible values are `north`, `northeast`, `northwest`, `south`,
            `southeast`, `southwest`, `west`, `east` and `center`.
        pos : tuple[float, float]
            The position in the subfigure relative to `gravity`. Default is `(10.0,
            10.0)`.
        font : str
            The type of font to use, default is Times New Roman. See `convert -list
            font` for a list of available fonts.
        fontsize : int
            The size of the font in pointsize. Default is `100`.
        color : str
            The color of the text. Default is `black`.
        """
        self._gravity = gravity
        self._fontsize = fontsize
        self._pos = pos
        self._font = font
        self._color = color
        return self

    def in_grid(self, w: int, h: int) -> Combine:
        """Specify the grid layout.

        Parameters
        ----------
        w : int
            The number of subfigures in the horizontal direction (width).
        h : int
            The number of subfigures in the vertical direction (height).
        """
        if not self._files:
            raise ValueError("You need to provide the files first.")
        if int(w * h) < len(self._files):
            raise ValueError("The grid is too small.")
        self._w = w
        self._h = h
        return self

    def with_labels(self, *labels: str) -> Combine:
        """Give the labels that should be printed on the subfigures.

        Providing labels is optional, and if not given, the labels will be generated
        alphabetically as (a), (b), (c), ..., (aa), (ab), (ac), ...
        """
        if not labels:
            self._labels = self._create_labels()
        elif len(labels) != len(self._files):
            raise ValueError("You need to provide the same amount of labels.")
        else:
            self._labels = list(labels)

        return self

    def _create_labels(self) -> list[str]:
        characters: list[str] = []
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        count = 0
        # If labels have not been provided, create labels that follow an alphabetical
        # order.
        while len(characters) < len(self._files):
            # Calculate the current character based on the count
            current_char = ""
            quotient, remainder = divmod(count, 26)
            current_char += alphabet[remainder]

            if quotient > 0:
                current_char = alphabet[quotient - 1] + current_char

            characters.append(f"({current_char})")
            count += 1
        return characters

    def save(self, output: pathlib.Path | str | None = None) -> None:
        """Save the combined images as a png file.

        Parameters
        ----------
        output : pathlib.Path | str, optional
            Give the name of the output file, default is `output.png`.
        """
        self._check_params_before_save(output)
        self._check_cli_available()
        self._run_subprocess()

    def _check_params_before_save(
        self, output: pathlib.Path | str | None = None
    ) -> None:
        # Check if there are files
        if output is not None:
            output = pathlib.Path(output)
            self._output = (
                output if output.name.endswith("png") else output.with_suffix(".png")
            )
        if not self._output.parents[0].exists():
            raise FileNotFoundError(
                f"The file path {self._output.parents[0]} does not exist."
            )
        if not self._labels:
            self._labels = self._create_labels()

    @staticmethod
    def _check_cli_available() -> None:
        try:
            subprocess.check_output("convert --help", shell=True)
        except subprocess.CalledProcessError as e:
            raise ChildProcessError(
                "Calling `convert --help` did not work. Are you sure you have imagemagick installed?"
            ) from e

    def _run_subprocess(self) -> None:
        # In case several python runtimes use this class, we prepend a random string so
        # that we do not experience conflicts when creating the temporary files.
        tmp_dir = tempfile.TemporaryDirectory()
        rnd_str = str(random.random())[2:]
        if self._w is None or self._h is None:
            raise ValueError("You need to specify the files and grid first.")
        idx = list(range(len(self._files)))
        for i, file, label in zip(idx, self._files, self._labels):
            # Add label to images
            subprocess.call(
                [
                    "convert",
                    file,
                    "-font",
                    self._font,
                    "-pointsize",
                    str(self._fontsize),
                    "-draw",
                    (
                        f"gravity {self._gravity} fill {self._color} text"
                        f" {self._pos[0]},{self._pos[1]} '{label}'"
                    ),
                    pathlib.Path(tmp_dir.name) / f"{rnd_str}_{str(i)}.png",
                ]
            )
        # Create horizontal subfigures
        for j in range(self._h):
            # Choose first n items in the list
            idx_sub = idx[j * self._w : (j + 1) * self._w]
            subprocess.call(
                ["convert", "+append"]
                + [
                    pathlib.Path(tmp_dir.name) / f"{rnd_str}_{str(i)}.png"
                    for i in idx_sub
                ]
                + [pathlib.Path(tmp_dir.name) / f"{rnd_str}_subfigure_{j}.png"]
            )

        # Create vertical subfigures from horizontal subfigures
        subprocess.call(
            ["convert", "-append"]
            + [
                pathlib.Path(tmp_dir.name) / f"{rnd_str}_subfigure_{j}.png"
                for j in range(self._h)
            ]
            + [self._output.resolve()]
        )

        # Delete temporary files
        tmp_dir.cleanup()

    def help(self) -> None:
        """Print commands that are used."""

        def _conv_cmd(lab) -> str:
            return (
                f"    convert in-{lab}.png -font {self._font} -pointsize"
                f' {self._fontsize} -draw "gravity {self._gravity} fill {self._color}'
                f" text {self._pos[0]},{self._pos[1]} '({lab})'\" {lab}.png\n"
            )

        print(
            "To create images with labels:\n"
            f"{_conv_cmd('a')}"
            f"{_conv_cmd('b')}"
            f"{_conv_cmd('c')}"
            f"{_conv_cmd('d')}"
            "Then to combine them horizontally:\n"
            "    convert +append a.png b.png ab.png\n"
            "    convert +append c.png d.png cd.png\n"
            "And finally stack them vertically:\n"
            "    convert -append ab.png cd.png out.png\n"
            "Optionally delete all temporary files:\n"
            "    rm a.png b.png c.png d.png ab.png cd.png"
        )


def combine(*files: str | pathlib.Path) -> Combine:
    """Give all files that should be combined.

    Parameters
    ----------
    files : str | pathlib.Path
        A file path that can be read by pathlib.Path.

    Returns
    -------
    Combine
        An instance of the Combine class.

    Examples
    --------
    Load the files and subsequently call the methods that updates the properties.

    >>> combine(
    ...     "file1.png", "file2.png", "file3.png", "file4.png", "file5.png", "file6.png"
    ... ).using(fontsize=120).in_grid(w=2, h=3).with_labels(
    ...     "(a)", "(b)", "(c)", "(d)", "(e)", "(f)"
    ... ).save()

    All (global) methods except from `save` and `help` return the object itself, and can
    be chained together.
    """
    return Combine().combine(*files)
