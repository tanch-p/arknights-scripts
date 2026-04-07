from __future__ import annotations

from typing import TypedDict

from common import ItemCost


class ZoneEntry(TypedDict):
    zoneID: str
    zoneIndex: int
    type: str  # "MAINLINE" | "WEEKLY" | "ACTIVITY" | ...
    zoneNameFirst: str
    zoneNameSecond: str
    zoneNameTitleCurrent: str
    zoneNameTitleUnCurrent: str
    zoneNameTitleEx: str
    zoneNameThird: str
    lockedText: str
    antiSpoilerId: str | None
    canPreview: bool
    hasAdditionalPanel: bool
    sixStarMilestoneGroupId: str | None
    bindMainlineZoneId: str | None
    bindMainlineRetroZoneId: str | None
    diamondRewardCount: int


class WeeklyAdditionInfo(TypedDict):
    daysOfWeek: list[int]  # 1=Monday … 7=Sunday
    type: str  # "EVOLVE" | ...


class ZoneValidInfo(TypedDict):
    startTs: int
    endTs: int


class MainlineAdditionInfo(TypedDict):
    zoneId: str
    chapterId: str
    preposedZoneId: str | None
    zoneIndex: int
    startStageId: str
    endStageId: str
    gameMusicId: str
    recapId: str
    recapPreStageId: str
    buttonName: str
    buttonStyle: str  # "NONE" | ...
    spoilAlert: bool
    zoneOpenTime: int
    diffGroup: list[str]  # "NORMAL" | "EASY" | "TOUGH" | ...


class RecordRewardStage(TypedDict):
    bindStageId: str
    stageDiff1: str
    stageDiff: str
    picRes: str
    textPath: str
    textDesc: str
    recordReward: list[ItemCost]


class ZoneRecord(TypedDict):
    recordId: str
    zoneId: str
    recordTitleName: str
    preRecordId: str | None
    nodeTitle1: str | None
    nodeTitle2: str | None
    rewards: list[RecordRewardStage]


class ZoneRecordGroup(TypedDict):
    zoneId: str
    records: list[ZoneRecord]


class ZoneRecordMission(TypedDict):
    missionId: str
    recordStageId: str
    templateDesc: str
    desc: str


class ZoneMetaData(TypedDict):
    ZoneRecordMissionData: dict[str, ZoneRecordMission]


class ZoneTable(TypedDict):
    zones: dict[str, ZoneEntry]
    weeklyAdditionInfo: dict[str, WeeklyAdditionInfo]
    zoneValidInfo: dict[str, ZoneValidInfo]
    mainlineAdditionInfo: dict[str, MainlineAdditionInfo]
    zoneRecordGroupedData: dict[str, ZoneRecordGroup]
    zoneRecordRewardData: dict[str, list[str]]  # zone ID → list of stage IDs
    mainlineZoneIdList: list[str]
    zoneMetaData: ZoneMetaData
