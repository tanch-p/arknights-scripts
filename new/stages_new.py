from __future__ import annotations

import json
from pathlib import Path

from stages import get_trimmed_stage_data


BASE_DIR = Path(__file__).resolve().parent
STAGE_CONFIG_PATH = BASE_DIR / "stage_config.json"
EXTRAINFO_PATH = BASE_DIR / "is_stages_extrainfo.json"
LEVELS_DIR = BASE_DIR / "cn_data/zh_CN/gamedata/levels"
OUTPUT_DIR = BASE_DIR / "ro_stage_data"
LOOKUP_TABLE_PATH = BASE_DIR / "stage_lookup_table.json"

# Temporary compatibility shim: some RO5 replacement levels use DLC-specific
# level ids, while is_stages_extrainfo.json still stores metadata under the
# original base level ids.
LEVEL_ID_COMPATIBILITY_TABLE = {
    "level_rogue5_1-1_dlc1": "level_rogue5_1-1",
    "level_rogue5_1-2_dlc1": "level_rogue5_1-2",
    "level_rogue5_1-3_dlc1": "level_rogue5_1-3",
    "level_rogue5_1-4_dlc1": "level_rogue5_1-4",
    "level_rogue5_2-1_dlc1": "level_rogue5_2-1",
    "level_rogue5_2-2_dlc1": "level_rogue5_2-2",
    "level_rogue5_2-3_dlc1": "level_rogue5_2-3",
    "level_rogue5_2-4_dlc1": "level_rogue5_2-4",
    "level_rogue5_3-1_dlc1": "level_rogue5_3-1",
    "level_rogue5_3-2_dlc1": "level_rogue5_3-2",
    "level_rogue5_3-3_dlc1": "level_rogue5_3-3",
    "level_rogue5_3-4_dlc1": "level_rogue5_3-4",
    "level_rogue5_3-5_dlc1": "level_rogue5_3-5",
    "level_rogue5_4-1_dlc2": "level_rogue5_4-1",
    "level_rogue5_4-2_dlc2": "level_rogue5_4-2",
    "level_rogue5_4-3_dlc2": "level_rogue5_4-3",
    "level_rogue5_4-4_dlc2": "level_rogue5_4-4",
    "level_rogue5_4-5_dlc2": "level_rogue5_4-5",
    "level_rogue5_4-6_dlc2": "level_rogue5_4-6",
    "level_rogue5_5-1_dlc2": "level_rogue5_5-1",
    "level_rogue5_5-2_dlc2": "level_rogue5_5-2",
    "level_rogue5_5-3_dlc2": "level_rogue5_5-3",
    "level_rogue5_5-4_dlc2": "level_rogue5_5-4",
    "level_rogue5_5-5_dlc2": "level_rogue5_5-5",
    "level_rogue5_5-6_dlc2": "level_rogue5_5-6",
    "level_rogue5_6-1_dlc2": "level_rogue5_6-1",
    "level_rogue5_6-2_dlc2": "level_rogue5_6-2",
    "level_rogue5_7-1_dlc2": "level_rogue5_7-1",
    "level_rogue5_7-2_dlc2": "level_rogue5_7-2",
}


def _get_topic(stage_group_id: str) -> str:
    stage_group_id = stage_group_id.lower()
    for topic_number in range(6, 0, -1):
        topic = f"ro{topic_number}"
        if topic in stage_group_id:
            return topic
    raise ValueError(f"Unsupported stage topic for id: {stage_group_id}")


def _normalize_level_ref(level_ref: str) -> str:
    return level_ref.lower()


def _get_level_id(level_ref: str) -> str:
    return Path(_normalize_level_ref(level_ref)).name


def _get_compatible_level_id(level_ref: str) -> str:
    level_id = _get_level_id(level_ref)
    return LEVEL_ID_COMPATIBILITY_TABLE.get(level_id, level_id)


def _get_level_config_path(level_ref: str) -> Path:
    return LEVELS_DIR / f"{_normalize_level_ref(level_ref)}.json"


def _normalize_description(text: str | None) -> str | None:
    return text.replace("\\n", "\n") if text is not None else None


def _normalize_stage_name(text: str | None) -> str | None:
    return text.replace(" ", "_") if text is not None else None


def _build_meta_info(
    stage_group: dict,
    stage_item: dict,
    level_id: str,
) -> dict:
    return {
        "suffix": "",
        "id": stage_item["id"],
        "levelId": level_id,
        "code": stage_group["code"],
        "name_zh": stage_group["name"].get("zh"),
        "name_ja": _normalize_stage_name(stage_group["name"].get("ja")),
        "name_en": _normalize_stage_name(stage_group["name"].get("en")),
        "description_zh": _normalize_description(stage_item["description"].get("zh")),
        "description_ja": _normalize_description(stage_item["description"].get("ja")),
        "description_en": _normalize_description(stage_item["description"].get("en")),
    }


def _build_trimmed_stage_config(
    stage_group: dict,
    stage_item: dict,
    extrainfo: dict,
) -> dict:
    topic = _get_topic(stage_group["id"])
    level_ref = (
        stage_item["levelReplaceIds"][-1]
        if stage_item["levelReplaceIds"]
        else stage_item["levelId"]
    )
    level_id = _get_compatible_level_id(level_ref)
    level_config_path = _get_level_config_path(level_ref)

    with level_config_path.open(encoding="utf-8") as level_config_file:
        stage_data = json.load(level_config_file)

    meta_info = _build_meta_info(stage_group, stage_item, level_id)
    print(meta_info["levelId"])
    return get_trimmed_stage_data(stage_data, meta_info, extrainfo, topic)


def _load_stage_groups(stage_config_path: Path) -> list[dict]:
    with stage_config_path.open(encoding="utf-8") as stage_config_file:
        return json.load(stage_config_file)


def expand_stage_configs(
    stage_config_path: Path = STAGE_CONFIG_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    stage_groups = _load_stage_groups(stage_config_path)
    with EXTRAINFO_PATH.open(encoding="utf-8") as extrainfo_file:
        extrainfo = json.load(extrainfo_file)

    output_dir.mkdir(exist_ok=True)

    for stage_group in stage_groups:
        topic = _get_topic(stage_group["id"])

        for stage_item in stage_group["stages"]:
            stage_item["topic"] = topic
            stage_item["config"] = _build_trimmed_stage_config(
                stage_group, stage_item, extrainfo
            )

        output_path = output_dir / f"{stage_group['id']}.json"
        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(stage_group, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")

    return stage_groups


def create_stage_lookup_table(
    stage_config_path: Path = STAGE_CONFIG_PATH,
    output_path: Path = LOOKUP_TABLE_PATH,
) -> dict[str, str]:
    stage_groups = _load_stage_groups(stage_config_path)
    lookup_table: dict[str, str] = {}

    for stage_group in stage_groups:
        for localized_name in stage_group["name"].values():
            if localized_name:
                name = stage_group["code"] + "_" + localized_name.replace(" ", "_")
                lookup_table[name] = stage_group["id"]

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(lookup_table, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return lookup_table


if __name__ == "__main__":
    expand_stage_configs()
    create_stage_lookup_table()
