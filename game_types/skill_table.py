from __future__ import annotations

from typing import TypedDict

from .common import Blackboard, ItemCost


class SpData(TypedDict):
    spType: str  # "INCREASE_WITH_TIME" | "INCREASE_WHEN_ATTACK" | "INCREASE_WHEN_TAKEN_DAMAGE" | "8"
    levelUpCost: list[ItemCost] | None
    maxChargeTime: int
    spCost: int
    initSp: int
    increment: float


class SkillLevel(TypedDict):
    name: str
    rangeId: str | None
    description: str | None
    skillType: str  # "AUTO" | "MANUAL" | "PASSIVE"
    durationType: str  # "NONE" | "AMMO"
    spData: SpData
    prefabId: str | None
    duration: float
    blackboard: list[Blackboard]


class SkillTableEntry(TypedDict):
    skillId: str
    iconId: str | None
    hidden: bool
    levels: list[SkillLevel]


# Top-level type: skill ID → entry
SkillTable = dict[str, SkillTableEntry]
