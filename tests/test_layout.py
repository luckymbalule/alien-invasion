import pytest
from layout import row_layout, col_layout, stack_vertical


@pytest.mark.parametrize(("width,screen_width,expected_cols,"
"expected_step,expected_start"), [
    (50, 900, 8, 100, 75),
    (50, 480, 4, 100, 65)
])
def test_col_layout_returns_correct_count_step_and_start(
    width, screen_width, expected_cols, expected_step, expected_start
):
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
def test_row_layout_returns_correct_count_step_and_start(
    height, screen_height, top_margin, bottom_margin, buffer_rows, expected_rows,
expected_step):

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


@pytest.mark.parametrize(
    "coordinates, size, count, step, expected_coords", [
        # Format: (x,y), (w,h), count, step, [(x,y)]
        ((250, 300), (50, 70), 1, 40, [(225, 265)]),
        ((300, 400), (85, 50), 3, 30,
            [(258, 295), (258, 375), (258, 455)]
        ),
        ((0, 0), (90, 60), 2, 25,
            [(0, 0), (0, 85)]
        )
    ]
)
def test_stack_vertical_returns_correct_vertical_stack_positions(
    coordinates, size, count, step, expected_coords
):
    w, h = size

    coords = stack_vertical(
        position=coordinates,
        item_w=w,
        item_h=h,
        count=count,
        step=step,
    )

    assert len(coords) == count
    assert coords == expected_coords