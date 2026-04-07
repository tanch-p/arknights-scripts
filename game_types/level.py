from __future__ import annotations

from typing import NotRequired, TypedDict
from .common import Blackboard


class LevelOptions(TypedDict):
    characterLimit: int
    maxLifePoint: int
    initialCost: int
    maxCost: int
    costIncreaseTime: float
    moveMultiplier: float
    steeringEnabled: bool
    isTrainingLevel: bool
    isHardTrainingLevel: bool
    isPredefinedCardsSelectable: bool
    displayRestTime: bool
    maxPlayTime: float
    functionDisableMask: str
    configBlackBoard: list[Blackboard] | None


class Vec2(TypedDict):
    x: float
    y: float


class Vec3(TypedDict):
    x: float
    y: float
    z: float


class TileEffect(TypedDict):
    key: str
    offset: Vec3
    direction: str


class Tile(TypedDict):
    tileKey: str
    heightType: str  # "LOWLAND" | "HIGHLAND"
    buildableType: str  # "NONE" | "MELEE" | "RANGED" | "ALL"
    passableMask: str  # "ALL" | "FLY_ONLY" | "NONE"
    playerSideMask: str  # "ALL" | "NONE"
    blackboard: list[Blackboard] | None
    effects: list[TileEffect] | None


class MapData(TypedDict):
    map: list[list[int]]  # 2D grid of tile indices
    tiles: list[Tile]


class Position(TypedDict):
    row: int
    col: int


class Checkpoint(TypedDict):
    type: str  # "MOVE" | "WAIT_CURRENT_FRAGMENT_TIME" | ...
    time: float
    position: Position
    reachOffset: Vec2
    randomizeReachOffset: bool
    reachDistance: float


class Route(TypedDict):
    motionMode: str  # "WALK" | "FLY" | "E_NUM"
    startPosition: Position
    endPosition: Position
    spawnRandomRange: Vec2
    spawnOffset: Vec2
    checkpoints: list[Checkpoint] | None
    allowDiagonalMove: bool
    visitEveryTileCenter: bool
    visitEveryNodeCenter: bool
    visitEveryCheckPoint: bool


# WaveActionType: "SPAWN" | "ACTIVATE_PREDEFINED" | "TRIGGER_PREDEFINED" | "WITHDRAW_PREDEFINED"
#   | "DISPLAY_ENEMY_INFO" | "PREVIEW_CURSOR" | "STORY" | "DIALOG" | "PLAY_BGM"
#   | "PLAY_OPERA" | "BATTLE_EVENTS" | "EMPTY" | int (legacy 0–8)
WaveActionType = str | int

# WaveRandomType: "ALWAYS" | "" | int (0 = fixed, 1/2 = random group variants)
WaveRandomType = str | int

# WaveRefreshType: "ALWAYS" | "NEVER" | "PER_DAY" | "PER_SEASON" | "PER_SETTLE_DAY" | ""
#   NEVER/PER_* values are sandbox-only (obt/sandbox/sandbox_1/)
WaveRefreshType = str


class WaveAction(TypedDict):
    actionType: WaveActionType
    managedByScheduler: bool
    key: str  # enemy ID or predefined alias; empty string = no-op placeholder
    count: int
    preDelay: float
    interval: float
    routeIndex: int
    blockFragment: bool
    autoPreviewRoute: bool
    autoDisplayEnemyInfo: bool
    isUnharmfulAndAlwaysCountAsKilled: bool
    hiddenGroup: str | None
    randomSpawnGroupKey: str | None
    randomSpawnGroupPackKey: str | None
    randomType: WaveRandomType
    refreshType: WaveRefreshType
    weight: int
    dontBlockWave: bool
    forceBlockWaveInBranch: bool


class WaveFragment(TypedDict):
    preDelay: float
    actions: list[WaveAction]


class Wave(TypedDict):
    preDelay: float
    postDelay: float
    maxTimeWaitingForNextWave: float
    fragments: list[WaveFragment]
    advancedWaveTag: str | None


class BranchPhase(TypedDict):
    preDelay: float
    actions: list[WaveAction]


class Branch(TypedDict):
    phases: list[BranchPhase]


