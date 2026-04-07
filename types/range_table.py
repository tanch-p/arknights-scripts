from __future__ import annotations

from typing import TypedDict


class GridCell(TypedDict):
    row: int
    col: int


class RangeEntry(TypedDict):
    id: str
    direction: int
    grids: list[GridCell]


# Top-level type: range ID → entry
RangeTable = dict[str, RangeEntry]
