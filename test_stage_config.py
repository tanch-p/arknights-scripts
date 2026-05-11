from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from stage_config import ROGUELIKE_TOPIC_TABLE_PATH, export_rogue_5_stages


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

    export_rogue_5_stages(output_path=output_path)

    with output_path.open(encoding="utf-8") as output_file:
        exported_data = json.load(output_file)

    exported_level_ids = {
        item["levelId"] for group in exported_data for item in group["data"]
    }
    expected_count = _count_expected_exported_level_ids(ROGUELIKE_TOPIC_TABLE_PATH)

    assert len(exported_level_ids) == expected_count