# RuneKey — known values with their blackboard parameters:
#
#   Global stage modifiers:
#     global_lifepoint              — value
#     global_cost_recovery          — scale
#     global_cost_recovery_mul      — scale
#     global_initial_cost_add       — value
#     global_placable_char_num_add  — value
#     global_squad_num_limit        — value
#     global_token_cnt_add          — char, value
#     global_forbid_location        — location
#     global_enemy_taunt_level_pow  — value
#
#   Enemy attribute modifiers:
#     enemy_attribute_mul           — atk, def, max_hp, attack_speed, move_speed, magic_resistance, mass_level, enemy, enemy_exclude
#     enemy_attribute_add           — atk, def, max_hp, attack_speed, magic_resistance, move_speed, enemy
#     enemy_weight_add              — enemy, value
#     enemy_attackradius_mul        — enemy, scale
#     enemy_abnormal_immune         — frozen
#
#   Enemy skill modifiers:
#     enemy_skill_blackb_add        — enemy, skill, force, boom_value_ally, ep_damage_ratio, blockee_value
#     enemy_skill_blackb_mul        — enemy, skill, + skill-specific keys
#     enemy_skill_cd_mul            — enemy, skill, scale (+ named skill keys: C4, P2S2, Rockfall, ...)
#     enemy_skill_init_cd_mul       — enemy, skill, scale
#     enemy_skill_radius_mul        — enemy, skill, scale
#     enemy_skill_sp_cost_add       — enemy, skill, value
#
#   Enemy talent modifiers:
#     enemy_talent_blackb_add       — enemy, key, + talent-specific dotted keys
#     enemy_talent_blackb_mul       — enemy, + talent-specific dotted keys
#     enemy_talent_blackb_max       — enemy, + talent-specific dotted keys
#
#   Enemy dynamic / buff:
#     enemy_dynamic_ability_new     — enemy, key
#     ebuff_attribute               — enemy, atk, def, max_hp, attack_speed, move_speed
#     ebuff_attack_radius           — enemy, range_scale
#     ebuff_talent_blackb_add       — talent-specific dotted keys
#     ebuff_talent_blackb_mul       — enemy, DeadSpawn.cnt
#     cooperate_enemy_side_shared   — enemy
#
#   Character attribute modifiers:
#     char_attribute_add            — char, atk, max_hp, attack_speed, hp_recovery_per_sec
#     char_attribute_mul            — char, char_id, atk, def, max_hp, magic_resistance, attack_speed
#     char_cost_add                 — char_id, value
#     char_cost_mul                 — char, char_id, scale
#     char_blockcnt_add             — value
#     char_respawntime_add          — char, value
#     char_respawntime_mul          — scale
#
#   Character skill / talent modifiers:
#     char_skill_blackb_add         — character, + skill-specific dotted keys
#     char_skill_blackb_mul         — char, + skill-specific dotted keys
#     char_skill_cd_mul             — char, character, scale
#     char_talent_blackb_assign     — char, talent_key, + talent-specific dotted keys
#     char_dynamic_ability_new      — char, key, cost, interval, target, at_root
#     char_exclude                  — char, include_predefined
#
#   Character buff objects:
#     cbuff_attribute               — max_hp
#     cbuff_char_cost               — scale
#     cbuff_cost_recovery           — scale
#     cbuff_max_cost                — max_cost, max_cost_ceil
#     cbuff_excluded                — char
#     cbuff_token_initial_cnt       — char, value
#
#   Map / tile modifiers:
#     map_tile_blackb_add           — location, tile, + tile-specific keys
#     map_tile_blackb_assign        — location, tile, + tile-specific keys
#     map_tile_blackb_mul           — tile, + tile-specific dotted keys
#
#   Environment / global-buff objects:
#     env_gbuff_new                 — key, alias, + various effect keys
#     env_gbuff_new_with_verify     — key, + condition and effect keys
#     env_system_new                — key, + large set of system-config keys
#     gbuff_lifepoint               — value
#     gbuff_placable_char_num       — value
#
#   Stage control:
#     level_hidden_group_enable     — key (group alias string)
#     level_hidden_group_disable    — key
#     level_enemy_replace           — key (source enemy id), value (replacement enemy id)
#     level_predefines_enable       — key (predefined alias to activate)
#     assign_global_blackboard      — key, value / value (str), channel_blackboard
RuneKey = str

# DifficultyMask: "ALL" | "NORMAL" | "FOUR_STAR" | "NONE" | int bitmask (1, 2, 3, 7)
DifficultyMask = str | int

# BuildableMask: "ALL" | "NONE" | "MELEE" | "RANGED" | int bitmask (1, 2, 3)
BuildableMask = str | int


class Rune(TypedDict):
    difficultyMask: DifficultyMask
    key: RuneKey
    professionMask: int
    buildableMask: BuildableMask
    blackboard: list[Blackboard]


