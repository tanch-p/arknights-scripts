from typing import TypedDict


class DefinedString(TypedDict):
    m_defined: bool
    m_value: str | None


class DefinedInt(TypedDict):
    m_defined: bool
    m_value: int


class DefinedFloat(TypedDict):
    m_defined: bool
    m_value: float


class DefinedBool(TypedDict):
    m_defined: bool
    m_value: bool


class DefinedStringList(TypedDict):
    m_defined: bool
    m_value: list[str] | None


Attributes = TypedDict(
    "Attributes",
    {
        "maxHp": DefinedInt,
        "atk": DefinedInt,
        "def": DefinedInt,
        "magicResistance": DefinedFloat,
        "cost": DefinedInt,
        "blockCnt": DefinedInt,
        "moveSpeed": DefinedFloat,
        "attackSpeed": DefinedFloat,
        "baseAttackTime": DefinedFloat,
        "respawnTime": DefinedInt,
        "hpRecoveryPerSec": DefinedFloat,
        "spRecoveryPerSec": DefinedFloat,
        "maxDeployCount": DefinedInt,
        "massLevel": DefinedInt,
        "baseForceLevel": DefinedInt,
        "tauntLevel": DefinedInt,
        "epDamageResistance": DefinedFloat,
        "epResistance": DefinedFloat,
        "damageHitratePhysical": DefinedFloat,
        "damageHitrateMagical": DefinedFloat,
        "epBreakRecoverSpeed": DefinedFloat,
        "stunImmune": DefinedBool,
        "silenceImmune": DefinedBool,
        "sleepImmune": DefinedBool,
        "frozenImmune": DefinedBool,
        "levitateImmune": DefinedBool,
        "disarmedCombatImmune": DefinedBool,
        "fearedImmune": DefinedBool,
        "palsyImmune": DefinedBool,
        "attractImmune": DefinedBool,
        "teleportImmune": DefinedBool,
        "groundBoundImmune": DefinedBool,
    },
)


class TalentBlackboard(TypedDict):
    key: str
    value: float
    valueStr: str | None


class SkillBlackboard(TypedDict):
    key: str | None
    value: float
    valueStr: str | None


class EnemySkill(TypedDict):
    prefabKey: str
    priority: int
    cooldown: float
    initCooldown: float
    spCost: int
    blackboard: list[SkillBlackboard] | None


class SpData(TypedDict):
    spType: str
    maxSp: int
    initSp: int
    increment: float


class EnemyData(TypedDict):
    name: DefinedString
    description: DefinedString
    prefabKey: DefinedString

    attributes: Attributes

    applyWay: DefinedString
    motion: DefinedString
    enemyTags: DefinedStringList

    lifePointReduce: DefinedInt
    levelType: DefinedString
    rangeRadius: DefinedFloat
    numOfExtraDrops: DefinedInt
    viewRadius: DefinedFloat
    notCountInTotal: DefinedBool

    talentBlackboard: list[TalentBlackboard] | None

    skills: list[EnemySkill] | None
    spData: SpData | None


class EnemyLevel(TypedDict):
    level: int
    enemyData: EnemyData


class EnemyEntry(TypedDict):
    Key: str
    Value: list[EnemyLevel]


class EnemyFile(TypedDict):
    enemies: list[EnemyEntry]


EnemyLookup = dict[str, EnemyEntry]
