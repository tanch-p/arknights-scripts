from __future__ import annotations

from typing import TypedDict


class RoguelikeStageEntry(TypedDict):
    id: str
    linkedStageId: str
    levelId: str
    levelReplaceIds: list[str]
    code: str
    name: str
    loadingPicId: str
    description: str
    eliteDesc: str | None
    isBoss: int
    isElite: int
    difficulty: str  # "NORMAL" | "FOUR_STAR" | ...
    capsulePool: str | None  # Only for ro1
    capsuleProb: float  # Only for ro1
    vutresProb: list[float]  # Only for ro1
    boxProb: list[float]
    specialNodeId: str | None  # For boss stages with the big icon in the background
    redCapsulePool: str | None  # Only for ro1
    redCapsuleProb: float  # Only for ro1


RoguelikeStages = dict[str, RoguelikeStageEntry]