# GlobalBuff prefabKey known values:
#   act1vautochess_time_out_global_buff, act27sisde_enemy_global_buff,
#   character_in_magiccircuit_env, cooperate_enemy_after_attack_harder,
#   cooperate_enemy_catch_up, cooperate_fortress_global_buff,
#   funlive_char_ban_battle_logic, funlive_enemy_ban_battle_logic,
#   funlive_rare_dangerous_event_data, funlive_unit_beginning_dangerous_effect_logic,
#   funlive_unit_beginning_rare_effect_logic, funlive_unit_npc_annoying_effect_logic,
#   game_city_mode_feature, kill_to_add_cost, mainline12_sightManager,
#   mainline14_enemy_sign_effect, night_map_default, night_map_default_new,
#   periodic_damage, rogue_4_lock_all_entities_when_born, rogue_4_parasitic_buff,
#   rogue_5_deify_common_buff, rogue_5_enemy_fall_down_log,
#   rogue_5_heaven_inherit_unit_status, sandbox_inherit_status, strife_mode_feature
class GlobalBuff(TypedDict):
    prefabKey: str
    blackboard: list[Blackboard] | None
    overrideCameraEffect: str | None
    passProfessionMaskFlag: bool
    professionMask: str  # "NONE" | "" | int bitmask
    useExtraData: NotRequired[bool]
    playerSideMask: NotRequired[str]  # "ALL" | "NONE"; absent on most entries


class EnemyAttributes(TypedDict):
    maxHp: int
    atk: int
    def_: int  # key in JSON is "def"
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


# Inline enemy definition (used in the `enemies` array, distinct from enemyDbRefs)
class EnemyInline(TypedDict):
    name: str | None
    description: str | None
    key: str
    attributes: EnemyAttributes
    applyWay: str
    motion: str
    enemyTags: list[str] | None
    notCountInTotal: bool
    alias: str | None
    lifePointReduce: int
    rangeRadius: float
    numOfExtraDrops: int
    viewRadius: float
    levelType: str
    talentBlackboard: list[Blackboard]
    skills: list[object]
    spData: object | None


# Overwritten enemy data uses nullable wrappers for each field
class MaybeValue(TypedDict):
    m_defined: bool
    m_value: object  # type varies per field


class EnemyOverwrittenData(TypedDict):
    name: MaybeValue
    description: MaybeValue
    prefabKey: MaybeValue
    attributes: dict[str, MaybeValue]
    applyWay: MaybeValue
    motion: MaybeValue
    enemyTags: MaybeValue
    lifePointReduce: MaybeValue
    levelType: MaybeValue
    rangeRadius: MaybeValue
    numOfExtraDrops: MaybeValue
    viewRadius: MaybeValue
    notCountInTotal: MaybeValue
    talentBlackboard: list[Blackboard] | None
    skills: object | None
    spData: object | None


class EnemyDbRef(TypedDict):
    useDb: bool
    id: str
    level: int
    overwrittenData: EnemyOverwrittenData | None


class CharacterInst(TypedDict):
    characterKey: str
    level: int
    phase: str
    favorPoint: int
    potentialRank: int


class PredefineToken(TypedDict):
    position: Position
    direction: str  # "UP" | "DOWN" | "LEFT" | "RIGHT"
    hidden: bool
    alias: str
    uniEquipIds: list[str] | None
    showSpIllust: bool
    masterInfos: object | None
    inst: CharacterInst
    skillIndex: int
    mainSkillLvl: int
    skinId: str | None
    tmplId: str | None
    overrideSkillBlackboard: list[Blackboard] | None


class Predefines(TypedDict):
    characterInsts: list[object]
    tokenInsts: list[PredefineToken]
    characterCards: list[object]
    tokenCards: list[object]


class LevelData(TypedDict):
    options: LevelOptions
    levelId: str | None
    mapId: str | None
    bgmEvent: str | None
    environmentSe: str | None
    mapData: MapData
    tilesDisallowToLocate: list[object]
    runes: list[Rune]
    optionalRunes: NotRequired[list[Rune] | None]
    globalBuffs: list[GlobalBuff]
    routes: list[Route]
    extraRoutes: NotRequired[list[Route]]
    enemies: list[EnemyInline]
    enemyDbRefs: list[EnemyDbRef]
    waves: list[Wave]
    branches: dict[str, Branch] | None
    predefines: Predefines
    hardPredefines: NotRequired[Predefines]
    excludeCharIdList: list[str] | None
    randomSeed: int
    operaConfig: NotRequired[str | None]
    cameraPlugin: NotRequired[str | None]
    runtimeData: NotRequired[None]  # present in activity files, always null
