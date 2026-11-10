import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
CN_DATA_DIR = BASE_DIR / "cn_data/zh_CN/gamedata"
OBT_DIR = CN_DATA_DIR / "levels/obt"
ENEMY_DATABASE_PATH = CN_DATA_DIR / "levels/enemydata/enemy_database.json"
CN_HANDBOOK_PATH = CN_DATA_DIR / "excel/enemy_handbook_table.json"
EN_DATABASE_PATH = (
    BASE_DIR / "global_data/en/gamedata/levels/enemydata/enemy_database.json"
)
JP_DATABASE_PATH = (
    BASE_DIR / "global_data/jp/gamedata/levels/enemydata/enemy_database.json"
)
OUTPUT_PATH = BASE_DIR / "temp.json"

EXCLUDED_OBT_FOLDERS = {"sandbox", "legion"}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def get_obt_enemy_keys() -> set[str]:
    """Return database enemy IDs referenced by included OBT levels."""
    enemy_keys: set[str] = set()

    for level_path in OBT_DIR.rglob("*.json"):
        relative_parts = level_path.relative_to(OBT_DIR).parts
        if any(part in EXCLUDED_OBT_FOLDERS for part in relative_parts[:-1]):
            continue

        level_data = load_json(level_path)
        for reference in level_data.get("enemyDbRefs", []):
            if isinstance(reference, dict) and isinstance(reference.get("id"), str):
                enemy_keys.add(reference["id"])

    return enemy_keys


def get_status_immune_list(stat: dict[str, Any]) -> list[str]:
    attributes = stat["enemyData"]["attributes"]
    immunity_fields = {
        "stunImmune": "stun",
        "silenceImmune": "silence",
        "sleepImmune": "sleep",
        "frozenImmune": "freeze",
        "levitateImmune": "levitate",
        "disarmedCombatImmune": "tremble",
        "fearedImmune": "fear",
        "palsyImmune": "palsy",
        "attractImmune": "attract",
        "teleportImmune": "teleport",
        "groundBoundImmune": "groundbind",
    }
    return [
        immunity_name
        for field, immunity_name in immunity_fields.items()
        if attributes[field]["m_value"]
    ]


def get_value(
    stat: dict[str, Any],
    base_stat: dict[str, Any],
    field: str,
    *,
    attribute: bool = True,
) -> Any:
    stat_data = stat["enemyData"]
    base_data = base_stat["enemyData"]
    if attribute:
        stat_data = stat_data["attributes"]
        base_data = base_data["attributes"]

    value = stat_data[field]
    return value["m_value"] if value["m_defined"] else base_data[field]["m_value"]


def is_flying_enemy(enemy_info: dict[str, Any], enemy_tags: list[str]) -> bool:
    ability_text = " ".join(
        ability.get("text", "") for ability in enemy_info.get("abilityList", [])
    )
    description = enemy_info.get("description") or ""
    return (
        "drone" in enemy_tags or "飞行单位" in ability_text or "飞行单位" in description
    )


def get_localized_name(
    key: str, localized_database: dict[str, list[dict[str, Any]]]
) -> str:
    entry = localized_database.get(key)
    if not entry:
        return ""
    return entry[0]["enemyData"]["name"]["m_value"] or ""


def get_blackboard_value(item: dict[str, Any]) -> Any:
    return item["valueStr"] if item.get("valueStr") is not None else item.get("value")


def get_traits(stat: dict[str, Any]) -> list[dict[str, Any]]:
    enemy_data = stat["enemyData"]
    traits = [
        {
            "key": talent["key"],
            "value": get_blackboard_value(talent),
        }
        for talent in enemy_data.get("talentBlackboard") or []
    ]

    for skill in enemy_data.get("skills") or []:
        trait = {
            "key": skill["prefabKey"],
            "priority": skill["priority"],
            "cooldown": skill["cooldown"],
            "initCooldown": skill["initCooldown"],
            "spCost": skill["spCost"],
        }
        for blackboard_item in skill.get("blackboard") or []:
            field = blackboard_item["key"]
            if field in trait:
                field = f"blackboard.{field}"
            trait[field] = get_blackboard_value(blackboard_item)
        traits.append(trait)

    return traits


def get_enemy_data(
    entry: dict[str, Any],
    enemy_info: dict[str, Any],
    en_database: dict[str, list[dict[str, Any]]],
    jp_database: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    key = entry["Key"]
    enemy_stats = entry["Value"]
    base_stat = enemy_stats[0]
    base_data = base_stat["enemyData"]

    attack_type = base_data["applyWay"]["m_value"].lower()
    attack_attribute: str | None = "phys"
    damage_type = enemy_info.get("damageType") or ""
    if "MAGIC" in damage_type:
        attack_attribute = "arts"
    elif "NO_DAMAGE" in damage_type:
        attack_attribute = None
        attack_type = "no_attack"

    normal_attack = {
        "atk_type": [attack_type, attack_attribute],
        "hits": 1,
    }

    enemy_tags = list(base_data["enemyTags"]["m_value"] or [])
    if is_flying_enemy(enemy_info, enemy_tags) and "flying" not in enemy_tags:
        enemy_tags.append("flying")
    enemy_tags.append(
        base_data["levelType"]["m_value"]
        if base_data["levelType"]["m_defined"]
        else "NORMAL"
    )
    enemy_tags.insert(0, attack_type)

    status_immunities = get_status_immune_list(base_stat)
    stats = []
    for stat in enemy_stats:
        stats.append(
            {
                "hp": get_value(stat, base_stat, "maxHp"),
                "atk": get_value(stat, base_stat, "atk"),
                "def": get_value(stat, base_stat, "def"),
                "res": get_value(stat, base_stat, "magicResistance"),
                "aspd": get_value(stat, base_stat, "baseAttackTime"),
                "range": get_value(stat, base_stat, "rangeRadius", attribute=False),
                "weight": get_value(stat, base_stat, "massLevel"),
                "lifepoint": (
                    base_data["lifePointReduce"]["m_value"]
                    if base_data["lifePointReduce"]["m_defined"]
                    else 1
                ),
                "ms": get_value(stat, base_stat, "moveSpeed"),
                "epDamageResistance": get_value(stat, base_stat, "epDamageResistance"),
                "epResistance": get_value(stat, base_stat, "epResistance"),
                "traits": get_traits(stat),
                "special": [],
            }
        )

    return {
        "id": enemy_info["enemyIndex"],
        "key": key,
        "sortId": enemy_info.get("sortId"),
        "name_zh": base_data["name"]["m_value"],
        "name_ja": get_localized_name(key, jp_database),
        "name_en": get_localized_name(key, en_database),
        "stats": stats,
        "forms": [
            {
                "title": None,
                "normal_attack": normal_attack,
                "status_immune": status_immunities,
            }
        ],
        "type": enemy_tags,
        "notCountInTotal": (
            base_data["notCountInTotal"]["m_value"]
            if base_data["notCountInTotal"]["m_defined"]
            else False
        ),
    }


def main() -> None:
    enemy_database = load_json(ENEMY_DATABASE_PATH)
    handbook = load_json(CN_HANDBOOK_PATH)["enemyData"]
    en_database = load_json(EN_DATABASE_PATH)
    jp_database = load_json(JP_DATABASE_PATH)
    obt_enemy_keys = get_obt_enemy_keys()

    output = {
        entry["Key"]: get_enemy_data(
            entry,
            handbook[entry["Key"]],
            en_database,
            jp_database,
        )
        for entry in enemy_database["enemies"]
        if entry["Key"] in obt_enemy_keys and entry["Key"] in handbook
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    print(f"Wrote {len(output)} enemies to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
