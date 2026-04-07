from __future__ import annotations

from typing import TypedDict

from character_table import UnlockCondition
from common import Blackboard


class EquipTalentCandidate(TypedDict):
    displayRangeId: bool
    upgradeDescription: str
    talentIndex: int
    validModeIndices: list[int] | None
    unlockCondition: UnlockCondition
    requiredPotentialRank: int
    prefabKey: str | None
    name: str | None
    description: str | None
    rangeId: str | None
    blackboard: list[Blackboard]
    tokenKey: str | None
    isHideTalent: bool


class TalentDataBundle(TypedDict):
    candidates: list[EquipTalentCandidate] | None


class EquipTraitCandidate(TypedDict):
    additionalDescription: str | None
    unlockCondition: UnlockCondition
    requiredPotentialRank: int
    blackboard: list[Blackboard]
    overrideDescripton: str | None  # sic: game data typo
    prefabKey: str | None
    rangeId: str | None


class TraitDataBundle(TypedDict):
    candidates: list[EquipTraitCandidate] | None


class EquipPart(TypedDict):
    resKey: str | None
    target: str  # "TRAIT" | "TALENT" | "TALENT_DATA_ONLY"
    isToken: bool
    validInGameTag: str | None
    validInMapTag: str | None
    addOrOverrideTalentDataBundle: TalentDataBundle
    overrideTraitDataBundle: TraitDataBundle


class EquipPhase(TypedDict):
    equipLevel: int
    parts: list[EquipPart]
    attributeBlackboard: list[Blackboard]
    tokenAttributeBlackboard: dict[str, list[Blackboard]]


class BattleEquipEntry(TypedDict):
    phases: list[EquipPhase]


# Top-level type: equip ID → entry
BattleEquipTable = dict[str, BattleEquipEntry]
