from __future__ import annotations
from .common import Blackboard, ItemCost
from typing import TypedDict


class UnlockCondition(TypedDict):
    phase: str  # "PHASE_0" | "PHASE_1" | "PHASE_2"
    level: int


class AttributeData(TypedDict):
    maxHp: int
    atk: int
    def_: int  # note: key in JSON is "def"
    magicResistance: float
    cost: int
    blockCnt: int
    moveSpeed: float
    attackSpeed: float
    baseAttackTime: float
    respawnTime: int
    hpRecoveryPerSec: float
    spRecoveryPerSec: float
    maxDeployCount: int
    maxDeckStackCnt: int
    tauntLevel: int
    massLevel: int
    baseForceLevel: int
    stunImmune: bool
    silenceImmune: bool
    sleepImmune: bool
    frozenImmune: bool
    levitateImmune: bool
    disarmedCombatImmune: bool
    fearedImmune: bool
    palsyImmune: bool
    attractImmune: bool


class AttributeKeyFrame(TypedDict):
    level: int
    data: AttributeData


class Phase(TypedDict):
    characterPrefabKey: str
    rangeId: str
    maxLevel: int
    attributesKeyFrames: list[AttributeKeyFrame]
    evolveCost: list[ItemCost] | None


class SkillLevelUpCostCond(TypedDict):
    unlockCond: UnlockCondition
    lvlUpTime: int
    levelUpCost: list[ItemCost] | None


class SkillRef(TypedDict):
    skillId: str
    overridePrefabKey: str | None
    overrideTokenKey: str | None
    levelUpCostCond: list[SkillLevelUpCostCond]
    unlockCond: UnlockCondition


class TalentCandidate(TypedDict):
    unlockCondition: UnlockCondition
    requiredPotentialRank: int
    prefabKey: str | None
    name: str | None
    description: str | None
    rangeId: str | None
    blackboard: list[Blackboard]
    tokenKey: str | None
    isHideTalent: bool


class Talent(TypedDict):
    candidates: list[TalentCandidate] | None


class TraitCandidate(TypedDict):
    unlockCondition: UnlockCondition
    requiredPotentialRank: int
    blackboard: list[Blackboard]
    overrideDescripton: str | None  # sic: game data has this typo
    prefabKey: str | None
    rangeId: str | None


class Trait(TypedDict):
    candidates: list[TraitCandidate]


class AttributeModifier(TypedDict):
    attributeType: str
    formulaItem: str
    value: float
    loadFromBlackboard: bool
    fetchBaseValueFromSourceEntity: bool


class BuffAttributes(TypedDict):
    abnormalFlags: list | None
    abnormalImmunes: list | None
    abnormalAntis: list | None
    abnormalCombos: list | None
    abnormalComboImmunes: list | None
    attributeModifiers: list[AttributeModifier] | None


class Buff(TypedDict):
    attributes: BuffAttributes


class PotentialRank(TypedDict):
    type: str  # "BUFF" | "CUSTOM"
    description: str
    buff: Buff | None
    equivalentCost: object | None


class PowerInfo(TypedDict):
    nationId: str | None
    groupId: str | None
    teamId: str | None


class SkillLvlup(TypedDict):
    unlockCond: UnlockCondition
    lvlUpCost: list[ItemCost] | None


class CharacterTableEntry(TypedDict):
    name: str
    description: str | None
    sortIndex: int
    spTargetType: str
    spTargetId: str | None
    canUseGeneralPotentialItem: bool
    canUseActivityPotentialItem: bool
    potentialItemId: str | None
    activityPotentialItemId: str | None
    classicPotentialItemId: str | None
    nationId: str | None
    groupId: str | None
    teamId: str | None
    mainPower: PowerInfo
    subPower: list[PowerInfo] | None
    displayNumber: str | None
    appellation: str
    position: str  # "MELEE" | "RANGED"
    tagList: list[str] | None
    itemUsage: str | None
    itemDesc: str | None
    itemObtainApproach: str | None
    isNotObtainable: bool
    isSpChar: bool
    maxPotentialLevel: int
    rarity: str  # "TIER_1" .. "TIER_6"
    profession: str
    subProfessionId: str
    trait: Trait | None
    phases: list[Phase]
    skills: list[SkillRef]
    displayTokenDict: dict[str, bool] | None
    talents: list[Talent] | None
    potentialRanks: list[PotentialRank]
    favorKeyFrames: list[AttributeKeyFrame] | None
    allSkillLvlup: list[SkillLvlup]


# Top-level type: character ID → entry
CharacterTable = dict[str, CharacterTableEntry]
