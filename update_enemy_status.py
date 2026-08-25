"""Add newly introduced CN enemy status immunities to the local database."""

import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CN_ENEMY_DATABASE_PATH = (
    BASE_DIR / "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
ENEMY_DATABASE_PATH = BASE_DIR / "enemy_database.json"

# Map the raw enemy-attribute keys to this project's status_immune labels.
STATUS_IMMUNITIES = {
    "teleportImmune": "teleport",
    "groundBoundImmune": "groundbind",
}


def get_new_status_immunities(enemy: dict) -> list[str]:
    """Return new immunity labels enabled on an enemy's base definition."""
    attributes = enemy["Value"][0]["enemyData"]["attributes"]
    return [
        status
        for attribute, status in STATUS_IMMUNITIES.items()
        if attributes.get(attribute, {}).get("m_value") is True
    ]


def _find_object_end(text: str, object_start: int) -> int:
    """Return the offset immediately after a JSON object starting at object_start."""
    depth = 0
    in_string = False
    escaped = False

    for index in range(object_start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return index + 1

    raise ValueError("Unterminated JSON object")


def _replace_status_lists(
    database_text: str, enemy_key: str, status_lists: list[list[str]]
) -> str:
    """Replace an enemy's status lists without reformatting the whole JSON file."""
    key_marker = f'"{enemy_key}": {{'
    object_start = database_text.index(key_marker)
    object_end = _find_object_end(database_text, object_start + len(key_marker) - 1)
    enemy_text = database_text[object_start:object_end]
    status_list_pattern = re.compile(r'("status_immune"\s*:\s*)\[[^\[\]]*\]')
    replacement_index = 0

    def replace(match: re.Match) -> str:
        nonlocal replacement_index
        if replacement_index >= len(status_lists):
            raise ValueError(f"Too many status_immune lists for {enemy_key}")
        status_list = json.dumps(status_lists[replacement_index], ensure_ascii=False)
        replacement_index += 1
        return match.group(1) + status_list

    updated_enemy_text = status_list_pattern.sub(replace, enemy_text)
    if replacement_index != len(status_lists):
        raise ValueError(f"Missing status_immune list for {enemy_key}")
    return (
        database_text[:object_start] + updated_enemy_text + database_text[object_end:]
    )


def update_enemy_status_immunities() -> list[tuple[str, list[str]]]:
    """Append teleport/groundbind immunities and return the changed enemies.

    Existing status immunities are retained. The function only uses the base
    enemy definition (Value[0]), matching the status handling in enemy.py.
    """
    with CN_ENEMY_DATABASE_PATH.open(encoding="utf-8") as source_file:
        cn_enemy_database = json.load(source_file)
    with ENEMY_DATABASE_PATH.open(encoding="utf-8") as database_file:
        local_database = json.load(database_file)

    source_enemies = {enemy["Key"]: enemy for enemy in cn_enemy_database["enemies"]}
    changes: dict[str, tuple[list[str], list[list[str]]]] = {}

    for enemy_key, local_enemy in local_database.items():
        source_enemy = source_enemies.get(enemy_key)
        if source_enemy is None:
            continue

        new_immunities = get_new_status_immunities(source_enemy)
        if not new_immunities:
            continue

        updated_status_lists = []
        changed = False
        for form in local_enemy.get("forms", []):
            status_immune = form.get("status_immune", [])
            updated_status_immune = status_immune + [
                status for status in new_immunities if status not in status_immune
            ]
            updated_status_lists.append(updated_status_immune)
            changed |= updated_status_immune != status_immune

        if changed:
            changes[enemy_key] = (new_immunities, updated_status_lists)

    if not changes:
        return []

    database_text = ENEMY_DATABASE_PATH.read_text(encoding="utf-8")
    for enemy_key, (_, status_lists) in changes.items():
        database_text = _replace_status_lists(database_text, enemy_key, status_lists)
    ENEMY_DATABASE_PATH.write_text(database_text, encoding="utf-8")

    return [
        (enemy_key, new_immunities)
        for enemy_key, (new_immunities, _) in changes.items()
    ]


def main() -> None:
    changes = update_enemy_status_immunities()
    if changes:
        for enemy_key, immunities in changes:
            print(f"{enemy_key}: added {', '.join(immunities)}")
    else:
        print("No status immunities needed updating.")


if __name__ == "__main__":
    main()
