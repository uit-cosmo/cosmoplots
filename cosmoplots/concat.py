"""Combine cosmoplots images in a subfigure layout."""

from typing import Self
import subprocess
import pathlib


class Combine:
    def __init__(
        self,
        gravity: str = "northwest",
        pos: tuple[float, float] = (0.0, 0.0),
        font: str = "Times-New-Roman",
        fontsize: int = 100,
        color: str = "black",
        output: str = "output",
    ) -> None:
        self._gravity = gravity
        self._fontsize = fontsize
        self._pos = pos
        self._font = font
        self._color = color
        self._output = output if output.endswith("png") else f"{output}.png"
        self._files: list[pathlib.Path] = []
        self._labels: list[str] = []
        self._w: int | None = None
        self._h: int | None = None

    def combine(self, *files: str) -> Self:
        """Give all files that should be combined.

        Parameters
        ----------
        files : str
            A file path that can be read by pathlib.Path.
        """
        for f in files:
            current_file = pathlib.Path(f)
            if current_file.exists():
                self._files.append(current_file)
            else:
                raise ValueError("File not found.")
        return self

    def using(
        self,
        gravity: str = "northwest",
        pos: tuple[float, float] = (0.0, 0.0),
        font: str = "Times-New-Roman",
        fontsize: int = 100,
        color: str = "black",
    ) -> Self:
        """Set text properties.

        Parameters
        ----------
        pos : tuple[float, float]
            The position relative to the top-left corner of the subfigure.
        font : str
            The type of font to use, default is Times New Roman. See `convert -list
            font` for a list of available fonts.
        fontsize : int
            The size of the font in pointsize.
        color : str
            The color of the text.
        """
        self._gravity = gravity
        self._fontsize = fontsize
        self._pos = pos
        self._font = font
        self._color = color
        return self

    def in_grid(self, w: int, h: int) -> Self:
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

    def with_labels(self, *labels: str) -> Self:
        """Give the labels that should be printed on the subfigures."""
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
        while len(characters) < len(self._files):
            # Calculate the current character based on the count
            current_char = ""
            quotient, remainder = divmod(count, 26)
            current_char += alphabet[remainder]

            if quotient > 0:
                current_char = alphabet[quotient - 1] + current_char

            characters.append(current_char)
            count += 1
        return characters

    def save(self, output: str | None = None) -> None:
        """Save the combined images as a png file.

        Parameters
        ----------
        output : str, optional
            Give the name of the output file, default is `output.png`.
        """
        # Check if there are files
        if output is not None:
            self._output = output if output.endswith("png") else f"{output}.png"
        if self._w is None or self._h is None:
            raise ValueError("You need to specify the files and grid first.")
        if not self._labels:
            self._labels = self._create_labels()
        idx = list(range(len(self._files)))
        for i, file, label in zip(idx, self._files, self._labels, strict=True):
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
                    f"gravity {self._gravity} fill {self._color} text {self._pos[0]},{self._pos[1]} '{label}'",
                    f"{str(i)}.png",
                ]
            )
        # Create horizontal subfigures
        for j in range(self._h):
            # Choose first n items in the list
            idx_sub = idx[j * self._w : (j + 1) * self._w]
            subprocess.call(
                ["convert", "+append"]
                + [f"{str(i)}.png" for i in idx_sub]
                + [f"subfigure_{j}.png"]
            )

        # Create vertical subfigures from horizontal subfigures
        subprocess.call(
            ["convert", "-append"]
            + [f"subfigure_{j}.png" for j in range(self._h)]
            + [str(self._output)]
        )

        # Delete temporary files
        subprocess.call(
            ["rm"]
            + [f"{str(i)}.png" for i in idx]
            + [f"subfigure_{j}.png" for j in range(self._h)]
        )

    def help(self) -> None:
        """Print commands that are used."""
        print(
            "To create images with labels:\n"
            "    convert in-1.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 0,0 '(a)'\" a.png\n"
            "    convert in-2.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 0,0 '(b)'\" b.png\n"
            "    convert in-3.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 0,0 '(c)'\" c.png\n"
            "    convert in-4.png -font Times-New-Roman -pointsize 100 -draw \"gravity northwest fill black text 0,0 '(d)'\" d.png\n"
            "Then to combine them horizontally:\n"
            "    convert +append a.png b.png ab.png\n"
            "    convert +append c.png d.png cd.png\n"
            "And finally stack them vertically:\n"
            "    convert -append ab.png cd.png out.png\n"
            "Optionally delete all temporary files:\n"
            "    rm a.png b.png c.png d.png ab.png cd.png"
        )


def combine(*files: str) -> Combine:
    """Give all files that should be combined.

    Parameters
    ----------
    files : str
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


if __name__ == "__main__":
    combine(
        "file1.png", "file2.png", "file3.png", "file4.png", "file5.png", "file6.png"
    ).using(fontsize=120).in_grid(w=2, h=3).with_labels(
        "a", "b", "c", "d", "e", "f"
    ).save()
    combine().help()
