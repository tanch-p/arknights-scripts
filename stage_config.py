from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from runes import generate_desc, get_runes
from tiles import get_special_tiles
from waves_new import get_wave_spawns_data


ROGUELIKE_TOPIC_TABLE_PATH = Path(
    "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
EN_ROGUELIKE_TOPIC_TABLE_PATH = Path(
    "global_data/en/gamedata/excel/roguelike_topic_table.json"
)
JP_ROGUELIKE_TOPIC_TABLE_PATH = Path(
    "global_data/jp/gamedata/excel/roguelike_topic_table.json"
)
OUTPUT_PATH = Path("stage_config.json")
CUSTOM_STAGE_OUTPUT_DIR = Path("custom_data/stages")
IS_STAGE_EXTRAINFO_PATH = Path("is_stages_extrainfo.json")
CUSTOM_STAGE_EXTRAINFO_FILENAME = "extrainfo.json"
CUSTOM_STAGE_NEW_STAGE_FILENAME = "new_stages.json"
RO_STAGE_DATA_DIR = Path("ro_stage_data")
STAGE_KEYS_TO_REMOVE = {
    "loadingPicId",
    "capsulePool",
    "capsuleProb",
    "specialNodeId",
    "redCapsulePool",
    "redCapsuleProb",
    "vutresProb",
}
EXTRAINFO_STAGE_KEYS = ("id", "levelId", "code", "name", "eliteDesc")


def _strip_stage_keys(stage_data: dict) -> dict:
    return {
        key: value
        for key, value in stage_data.items()
        if key not in STAGE_KEYS_TO_REMOVE
    }


def _get_roguelike_topic_id(topic: str) -> str:
    topic_map = {f"ro{i}": f"rogue_{i}" for i in range(1, 7)}
    try:
        return topic_map[topic]
    except KeyError as exc:
        raise ValueError("topic must be one of: ro1, ro2, ro3, ro4, ro5, 'ro6") from exc


def _get_localized_text(
    zh_value: str | None,
    jp_value: str | None,
    en_value: str | None,
) -> dict[str, str | None]:
    return {"zh": zh_value, "ja": jp_value, "en": en_value}


def _get_level_id_basename(level_id: str) -> str:
    return level_id.split("/")[-1]


def _get_custom_stage_extrainfo_path(topic: str) -> Path:
    return CUSTOM_STAGE_OUTPUT_DIR / topic / CUSTOM_STAGE_EXTRAINFO_FILENAME


def _get_roguelike_level_data_path(topic: str, level_id: str) -> Path:
    level_data_dir = Path("cn_data/zh_CN/gamedata/levels/obt/roguelike") / topic
    if "dlc1" in level_id:
        return level_data_dir / "dlc1" / f"{level_id}.json"
    if "dlc2" in level_id:
        return level_data_dir / "dlc2" / f"{level_id}.json"
    return level_data_dir / f"{level_id}.json"


def _add_localized_stage_texts(
    zh_stage_data: dict,
    en_stage_data: dict | None,
    jp_stage_data: dict | None,
) -> dict:
    localized_stage_data = dict(zh_stage_data)
    for text_key in ("name", "description", "eliteDesc"):
        localized_stage_data[text_key] = _get_localized_text(
            zh_stage_data.get(text_key),
            jp_stage_data.get(text_key) if jp_stage_data else None,
            en_stage_data.get(text_key) if en_stage_data else None,
        )

    return localized_stage_data


def _add_stage_field(stage_data: dict, topic_id: str) -> dict:
    annotated_stage = dict(stage_data)
    stage_id = annotated_stage["id"].lower()

    if topic_id == "rogue_5" and "sv" in stage_id and "dlc1" in stage_id:
        annotated_stage["field"] = "sui_portal_b"
    elif topic_id == "rogue_5" and "sv" in stage_id:
        annotated_stage["field"] = "sui_portal"

    return annotated_stage


def _group_stages_with_same_name(stage_list: list[dict], topic_id: str) -> list[dict]:
    grouped_stages: dict[str, list[dict]] = {}

    for stage in stage_list:
        stage_name = stage["name"]["zh"]
        if stage_name not in grouped_stages:
            grouped_stages[stage_name] = []
        grouped_stages[stage_name].append(stage)

    return [
        {
            "id": stages[0]["id"],
            "code": stages[0]["code"],
            "name": stages[0]["name"],
            "stages": [
                {
                    key: value
                    for key, value in _add_stage_field(stage, topic_id).items()
                    if key not in {"code", "name"}
                }
                for stage in stages
            ],
        }
        for stages in grouped_stages.values()
        if len(stages) > 1
    ]


def _dedupe_grouped_stage_data(grouped_stage_list: list[dict]) -> list[dict]:
    for grouped_stage in grouped_stage_list:
        level_id_groups: dict[str, list[dict]] = {}
        for stage in grouped_stage["stages"]:
            level_id = stage["levelId"]
            if level_id not in level_id_groups:
                level_id_groups[level_id] = []
            level_id_groups[level_id].append(stage)

        deduped_data = []
        for level_id, stages in level_id_groups.items():
            if len(stages) == 1:
                deduped_data.extend(stages)
                continue

            linked_stages = [stage for stage in stages if stage["linkedStageId"]]
            if linked_stages:
                deduped_data.extend(linked_stages)
            else:
                deduped_data.extend(stages)

        grouped_stage["stages"] = deduped_data

    return grouped_stage_list


def _build_stage_list(
    topic: str,
    source_path: Path,
    en_source_path: Path,
    jp_source_path: Path,
) -> list[dict]:
    with source_path.open(encoding="utf-8") as source_file:
        data = json.load(source_file)
    with en_source_path.open(encoding="utf-8") as en_source_file:
        en_data = json.load(en_source_file)
    with jp_source_path.open(encoding="utf-8") as jp_source_file:
        jp_data = json.load(jp_source_file)

    stages = data["details"][topic]["stages"]
    en_stages = en_data["details"].get(topic, {}).get("stages", {})
    jp_stages = jp_data["details"].get(topic, {}).get("stages", {})

    return [
        _strip_stage_keys(
            _add_localized_stage_texts(
                dict(stage_data),
                en_stages.get(stage_id),
                jp_stages.get(stage_id),
            )
        )
        for stage_id, stage_data in stages.items()
    ]


def _load_stage_extrainfo_by_level_id(source_path: Path) -> dict[str, dict]:
    with source_path.open(encoding="utf-8") as source_file:
        data = json.load(source_file)

    return {
        _get_level_id_basename(level_id): stage_info
        for level_id, stage_info in data.items()
    }


@lru_cache(maxsize=None)
def _load_ro_stage_configs_by_level_id(topic: str) -> dict[str, dict[str, Any]]:
    stage_configs_by_level_id: dict[str, dict[str, Any]] = {}
    for source_path in sorted(RO_STAGE_DATA_DIR.glob(f"{topic}_*.json")):
        with source_path.open(encoding="utf-8") as source_file:
            data = json.load(source_file)

        for stage_info in data.get("stages", []):
            config = stage_info.get("config")
            if not config or not config.get("levelId"):
                continue
            stage_configs_by_level_id[_get_level_id_basename(config["levelId"])] = (
                config
            )

    return stage_configs_by_level_id


def _build_stage_extrainfo_fallback(
    topic: str,
    stage: dict,
    ro_stage_configs_by_level_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    level_id = _get_level_id_basename(stage["levelId"])
    level_config = ro_stage_configs_by_level_id.get(level_id, {})

    stage_data_path = _get_roguelike_level_data_path(topic, level_id)
    with stage_data_path.open(encoding="utf-8") as source_file:
        stage_data = json.load(source_file)

    sp_terrain = get_special_tiles(stage_data["mapData"]["tiles"])
    if not sp_terrain:
        sp_terrain = None

    runes_data = get_runes(stage_data["runes"]) if stage_data["runes"] else None
    all_mods = None
    normal_mods = None
    elite_mods = None
    if runes_data:
        all_mods = runes_data["all_mods"]
        normal_mods = runes_data["normal_mods"]
        elite_mods = runes_data["elite_mods"]

    elite_desc = generate_desc(elite_mods)

    return {
        "id": stage["id"],
        "levelId": level_id,
        "code": level_config.get("code", stage["code"]),
        "name_zh": level_config.get("name_zh", stage["name"]["zh"]),
        "name_ja": level_config.get("name_ja", stage["name"]["ja"]),
        "name_en": level_config.get("name_en", stage["name"]["en"]),
        "category": level_config.get("category"),
        "floors": level_config.get("floors"),
        "addInfo_zh": level_config.get("addInfo_zh"),
        "addInfo_ja": level_config.get("addInfo_ja"),
        "addInfo_en": level_config.get("addInfo_en"),
        "eliteDesc_zh": elite_desc.get("zh"),
        "eliteDesc_ja": elite_desc.get("ja"),
        "eliteDesc_en": elite_desc.get("en"),
        "all_mods": all_mods,
        "normal_mods": normal_mods,
        "elite_mods": elite_mods,
        "sp_terrain": sp_terrain,
    }


def _build_stage_extrainfo_data(
    topic: str = "ro6",
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    extrainfo_source_path: Path = IS_STAGE_EXTRAINFO_PATH,
) -> dict[str, dict]:
    topic_id = _get_roguelike_topic_id(topic)
    stage_list = _build_stage_list(
        topic=topic_id,
        source_path=source_path,
        en_source_path=en_source_path,
        jp_source_path=jp_source_path,
    )
    stage_extrainfo_by_level_id = _load_stage_extrainfo_by_level_id(
        extrainfo_source_path
    )
    ro_stage_configs_by_level_id = _load_ro_stage_configs_by_level_id(topic)
    stage_data = {
        level_id: stage_extrainfo_by_level_id.get(
            level_id,
            _build_stage_extrainfo_fallback(
                topic=topic,
                stage=stage,
                ro_stage_configs_by_level_id=ro_stage_configs_by_level_id,
            ),
        )
        for stage in stage_list
        for level_id in [_get_level_id_basename(stage["levelId"])]
    }

    return stage_data


def export_stage_extrainfo(
    topic: str = "ro5",
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    extrainfo_source_path: Path = IS_STAGE_EXTRAINFO_PATH,
    output_path: Path | None = None,
) -> dict[str, dict]:
    if output_path is None:
        output_path = _get_custom_stage_extrainfo_path(topic)

    stage_data = _build_stage_extrainfo_data(
        topic=topic,
        source_path=source_path,
        en_source_path=en_source_path,
        jp_source_path=jp_source_path,
        extrainfo_source_path=extrainfo_source_path,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(stage_data, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return stage_data


def _load_existing_stage_level_ids(source_path: Path) -> set[str]:
    if not source_path.exists():
        return set()

    with source_path.open(encoding="utf-8") as source_file:
        data = json.load(source_file)

    existing_level_ids = set()
    for key, stage_info in data.items():
        if isinstance(stage_info, dict) and stage_info.get("levelId"):
            existing_level_ids.add(_get_level_id_basename(stage_info["levelId"]))
            continue
        existing_level_ids.add(_get_level_id_basename(key))

    return existing_level_ids


def export_new_stage_extrainfo(
    topic: str = "ro5",
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    extrainfo_source_path: Path = IS_STAGE_EXTRAINFO_PATH,
    existing_extrainfo_path: Path | None = None,
    output_path: Path | None = None,
) -> dict[str, dict]:
    if existing_extrainfo_path is None:
        existing_extrainfo_path = _get_custom_stage_extrainfo_path(topic)
    if output_path is None:
        output_path = CUSTOM_STAGE_OUTPUT_DIR / topic / CUSTOM_STAGE_NEW_STAGE_FILENAME

    stage_data = _build_stage_extrainfo_data(
        topic=topic,
        source_path=source_path,
        en_source_path=en_source_path,
        jp_source_path=jp_source_path,
        extrainfo_source_path=extrainfo_source_path,
    )
    existing_level_ids = _load_existing_stage_level_ids(existing_extrainfo_path)
    new_stage_data = {
        level_id: stage_info
        for level_id, stage_info in stage_data.items()
        if level_id not in existing_level_ids
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(new_stage_data, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return new_stage_data


def export_stages_config(
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> list[dict]:
    stage_list = _build_stage_list(
        topic="rogue_6",
        source_path=source_path,
        en_source_path=en_source_path,
        jp_source_path=jp_source_path,
    )
    grouped_stage_list = _group_stages_with_same_name(stage_list, topic_id="rogue_5")
    grouped_stage_list = _dedupe_grouped_stage_data(grouped_stage_list)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(grouped_stage_list, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return grouped_stage_list


if __name__ == "__main__":
    export_new_stage_extrainfo("ro6")
    # export_stage_extrainfo('ro5')
    export_stages_config()
