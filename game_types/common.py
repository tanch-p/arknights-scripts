from typing import TypedDict


class Blackboard(TypedDict):
    key: str
    value: float
    valueStr: str | None


class ItemCost(TypedDict):
    id: str
    count: int
    type: str  # e.g. "MATERIAL"
