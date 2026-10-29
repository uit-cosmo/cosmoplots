import matplotlib.pyplot as plt

import cosmoplots


def test_generate_hex_colors():
    color_list = cosmoplots.generate_hex_colors(5, "viridis", show_swatch=False)
    assert len(color_list) == 5
    assert color_list[0] == "#fde725"
    assert color_list[-1] == "#440154"


def test_generate_hex_colors_descending_with_swatch():
    color_list = cosmoplots.generate_hex_colors(
        3, "viridis", show_swatch=True, ascending=False
    )
    assert color_list == ["#440154", "#21918c", "#fde725"]
    plt.close("all")
