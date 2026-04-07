from __future__ import annotations

from typing import TypedDict

from .common import ItemCost


class UniEquipEntry(TypedDict):
    uniEquipId: str
    uniEquipName: str
    uniEquipIcon: str
    uniEquipDesc: str
    typeIcon: str
    typeName1: str
    typeName2: str | None
    equipShiningColor: str
    showEvolvePhase: str  # "PHASE_0" | "PHASE_1" | "PHASE_2"
    unlockEvolvePhase: str  # "PHASE_0" | "PHASE_1" | "PHASE_2"
    charId: str
    tmplId: str | None
    showLevel: int
    unlockLevel: int
    missionList: list[str]
    unlockFavors: dict[str, int] | None  # stage "1"/"2"/"3" → favor value
    itemCost: dict[str, list[ItemCost]] | None  # stage "1"/"2"/"3" → cost list
    type: str  # "INITIAL" | "ADVANCED"
    uniEquipGetTime: int
    uniEquipShowEnd: int
    charEquipOrder: int
    hasUnlockMission: bool
    isSpecialEquip: bool
    specialEquipDesc: str | None
    specialEquipColor: str | None
    charColor: str


class UniEquipMission(TypedDict):
    template: str
    desc: str
    paramList: list[str]
    uniEquipMissionId: str
    uniEquipMissionSort: int
    uniEquipId: str
    jumpStageId: str | None


class SubProfEntry(TypedDict):
    subProfessionId: str
    subProfessionName: str
    subProfessionCatagory: int


class EquipTypeInfo(TypedDict):
    uniEquipTypeName: str
    sortId: int
    isSpecial: bool
    isInitial: bool


class EquipTrackItem(TypedDict):
    charId: str
    equipId: str
    type: str
    archiveShowTimeEnd: int


class EquipTrackEntry(TypedDict):
    timeStamp: int
    trackList: list[EquipTrackItem]


class UniEquipTable(TypedDict):
    equipDict: dict[str, UniEquipEntry]
    missionList: dict[str, UniEquipMission]
    subProfDict: dict[str, SubProfEntry]
    subProfToProfDict: dict[str, int]
    charEquip: dict[str, list[str]]  # char ID → list of equip IDs
    equipTypeInfos: list[EquipTypeInfo]
    equipTrackDict: list[EquipTrackEntry]
