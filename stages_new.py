from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STAGE_CONFIG_PATH = BASE_DIR / "stage_config.json"
LEVELS_DIR = BASE_DIR / "cn_data/zh_CN/gamedata/levels"
OUTPUT_DIR = BASE_DIR / "ro_stage_data"


def _get_topic(stage_group_id: str) -> str:
    stage_group_id = stage_group_id.lower()
    if "ro5" in stage_group_id:
        return "ro5"
    if "ro4" in stage_group_id:
        return "ro4"
    raise ValueError(f"Unsupported stage topic for id: {stage_group_id}")


def _get_level_config_path(level_id: str) -> Path:
    return LEVELS_DIR / f"{level_id.lower()}.json"


def expand_stage_configs(
    stage_config_path: Path = STAGE_CONFIG_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    with stage_config_path.open(encoding="utf-8") as stage_config_file:
        stage_groups = json.load(stage_config_file)

    output_dir.mkdir(exist_ok=True)

    for stage_group in stage_groups:
        topic = _get_topic(stage_group["id"])

        for stage_item in stage_group["stages"]:
            stage_item["topic"] = topic
            level_id = (
                stage_item["levelReplaceIds"][-1]
                if stage_item["levelReplaceIds"]
                else stage_item["levelId"]
            )
            level_config_path = _get_level_config_path(level_id)

            with level_config_path.open(encoding="utf-8") as level_config_file:
                stage_item["config"] = json.load(level_config_file)

        output_path = output_dir / f"{stage_group['id']}.json"
        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(stage_group, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")

    return stage_groups


if __name__ == "__main__":
    expand_stage_configs()
