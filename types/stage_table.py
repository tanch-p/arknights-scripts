from __future__ import annotations

from typing import TypedDict

from common import ItemCost


class StageUnlockCondition(TypedDict):
    stageId: str
    completeState: str  # "PASS" | "COMPLETE"


class DropItem(TypedDict):
    type: str
    id: str
    dropType: str  # "ONCE" | "NORMAL" | "COMPLETE" | "ADDITIONAL"


class DetailDropItem(TypedDict):
    occPercent: str  # "ALWAYS" | "SOMETIMES" | "OFTEN" | "RARE"
    type: str
    id: str
    dropType: str


class StageDropInfo(TypedDict):
    firstPassRewards: list[ItemCost] | None
    firstCompleteRewards: list[ItemCost] | None
    passRewards: list[list[ItemCost]] | None
    completeRewards: list[list[ItemCost]] | None
    displayRewards: list[DropItem]
    displayDetailRewards: list[DetailDropItem]


class StageExtraCondition(TypedDict):
    index: int
    template: str
    unlockParam: list[str]


class StageExtraInfoProgressInfo(TypedDict):
    progressType: str
    descList: list[str] | None


class StageExtraInfo(TypedDict):
    stageId: str
    rewards: list[ItemCost]
    progressInfo: StageExtraInfoProgressInfo
    imageId: str
    keyItemId: str | None
    unlockDesc: str | None


class StageEntry(TypedDict):
    stageType: str  # "MAIN" | "SUB" | "ACTIVITY" | "DAILY" | ...
    difficulty: str  # "NORMAL" | "FOUR_STAR" | "STORY"
    performanceStageFlag: str
    diffGroup: str  # "NONE" | "EASY" | "NORMAL" | "TOUGH" | ...
    unlockCondition: list[StageUnlockCondition]
    stageId: str
    levelId: str
    zoneId: str
    code: str
    name: str
    description: str
    hardStagedId: str | None
    sixStarStageId: str | None
    dangerLevel: str
    dangerPoint: float
    loadingPicId: str
    canPractice: bool
    canBattleReplay: bool
    apCost: int
    apFailReturn: int
    maxSlot: int
    etItemId: str | None
    etCost: int
    etFailReturn: int
    etButtonStyle: str | None
    apProtectTimes: int
    diamondOnceDrop: int
    practiceTicketCost: int
    dailyStageDifficulty: int
    expGain: int
    goldGain: int
    loseExpGain: int
    loseGoldGain: int
    passFavor: int
    completeFavor: int
    slProgress: int
    displayMainItem: str
    hilightMark: bool
    bossMark: bool
    isPredefined: bool
    isHardPredefined: bool
    isSkillSelectablePredefined: bool
    isStoryOnly: bool
    appearanceStyle: str
    stageDropInfo: StageDropInfo
    canUseCharm: bool
    canUseTech: bool
    canUseTrapTool: bool
    canUseBattlePerformance: bool
    canUseFirework: bool
    canMultipleBattle: bool
    startButtonOverrideId: str | None
    isStagePatch: bool
    mainStageId: str
    extraCondition: list[StageExtraCondition] | None
    extraInfo: list[StageExtraInfo] | None
    sixStarBaseDesc: str | None
    sixStarDisplayRewardList: list[ItemCost] | None
    advancedRuneIdList1: list[str]
    advancedRuneIdList2: list[str]
    useSpecialSizeMapPreview: bool


class MapTheme(TypedDict):
    themeId: str
    unitColor: str
    buildableColor: str | None
    themeType: str | None
    trapTintColor: str | None
    emissionColor: str | None


class TileInfo(TypedDict):
    tileKey: str
    name: str
    description: str
    isFunctional: bool


class ForceOpenEntry(TypedDict):
    id: str
    startTime: int
    endTime: int
    forceOpenList: list[str]


class TimelyStageDropInfo(TypedDict):
    startTs: int
    endTs: int
    stagePic: str
    dropPicId: str
    stageUnlock: str
    entranceDownPicId: str
    entranceUpPicId: str
    timelyGroupId: str
    weeklyPicId: str
    isReplace: bool
    apSupplyOutOfDateDict: dict[str, object]


