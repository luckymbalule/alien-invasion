from typing import NamedTuple

class LayoutSpec(NamedTuple):
    count: int
    step: int
    start: int


def row_layout(*, scr_w: int, asset_w: int) -> LayoutSpec:
    """
    Calculate asset count that fit screen width

    Inequality:
    asset_w * (2N + 1) <= scr_w
    """
    step = asset_w * 2
    count = (scr_w - asset_w) // step
    start = (scr_w - (asset_w * (2 * count - 1))) // 2

    return LayoutSpec(count=int(count), step=int(step), start=int(start))


def col_layout(*, scr_h: int, asset_h: int, top: int, bottom: int,
                buf_rows=0) -> LayoutSpec:
    """
    Calculate column in respect to top, bottom and empty buffers

    Inequality:
    asset_h * (2N - 1) + top + bottom + asset_h * (2*buf_rows - 1) 
    <= scr_h
    """

    step = 2 * asset_h    
    buf_h = asset_h * (2 * buf_rows - 1) if buf_rows > 0 else 0
    count = (scr_h - (-asset_h + top + bottom + buf_h)) // step

    return LayoutSpec(count=int(count), step=int(step), start=int(top))