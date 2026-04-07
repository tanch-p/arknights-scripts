from __future__ import annotations

from typing import TypedDict

from .common import ItemCost


class TimeOfDay(TypedDict):
    Hour: int
    Minute: int


class FeverGameData(TypedDict):
    feverDuration: float
    feverNeed: float


class GamedataConst(TypedDict):
    maxPlayerLevel: int
    playerExpMap: list[int]  # exp required per player level
    playerApMap: list[int]  # max AP per player level
    maxLevel: list[list[int]]  # max char level per rarity (index) and phase
    characterExpMap: list[list[int]]  # exp cost tables by phase group
    characterUpgradeCostMap: list[list[int]]  # gold cost tables by phase group
    evolveGoldCost: list[list[int]]  # gold cost per rarity and elite phase; -1 = N/A
    completeGainBonus: float
    playerApRegenSpeed: int
    maxPracticeTicket: int
    advancedGachaCrystalCost: int
    completeCrystalBonus: int
    initPlayerGold: int
    initPlayerDiamondShard: int
    initCampaignTotalFee: int
    initRecruitTagList: list[str]
    initCharIdList: list[str]
    attackMax: float
    defMax: float
    hpMax: float
    reMax: float
    diamondToShdRate: int
    requestSameFriendCD: int
    baseMaxFriendNum: int
    maxStarFriendNum: int
    maxSquadAssistDisplayNum: int
    friendStarEditTrackTs: int
    hardDiamondDrop: int
    instFinDmdShdCost: int
    easyCrystalBonus: int
    diamondMaterialToShardExchangeRatio: int
    diamondHandbookStageGain: int
    apBuyCost: int
    apBuyThreshold: int
    creditLimit: int
    monthlySubRemainTimeLimitDays: int
    friendAssistRarityLimit: list[int]  # min rarity per assist slot; -1 = no limit
    mainlineCompatibleDesc: str
    mainlineToughDesc: str
    mainlineEasyDesc: str
    mainlineNormalDesc: str
    rejectSpCharMission: int
    addedRewardDisplayZone: str
    oneDiamondAp: int
    charRotationPresetMaxCnt: int
    charRotationSkinListMaxCnt: int
    defaultCRPresetCharId: str
    defaultCRPresetCharSkinId: str
    defaultCRPresetBGId: str
    defaultCRPresetThemeId: str
    defaultCRPresetName: str
    charRotationPresetTrackTs: int
    uniequipArchiveSysTrackTs: int
    manufactPromptTime: int
    mainGuideActivedStageId: str
    richTextStyles: dict[str, str]
    charAssistRefreshTime: list[TimeOfDay]
    normalRecruitLockedString: list[str]
    commonPotentialLvlUpCount: int
    weeklyOverrideDesc: str
    voucherDiv: int
    recruitPoolVersion: int
    v006RecruitTimeStep1Refresh: int
    v006RecruitTimeStep2Check: int
    v006RecruitTimeStep2Flush: int
    buyApTimeNoLimitFlag: bool
    isLMGTSEnabled: bool
    legacyTime: int
    legacyItemList: list[ItemCost]
    useAssistSocialPt: int
    useAssistSocialPtMaxCount: int
    assistBeUsedSocialPt: dict[str, int]  # assist type → social point reward
    pushForces: list[float]
    pushForceZeroIndex: int
    normalGachaUnlockPrice: list[int]  # -1 = free
    pullForces: list[float]
    pullForceZeroIndex: int
    multiInComeByRank: list[str]
    LMTGSToEPGSRatio: int
    newBeeGiftEPGS: int
    lMTGSDescConstOne: str
    lMTGSDescConstTwo: str
    defCDPrimColor: str
    defCDSecColor: str
    mailBannerType: list[str]
    monthlySubWarningTime: int
    UnlimitSkinOutOfTime: int
    replicateShopStartTime: int
    TSO: int
    isDynIllustEnabled: bool
    isDynIllustStartEnabled: bool
    isClassicQCShopEnabled: bool
    isRoguelikeTopicFuncEnabled: bool
    isSandboxPermFuncEnabled: bool
    isRoguelikeAvgAchieveFuncEnabled: bool
    isClassicPotentialItemFuncEnabled: bool
    isClassicGachaPoolFuncEnabled: bool
    isSpecialGachaPoolFuncEnabled: bool
    isVoucherClassicItemDistinguishable: bool
    isRecalRuneFuncEnabled: bool
    voucherSkinRedeem: int
    voucherSkinDesc: str
    charmEquipCount: int
    termDescriptionDict: dict[str, str]
    storyReviewUnlockItemLackTip: str
    dataVersion: str
    resPrefVersion: str
    announceWebBusType: str
    videoPlayerWebBusType: str
    gachaLogBusType: str
    defaultMinMultipleBattleTimes: int
    defaultMaxMultipleBattleTimes: int
    multipleActionOpen: bool
    subProfessionDamageTypePairs: dict[str, str]  # subProfessionId → damage type
    classicProtectChar: list[str]
    feverGameData: FeverGameData
    birthdaySettingDesc: str
    birthdaySettingConfirmDesc: str
    birthdaySettingLeapConfirmDesc: str
    leapBirthdayRewardMonth: int
    leapBirthdayRewardDay: int
    birthdaySettingShowStageId: str
    isBirthdayFuncEnabled: bool
    isSoCharEnabled: bool
