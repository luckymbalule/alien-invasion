from layout import row_layout, col_layout


def test_compute_row():
    asset_width = 50
    screen_width = 900

    row = row_layout(
        scr_w=screen_width,
        asset_w=asset_width
    )

    assert row.count == 8
    assert row.step == 100
    assert row.start == 75


def test_compute_column_layout():
    asset_height = 50
    screen_height = 900
    top_margin = 55

    col = col_layout(
        scr_h=screen_height,
        asset_h=asset_height,
        bottom=30,
        top=top_margin,
        buf_rows=2
    )

    assert col.count == 7
    assert col.step == 100
    assert col.start == top_margin