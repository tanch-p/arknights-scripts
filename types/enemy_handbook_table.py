from __future__ import annotations

from typing import TypedDict


class StatRange(TypedDict):
    min: float
    max: float  # -1.0 means no upper bound


class LevelInfo(TypedDict):
    classLevel: str  # "SS" | "S+" | "S" | ...
    attack: StatRange
    def_: StatRange  # key in JSON is "def"
    magicRes: StatRange
    maxHP: StatRange
    moveSpeed: StatRange
    attackSpeed: StatRange
    enemyDamageRes: StatRange
    enemyRes: StatRange


class EnemyAbility(TypedDict):
    text: str
    textFormat: str  # "SILENCE" | ...


class EnemyHandbookEntry(TypedDict):
    enemyId: str
    enemyIndex: str
    enemyTags: list[str] | None
    sortId: int
    name: str
    enemyLevel: str  # "NORMAL" | "ELITE" | "BOSS"
    description: str
    attackType: str | None
    ability: str | None
    isInvalidKilled: bool
    overrideKillCntInfos: dict[str, int]  # stage ID → kill count override
    hideInHandbook: bool
    hideInStage: bool
    abilityList: list[EnemyAbility]
    linkEnemies: list[str]
    damageType: list[str]  # "PHYSIC" | "MAGIC" | "NO_DAMAGE"
    invisibleDetail: bool


class RaceEntry(TypedDict):
    id: str
    raceName: str
    sortId: int


class EnemyHandbookTable(TypedDict):
    levelInfoList: list[LevelInfo]
    enemyData: dict[str, EnemyHandbookEntry]
    raceData: dict[str, RaceEntry]
