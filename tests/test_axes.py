import matplotlib.pyplot as plt

import cosmoplots


def test_subfigure_labels_beyond_26():
    fig, axes = cosmoplots.figure_multiple_rows_columns(8, 4)
    labels = [ax.texts[0].get_text() for ax in axes]
    assert labels[0] == r"$\mathrm{(a)}$"
    assert labels[25] == r"$\mathrm{(z)}$"
    assert labels[26] == r"$\mathrm{(aa)}$"
    assert labels[31] == r"$\mathrm{(af)}$"
    plt.close(fig)


def test_subfigure_label_sequence():
    assert cosmoplots.axes._subfigure_label(0) == "a"
    assert cosmoplots.axes._subfigure_label(51) == "az"
    assert cosmoplots.axes._subfigure_label(52) == "ba"
    assert cosmoplots.axes._subfigure_label(701) == "zz"
    assert cosmoplots.axes._subfigure_label(702) == "aaa"
