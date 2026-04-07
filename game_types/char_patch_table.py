from __future__ import annotations

from typing import TypedDict

from .character_table import CharacterTableEntry


class PatchInfo(TypedDict):
    tmplIds: list[str]
    default: str


class UnlockCond(TypedDict):
    stageId: str
    completeState: str
    unlockTs: int


class UnlockCondGroup(TypedDict):
    conds: list[UnlockCond]


class PatchDetailInfo(TypedDict):
    patchId: str
    sortId: int
    infoParam: str
    transSortId: int


class CharPatchTable(TypedDict):
    infos: dict[str, PatchInfo]
    patchChars: dict[str, CharacterTableEntry]
    unlockConds: dict[str, UnlockCondGroup]
    patchDetailInfoList: dict[str, PatchDetailInfo]
