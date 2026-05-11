from __future__ import annotations

import json
from pathlib import Path


ROGUELIKE_TOPIC_TABLE_PATH = Path(
    "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
TEMP_OUTPUT_PATH = Path("temp.json")


def export_rogue_5_stages(
    source_path: Path = ROGUELIKE_TOPIC_TABLE_PATH,
    output_path: Path = TEMP_OUTPUT_PATH,
) -> list[dict]:
    with source_path.open(encoding="utf-8") as source_file:
        data = json.load(source_file)

    stages = data["details"]["rogue_5"]["stages"]
    if output_path.exists():
        with output_path.open(encoding="utf-8") as output_file:
            stage_list = json.load(output_file)
    else:
        stage_list = []

    existing_stage_ids = {
        stage["id"] for stage in stage_list if isinstance(stage, dict) and "id" in stage
    }

    for stage_data in stages.values():
        if stage_data["id"] not in existing_stage_ids:
            stage_list.append(dict(stage_data))
            existing_stage_ids.add(stage_data["id"])

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(stage_list, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    return stage_list


if __name__ == "__main__":
    export_rogue_5_stages()
