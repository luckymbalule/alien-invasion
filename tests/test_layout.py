import pytest
from layout import row_layout, col_layout


@pytest.mark.parametrize(("width,screen_width,expected_cols,"
"expected_step,expected_start"), [
    (50, 900, 8, 100, 75),
    (50, 480, 4, 100, 65)
])
def test_compute_column_layout(width, screen_width, expected_cols,
                expected_step, expected_start):
    col = col_layout(
        scr_w=screen_width,
        asset_w=width
    )

    assert col.count == expected_cols
    assert col.step == expected_step
    assert col.start == expected_start


@pytest.mark.parametrize(("height,screen_height,top_margin,bottom_margin,"
"buffer_rows,expected_rows,expected_step"), [
    (50, 900, 55, 30, 2, 7, 100),
    (50, 640, 60, 40, 2, 4, 100)
])
def test_compute_row_layout(height, screen_height, top_margin,
            bottom_margin, buffer_rows, expected_rows, expected_step):

    row = row_layout(
        scr_h=screen_height,
        asset_h=height,
        bottom=bottom_margin,
        top=top_margin,
        buf_rows=buffer_rows
    )

    assert row.count == expected_rows
    assert row.step == expected_step
    assert row.start == top_margin