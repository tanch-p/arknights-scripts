from __future__ import annotations

import json
from pathlib import Path


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
EXTRAINFO_OUTPUT_PATH = Path("ro_stage_extrainfo.json")
STAGE_KEYS_TO_REMOVE = {
    "loadingPicId",
    "capsulePool",
    "capsuleProb",
    "specialNodeId",
    "redCapsulePool",
    "redCapsuleProb",
    "vutresProb",
}


def _strip_stage_keys(stage_data: dict) -> dict:
    return {
        key: value
        for key, value in stage_data.items()
        if key not in STAGE_KEYS_TO_REMOVE
    }


def _get_localized_text(
    zh_value: str | None,
    jp_value: str | None,
    en_value: str | None,
) -> dict[str, str | None]:
    return {"zh": zh_value, "ja": jp_value, "en": en_value}


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


def _build_rogue_5_stage_list(
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

    stages = data["details"]["rogue_5"]["stages"]
    en_stages = en_data["details"].get("rogue_5", {}).get("stages", {})
    jp_stages = jp_data["details"].get("rogue_5", {}).get("stages", {})

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


def export_rogue_5_stage_extrainfo(
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    output_path: Path = EXTRAINFO_OUTPUT_PATH,
) -> list[dict]:
    stage_list = _build_rogue_5_stage_list(
        source_path=source_path,
        en_source_path=en_source_path,
        jp_source_path=jp_source_path,
    )

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(stage_list, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return stage_list


def export_rogue_5_stages(
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    en_source_path: Path = EN_ROGUELIKE_TOPIC_TABLE_PATH,
    jp_source_path: Path = JP_ROGUELIKE_TOPIC_TABLE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> list[dict]:
    stage_list = _build_rogue_5_stage_list(
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
    export_rogue_5_stages()
