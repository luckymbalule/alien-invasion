from typing import NamedTuple

class LayoutSpec(NamedTuple):
    count: int
    step: int
    start: int


def col_layout(*, scr_w: int, asset_w: int) -> LayoutSpec:
    """
    Calculate asset count that fit screen width

    Inequality:
    asset_w * (2N + 1) <= scr_w
    """
    step = asset_w * 2
    count = (scr_w - asset_w) // step
    start = (scr_w - (asset_w * (2 * count - 1))) // 2

    return LayoutSpec(count=int(count), step=int(step), start=int(start))


def row_layout(*, scr_h: int, asset_h: int, top: int, bottom: int,
                buf_rows=0) -> LayoutSpec:
    """
    Calculates rows fitting screen height in respect to y margins and
    buffer space

    Inequality:
    asset_h * (2N - 1) + top + bottom + asset_h * (2*buf_rows - 1) 
    <= scr_h
    """

    step = 2 * asset_h    
    buf_h = asset_h * (2 * buf_rows - 1) if buf_rows > 0 else 0
    count = (scr_h - (-asset_h + top + bottom + buf_h)) // step

    return LayoutSpec(count=int(count), step=int(step), start=int(top))


def stack_vertical(*, position: list, item_w: int, item_h: int,
            count: int, step: int) -> list[tuple[int, int]]:
    """
    
    """

    stack_height = item_h * count + (step * (count - 1))
    x, y = position

    start_y = y - stack_height // 2
    if start_y < 0:
        start_y = 0
    
    start_x = x - item_w // 2
    if start_x < 0:
        start_x = 0
    
    return [
        (start_x, start_y + i * (item_h + step))
        for i in range(count)
    ]