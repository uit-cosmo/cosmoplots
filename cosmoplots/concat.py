"""Combine images in a subfigure layout."""

# `Self` was introduced in 3.11, but returning the class type works from 3.7 onwards.
from __future__ import annotations
import warnings

import logging
import pathlib
import subprocess
import tempfile
from contextlib import contextmanager

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont


@contextmanager
def _ignore_logging_context():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    # turn loggers off
    for logger in loggers:
        logger.disabled = True
    logging.root.disabled = True
    yield
    # turn loggers back on
    for logger in loggers:
        logger.disabled = False
    logging.root.disabled = False


class Combine:
    """Combine images into a subfigure layout."""

    def __init__(self) -> None:
        self._gravity = "northwest"
        self._pos = (10.0, 10.0)
        with _ignore_logging_context():
            font = findfont(FontProperties(family=plt.rcParams["font.serif"]))
        self._font = font
        self._fontsize = int(plt.rcParams["font.size"])
        self._color = "black"
        self._ft: str = ".png"
        self._output = pathlib.Path(f"output{self._ft}")
        self._dpi = (
            plt.rcParams["savefig.dpi"]
            if isinstance(plt.rcParams["savefig.dpi"], float)
            else plt.rcParams["figure.dpi"]
        )
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
        *,
        gravity: str | None = None,
        pos: tuple[float, float] | None = None,
        font: str | None = None,
        fontsize: int | None = None,
        color: str | None = None,
    ) -> Combine:
        """Set text properties.

        The properties must be given as keyword arguments to take effect.

        Parameters
        ----------
        gravity : str, optional
            Where the position of the text is relative to in the subfigure. Default is
            `northwest`. Possible values are `north`, `northeast`, `northwest`, `south`,
            `southeast`, `southwest`, `west`, `east` and `center`.
        pos : tuple[float, float], optional
            The position in the subfigure relative to `gravity`. Default is `(10.0,
            10.0)`.
        font : str, optional
            The type of font to use, default is Times New Roman. See `magick -list
            font` for a list of available fonts.
        fontsize : int, optional
            The size of the font in pointsize. Default is to use the "font.size" field
            in the matplotlib rcParams.
        color : str, optional
            The color of the text. Default is `black`.
        """
        self._gravity = gravity or self._gravity
        self._fontsize = fontsize or self._fontsize
        self._pos = pos or self._pos
        self._font = font or self._font
        self._color = color or self._color
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
        elif int(w * (h - 1)) > len(self._files) or int(h * (w - 1)) > len(self._files):
            raise ValueError("The grid is too big.")
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

    def save(
        self, output: pathlib.Path | str | None = None, dpi: float | int | None = None
    ) -> None:
        """Save the combined images as a png file.

        Parameters
        ----------
        output : pathlib.Path | str, optional
            Give the name of the output file, default is `output.png`.
        dpi : float | int, optional
            The resolution that the input files were saved with. Default is the same as
            the matplotlib savefig dpi.
        """
        self._dpi = dpi or self._dpi
        self._check_params_before_save(output)
        self._check_cli_available()
        self._run_subprocess()

    def _check_params_before_save(
        self, output: pathlib.Path | str | None = None, ft: str | None = None
    ) -> None:
        # Check if there are files
        if output is not None:
            output = pathlib.Path(output)
            if ft is None:
                self._ft = output.suffix or ".png"
            else:
                self._ft = ft if ft.startswith(".") else f".{ft}"
            self._output = (
                output
                if output.name.endswith(self._ft)
                else output.with_suffix(self._ft)
            )
        if self._ft in [".eps", ".pdf"]:
            warnings.warn(
                "The ImageMagick `magick` command does not work well with vector"
                " formats. Consider combining the plots directly using matplotlib,"
                " or change to a different format, such as 'png' or 'jpg'. See also"
                " https://www.imagemagick.org/Usage/formats/#vector",
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
            subprocess.check_output("magick --help", shell=True)
        except subprocess.CalledProcessError as e:
            raise ChildProcessError(
                "Calling `magick --help` did not work. Are you sure you have "
                "imagemagick installed? If not, resort to the ImageMagick website: "
                "https://imagemagick.org/script/download.php"
            ) from e
        result = subprocess.check_output(["magick", "--version"])
        out = "b'Version: ImageMagick 7'"
        v = str(result).split(" ")[2]
        if str(result[:22]) != out:
            warnings.warn(
                f"WARNING: It looks like your version of ImageMagick is {v}. This class"
                " assumes you are using version 7.",
                stacklevel=2,
            )

    def _run_subprocess(self) -> None:
        # In case several python runtimes use this class, we use a temporary directory
        # to which we save the files generated from the intermediate subprocess calls.
        # This way we will not experience conflicts when calling the combine class from
        # two or more parallel python runtimes.
        tmp_dir = tempfile.TemporaryDirectory()
        if self._w is None or self._h is None:
            raise ValueError("You need to specify the files and grid first.")
        idx = list(range(len(self._files)))
        tmp_path = pathlib.Path(tmp_dir.name)
        for i, file, label in zip(idx, self._files, self._labels):
            # Add label to images
            subprocess.call(
                [
                    "magick",
                    file,
                    "-units",
                    "PixelsPerInch",
                    "-density",
                    str(self._dpi),
                    "-font",
                    self._font,
                    "-pointsize",
                    str(self._fontsize),
                    "-draw",
                    (
                        f"gravity {self._gravity} fill {self._color} text"
                        f" {self._pos[0]},{self._pos[1]} '{label}'"
                    ),
                    tmp_path / f"{str(i)}{self._ft}",
                ]
            )
        # Create horizontal subfigures
        for j in range(self._h):
            # Choose first n items in the list
            idx_sub = idx[j * self._w : (j + 1) * self._w]
            subprocess.call(
                ["magick"]
                + [tmp_path / f"{str(i)}{self._ft}" for i in idx_sub]
                + ["+append"]
                + [tmp_path / f"subfigure_{j}{self._ft}"],
            )

        # Create vertical subfigures from horizontal subfigures
        subprocess.call(
            ["magick"]
            + [tmp_path / f"subfigure_{j}{self._ft}" for j in range(self._h)]
            + ["-append"]
            + [self._output.resolve()]
        )

        # Delete temporary files
        tmp_dir.cleanup()

    def help(self) -> None:
        """Print commands that are used."""

        def _conv_cmd(lab) -> str:
            return (
                f"    magick in-{lab}{self._ft} -font {self._font} -pointsize"
                f' {self._fontsize} -draw "gravity {self._gravity} fill {self._color}'
                f" text {self._pos[0]},{self._pos[1]} '({lab})'\" {lab}{self._ft}\n"
            )

        print(
            "To create images with labels:\n"
            f"{_conv_cmd('a')}"
            f"{_conv_cmd('b')}"
            f"{_conv_cmd('c')}"
            f"{_conv_cmd('d')}"
            "Then to combine them horizontally:\n"
            f"    magick a{self._ft} b{self._ft} +append ab{self._ft}\n"
            f"    magick c{self._ft} d{self._ft} +append cd{self._ft}\n"
            "And finally stack them vertically:\n"
            f"    magick ab{self._ft} cd{self._ft} -append out{self._ft}\n"
            "Optionally delete all temporary files:\n"
            f"    rm a{self._ft} b{self._ft} c{self._ft} d{self._ft} ab{self._ft} cd{self._ft}"
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
