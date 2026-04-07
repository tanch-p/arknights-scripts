from __future__ import annotations
from .common import Blackboard
from typing import TypedDict, Generic, TypeVar

T = TypeVar("T")


class MaybeField(TypedDict, Generic[T]):
    m_defined: bool
    m_value: T


class EnemySkill(TypedDict):
    prefabKey: str
    priority: int
    cooldown: float
    initCooldown: float
    spCost: int
    blackboard: list[Blackboard]


class SpData(TypedDict):
    spType: str
    maxSp: int
    initSp: int
    increment: float


class EnemyAttributes(TypedDict):
    maxHp: MaybeField[int]
    atk: MaybeField[int]
    def_: MaybeField[int]  # key in JSON is "def"
    magicResistance: MaybeField[float]
    cost: MaybeField[int]
    blockCnt: MaybeField[int]
    moveSpeed: MaybeField[float]
    attackSpeed: MaybeField[float]
    baseAttackTime: MaybeField[float]
    respawnTime: MaybeField[int]
    hpRecoveryPerSec: MaybeField[float]
    spRecoveryPerSec: MaybeField[float]
    maxDeployCount: MaybeField[int]
    massLevel: MaybeField[int]
    baseForceLevel: MaybeField[int]
    tauntLevel: MaybeField[int]
    epDamageResistance: MaybeField[float]
    epResistance: MaybeField[float]
    damageHitratePhysical: MaybeField[float]
    damageHitrateMagical: MaybeField[float]
    epBreakRecoverSpeed: MaybeField[float]
    stunImmune: MaybeField[bool]
    silenceImmune: MaybeField[bool]
    sleepImmune: MaybeField[bool]
    frozenImmune: MaybeField[bool]
    levitateImmune: MaybeField[bool]
    disarmedCombatImmune: MaybeField[bool]
    fearedImmune: MaybeField[bool]
    palsyImmune: MaybeField[bool]
    attractImmune: MaybeField[bool]


class EnemyData(TypedDict):
    name: MaybeField[str]
    description: MaybeField[str]
    prefabKey: MaybeField[str]
    attributes: EnemyAttributes
    applyWay: MaybeField[str]
    motion: MaybeField[str]
    enemyTags: MaybeField[list[str]]
    lifePointReduce: MaybeField[int]
    levelType: MaybeField[str]
    rangeRadius: MaybeField[float]
    numOfExtraDrops: MaybeField[int]
    viewRadius: MaybeField[float]
    notCountInTotal: MaybeField[bool]
    talentBlackboard: list[Blackboard] | None
    skills: list[EnemySkill]
    spData: SpData | None


class EnemyLevel(TypedDict):
    level: int
    enemyData: EnemyData


class EnemyEntry(TypedDict):
    Key: str
    Value: list[EnemyLevel]


class EnemyDatabase(TypedDict):
    enemies: list[EnemyEntry]
