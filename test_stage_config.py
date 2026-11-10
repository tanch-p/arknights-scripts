from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from stage_config import (
    IS_STAGE_EXTRAINFO_PATH,
    ROGUELIKE_TOPIC_TABLE_PATH,
    export_new_stage_extrainfo,
    export_stage_extrainfo,
    export_stages_config,
)


def _count_expected_exported_level_ids(source_path: Path) -> int:
    with source_path.open(encoding="utf-8") as source_file:
        data = json.load(source_file)

    grouped_stages: dict[str, list[dict]] = defaultdict(list)
    for stage in data["details"]["rogue_5"]["stages"].values():
        grouped_stages[stage["name"]].append(stage)

    count = 0
    for stages in grouped_stages.values():
        if len(stages) <= 1:
            continue

        level_id_groups: dict[str, list[dict]] = defaultdict(list)
        for stage in stages:
            level_id_groups[stage["levelId"]].append(stage)

        for same_level_stages in level_id_groups.values():
            if any(stage["linkedStageId"] for stage in same_level_stages):
                count += 1
            else:
                count += len(same_level_stages)

    return count


def test_temp_json_stage_count_matches_expected(tmp_path: Path) -> None:
    output_path = tmp_path / "stage_config.json"

    export_stages_config(output_path=output_path)

    with output_path.open(encoding="utf-8") as output_file:
        exported_data = json.load(output_file)

    exported_level_ids = {
        item["levelId"] for group in exported_data for item in group["stages"]
    }
    expected_count = _count_expected_exported_level_ids(ROGUELIKE_TOPIC_TABLE_PATH)

    assert len(exported_level_ids) == expected_count


def test_export_new_stage_extrainfo_filters_existing_level_ids(tmp_path: Path) -> None:
    all_stage_data = export_stage_extrainfo(
        topic="ro5",
        output_path=tmp_path / "all_extrainfo.json",
    )
    existing_level_id, existing_stage_info = next(iter(all_stage_data.items()))

    existing_extrainfo_path = (
        tmp_path / "custom_data" / "stages" / "ro5" / "extrainfo.json"
    )
    existing_extrainfo_path.parent.mkdir(parents=True, exist_ok=True)
    with existing_extrainfo_path.open("w", encoding="utf-8") as existing_file:
        json.dump(
            {
                "ro5_existing_stage": {
                    **existing_stage_info,
                    "levelId": f"Obt/Roguelike/RO5/{existing_level_id}",
                }
            },
            existing_file,
            ensure_ascii=False,
            indent=2,
        )
        existing_file.write("\n")

    output_path = tmp_path / "custom_data" / "stages" / "ro5" / "new_stages.json"
    new_stage_data = export_new_stage_extrainfo(
        topic="ro5",
        existing_extrainfo_path=existing_extrainfo_path,
        output_path=output_path,
    )

    assert existing_level_id not in new_stage_data
    assert len(new_stage_data) == len(all_stage_data) - 1

    with output_path.open(encoding="utf-8") as output_file:
        assert json.load(output_file) == new_stage_data


def test_export_stage_extrainfo_builds_rich_fallback_for_missing_source_entry(
    tmp_path: Path,
) -> None:
    with IS_STAGE_EXTRAINFO_PATH.open(encoding="utf-8") as source_file:
        extrainfo_source = json.load(source_file)

    missing_level_id = "level_rogue5_1-1"
    extrainfo_source.pop(missing_level_id)

    temp_source_path = tmp_path / "is_stages_extrainfo.json"
    with temp_source_path.open("w", encoding="utf-8") as temp_source_file:
        json.dump(extrainfo_source, temp_source_file, ensure_ascii=False, indent=2)
        temp_source_file.write("\n")

    stage_data = export_stage_extrainfo(
        topic="ro5",
        extrainfo_source_path=temp_source_path,
        output_path=tmp_path / "fallback_extrainfo.json",
    )

    fallback_stage = stage_data[missing_level_id]

    assert fallback_stage["id"] == "ro5_e_1_1"
    assert fallback_stage["levelId"] == missing_level_id
    assert fallback_stage["name_zh"] == "狡鼷三窟"
    assert fallback_stage["floors"] == [1]
    assert fallback_stage["addInfo_zh"] is not None
    assert fallback_stage["enemy_list"]
    assert "eliteDesc_zh" in fallback_stage
    assert "normal_mods" in fallback_stage
