from __future__ import annotations

from typing import TypedDict


class ActivityBasicInfo(TypedDict):
    id: str
    type: str  # "TYPE_ACT9D0" | "TYPE_SIDESTORY" | ...
    displayType: str  # "SIDESTORY" | "MAINLINE" | ...
    name: str
    startTime: int
    endTime: int
    rewardEndTime: int
    displayOnHome: bool
    hasStage: bool
    templateShopId: str | None
    medalGroupId: str | None
    ungroupedMedalIds: list[str] | None
    isReplicate: bool
    needFixedSync: bool
    trapDomainId: str | None
    recType: str  # "SPECIAL" | "NONE" | ...
    isPageEntry: bool
    isMagnify: bool
    picGroup: list[str]
    usePicGroup: bool


class HomeActConfig(TypedDict):
    actId: str
    isPopupAfterCheckin: bool
    showTopBarMenu: bool
    actTopBarColor: str | None
    actTopBarText: str | None


class MissionReward(TypedDict):
    type: str
    id: str
    count: int


class MissionData(TypedDict):
    id: str
    sortId: int
    description: str
    type: str  # "ACTIVITY" | "DAILY" | "WEEKLY" | ...
    itemBgType: str  # "COMMON" | "RARE" | ...
    preMissionIds: list[str] | None
    template: str
    templateType: str
    param: list[str]
    unlockCondition: str | None
    unlockParam: list[str] | None
    missionGroup: str
    toPage: str | None
    periodicalPoint: int
    rewards: list[MissionReward]
    backImagePath: str | None
    foldId: str | None
    haveSubMissionToUnlock: bool
    countEndTs: int


class MissionGroup(TypedDict):
    id: str
    title: str | None
    type: str
    preMissionGroup: str | None
    period: object | None
    rewards: list[MissionReward]
    missionIds: list[str]
    startTs: int
    endTs: int


class ActThemeTimeNode(TypedDict):
    title: str
    ts: int


class ActTheme(TypedDict):
    id: str
    type: str
    funcId: str
    endTs: int
    sortId: int
    itemId: str
    timeNodes: list[ActThemeTimeNode]
    picGroups: list[object]
    startTs: int


class ActivityTable(TypedDict):
    basicInfo: dict[str, ActivityBasicInfo]
    homeActConfig: dict[str, HomeActConfig]
    zoneToActivity: dict[str, str]  # zone ID → activity ID
    actTimeTrackPoint: dict[str, object]
    missionData: list[MissionData]
    missionGroup: list[MissionGroup]
    replicateMissions: None
    activity: dict[str, object]
    extraData: dict[str, object]
    activityItems: dict[str, list[str]]  # activity ID → item ID list
    syncPoints: dict[str, list[int]]  # activity ID → [startTs, endTs]
    dynActs: dict[str, object]
    stageRewardsData: dict[str, object]
    actThemes: list[ActTheme]
    actFunData: dict[str, object]
    carData: dict[str, object]
    siracusaData: dict[str, object]
    fireworkData: dict[str, object]
    halfIdleData: dict[str, object]
    kvSwitchData: dict[str, object]
    dynEntrySwitchData: dict[str, object]
    hiddenStageData: list[object]
    missionArchives: dict[str, object]
    fifthAnnivExploreData: dict[str, object]
    autoChessData: dict[str, object]
    stringRes: dict[str, object]
    activityTraps: dict[str, object]
    activityTrapMissions: dict[str, object]
    trapRuneDataDict: dict[str, object]
    activityTemplateMissionStyles: dict[str, object]
    activityCrossDayTrackTypeDataDict: dict[str, object]
    activityCrossDayTrackTypeMap: dict[str, object]
    activityStoryReadTipsDatas: dict[str, object]