class StageValidInfo(TypedDict):
    startTs: int
    endTs: int


class StageFogInfo(TypedDict):
    lockId: str
    fogType: str
    stageButtonInFogRenderType: str
    stageId: str
    lockName: str
    lockDesc: str
    unlockItemId: str
    unlockItemType: str
    unlockItemNum: int
    preposedStageId: str | None
    preposedLockId: str | None


class StageStartCondRequireChar(TypedDict):
    charId: str
    evolvePhase: str


class StageStartCond(TypedDict):
    requireChars: list[StageStartCondRequireChar]
    excludeAssists: list[str]
    isNotPass: bool


class DiffGroupEntry(TypedDict):
    normalId: str | None
    toughId: str | None
    easyId: str | None


class StoryStageShowItem(TypedDict):
    displayRecordId: str
    stageId: str
    accordingStageId: str | None
    diffGroup: str


class SpecialBattleFinishStageData(TypedDict):
    stageId: str
    skipAccomplishPerform: bool


class SixStarRuneData(TypedDict):
    runeId: str
    runeDesc: str
    runeKey: str


class SixStarMilestoneMilestone(TypedDict):
    id: str
    sortId: int
    nodePoint: int
    rewardType: str
    unlockStageFog: str | None
    unlockStageId: str | None
    unlockStageName: str | None
    rewardList: list[ItemCost]


class SixStarMilestoneInfo(TypedDict):
    groupId: str
    stageIdList: list[str]
    milestoneDataList: list[SixStarMilestoneMilestone]


class SixStarCompatibleInfo(TypedDict):
    stageId: str
    apCost: int
    apFailReturn: int
    dropType: str


class ApProtectTimeRange(TypedDict):
    startTs: int
    endTs: int


class ApProtectZoneInfo(TypedDict):
    zoneId: str
    timeRanges: list[ApProtectTimeRange]


class CgGalleryDisplay(TypedDict):
    displayId: str
    cgList: list[str]
    cgSource: str
    displayName: str
    displayDesc: str
    storySetId: str
    sortId: int
    relatedStoryId: str | None
    relatedStageId: str | None


class CgGalleryGroup(TypedDict):
    storySetId: str
    storylineId: str
    locationId: str
    displays: list[str]


class CgGalleryCg(TypedDict):
    cgId: str
    cgType: str
    cgPath: str


class StageTable(TypedDict):
    stages: dict[str, StageEntry]
    runeStageGroups: dict[str, object]
    mapThemes: dict[str, MapTheme]
    tileInfo: dict[str, TileInfo]
    forceOpenTable: dict[str, ForceOpenEntry]
    timelyStageDropInfo: dict[str, TimelyStageDropInfo]
    overrideDropInfo: dict[str, object]
    overrideUnlockInfo: dict[str, object]
    timelyTable: dict[str, object]
    stageValidInfo: dict[str, StageValidInfo]
    stageFogInfo: dict[str, StageFogInfo]
    stageStartConds: dict[str, StageStartCond]
    diffGroupTable: dict[str, DiffGroupEntry]
    storyStageShowGroup: dict[str, dict[str, StoryStageShowItem]]
    specialBattleFinishStageData: dict[str, SpecialBattleFinishStageData]
    recordRewardData: None
    apProtectZoneInfo: dict[str, ApProtectZoneInfo]
    antiSpoilerDict: dict[str, list[str]]
    actCustomStageDatas: dict[str, object]
    spNormalStageIdFor4StarList: list[str]
    storylines: dict[str, object]
    storylineStorySets: dict[str, object]
    storylineTags: dict[str, object]
    storylineConst: dict[str, object]
    cgGalleryDisplays: dict[str, CgGalleryDisplay]
    cgGalleryGroups: dict[str, CgGalleryGroup]
    cgGalleryCgs: dict[str, object]
    sixStarRuneData: dict[str, SixStarRuneData]
    sixStarMilestoneInfo: dict[str, SixStarMilestoneInfo]
    sixStarCompatibleInfo: dict[str, SixStarCompatibleInfo]
    conditionalDropInfo: dict[str, object]
