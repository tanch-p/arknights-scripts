import os
from os import walk
import json
from waves_new import get_wave_spawns_data

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

STAGES_WITH_ENEMY_REF_TO_REPLACE = {'level_rogue4_b-4': 'level_rogue4_b-4-c',
                                    'level_rogue4_b-4-b': 'level_rogue4_b-4-d',
                                    'level_rogue4_b-5': 'level_rogue4_b-5-c',
                                    'level_rogue4_b-5-b': 'level_rogue4_b-5-d',
                                    'level_rogue4_1-1': 'levelreplacers/level_rogue4_1-1_r2',
                                    'level_rogue4_1-2': 'levelreplacers/level_rogue4_1-2_r2',
                                    'level_rogue4_1-3': 'levelreplacers/level_rogue4_1-3_r2',
                                    'level_rogue4_1-4': 'levelreplacers/level_rogue4_1-4_r2',
                                    'level_rogue4_2-1': 'levelreplacers/level_rogue4_2-1_r2',
                                    'level_rogue4_2-2': 'levelreplacers/level_rogue4_2-2_r2',
                                    'level_rogue4_2-3': 'levelreplacers/level_rogue4_2-3_r2',
                                    'level_rogue4_2-4': 'levelreplacers/level_rogue4_2-4_r2',
                                    'level_rogue4_2-5': 'levelreplacers/level_rogue4_2-5_r2',
                                    'level_rogue4_2-6': 'levelreplacers/level_rogue4_2-6_r1',
                                    'level_rogue4_3-1': 'levelreplacers/level_rogue4_3-1_r2',
                                    'level_rogue4_3-2': 'levelreplacers/level_rogue4_3-2_r2',
                                    'level_rogue4_3-3': 'levelreplacers/level_rogue4_3-3_r2',
                                    'level_rogue4_3-4': 'levelreplacers/level_rogue4_3-4_r2',
                                    'level_rogue4_3-5': 'levelreplacers/level_rogue4_3-5_r2',
                                    'level_rogue4_3-6': 'levelreplacers/level_rogue4_3-6_r2',
                                    'level_rogue4_3-7': 'levelreplacers/level_rogue4_3-7_r1',
                                    'level_rogue4_4-1': 'levelreplacers/level_rogue4_4-1_r2',
                                    'level_rogue4_4-2': 'levelreplacers/level_rogue4_4-2_r2',
                                    'level_rogue4_4-3': 'levelreplacers/level_rogue4_4-3_r2',
                                    'level_rogue4_4-4': 'levelreplacers/level_rogue4_4-4_r2',
                                    'level_rogue4_4-5': 'levelreplacers/level_rogue4_4-5_r2',
                                    'level_rogue4_4-6': 'levelreplacers/level_rogue4_4-6_r2',
                                    'level_rogue4_4-7': 'levelreplacers/level_rogue4_4-7_r2',
                                    'level_rogue4_4-8': 'levelreplacers/level_rogue4_4-8_r1',
                                    'level_rogue4_4-9': 'levelreplacers/level_rogue4_4-9_r1',
                                    'level_rogue4_5-1': 'levelreplacers/level_rogue4_5-1_r2',
                                    'level_rogue4_5-2': 'levelreplacers/level_rogue4_5-2_r2',
                                    'level_rogue4_5-3': 'levelreplacers/level_rogue4_5-3_r2',
                                    'level_rogue4_5-4': 'levelreplacers/level_rogue4_5-4_r2',
                                    'level_rogue4_5-5': 'levelreplacers/level_rogue4_5-5_r2',
                                    'level_rogue4_5-6': 'levelreplacers/level_rogue4_5-6_r2',
                                    'level_rogue4_5-7': 'levelreplacers/level_rogue4_5-7_r2',
                                    'level_rogue4_5-8': 'levelreplacers/level_rogue4_5-8_r1',
                                    'level_rogue4_6-1': 'levelreplacers/level_rogue4_6-1_r2',
                                    'level_rogue4_6-2': 'levelreplacers/level_rogue4_6-2_r2',
                                    'level_rogue4_7-1': 'levelreplacers/level_rogue4_7-1_r1',
                                    'level_rogue4_7-2': 'levelreplacers/level_rogue4_7-2_r1',
                                    'level_rogue4_b-1': 'levelreplacers/level_rogue4_b-1_r1',
                                    'level_rogue4_b-1-b': 'levelreplacers/level_rogue4_b-1-b_r1',
                                    'level_rogue4_b-1-c': 'levelreplacers/level_rogue4_b-1-c_r1',
                                    'level_rogue4_b-2': 'levelreplacers/level_rogue4_b-2_r1',
                                    'level_rogue4_b-2-b': 'levelreplacers/level_rogue4_b-2-b_r1',
                                    'level_rogue4_b-2-c': 'levelreplacers/level_rogue4_b-2-c_r1',
                                    'level_rogue4_b-3': 'levelreplacers/level_rogue4_b-3_r1',
                                    'level_rogue4_b-3-b': 'levelreplacers/level_rogue4_b-3-b_r1',
                                    'level_rogue4_b-3-c': 'levelreplacers/level_rogue4_b-3-c_r1',
                                    'level_rogue4_b-6': 'levelreplacers/level_rogue4_b-6_r1',
                                    'level_rogue4_ev-1': 'levelreplacers/level_rogue4_ev-1_r1',
                                    'level_rogue4_ev-2': 'levelreplacers/level_rogue4_ev-2_r1',
                                    'level_rogue4_t-1': 'levelreplacers/level_rogue4_t-1_r1',
                                    'level_rogue4_t-2': 'levelreplacers/level_rogue4_t-2_r1',
                                    'level_rogue4_t-3': 'levelreplacers/level_rogue4_t-3_r1',
                                    'level_rogue4_t-4': 'levelreplacers/level_rogue4_t-4_r1',
                                    'level_rogue4_t-5': 'levelreplacers/level_rogue4_t-5_r1',
                                    'level_rogue4_t-6': 'levelreplacers/level_rogue4_t-6_r1',
                                    'level_rogue4_t-7': 'levelreplacers/level_rogue4_t-7_r1',
                                    'level_rogue4_t-8': 'levelreplacers/level_rogue4_t-8_r1', }


# for consumption in enemy routes
folders = ['ro1','ro2', 'ro3', 'ro4','ro5']
stages_to_ignore = []
for folder in folders:
    files = []
    path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
    )
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend([f for (
            dirpath, dirnames, filenames) in os.walk(path) for f in filenames])
        break
    for stage_id in files:
        if stage_id.split(".")[0] in stages_to_ignore:
            continue
        if not 'level_rogue5_b-4.json' in stage_id:
            continue
        if "r1" in stage_id or "r2" in stage_id:
            continue
        if stage_id in STAGES_WITH_ENEMY_REF_TO_REPLACE:
            stage_id = STAGES_WITH_ENEMY_REF_TO_REPLACE[stage_id]
        print(stage_id)
        file_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{stage_id}",
        )
        with open(file_path, encoding="utf-8") as f:
            stage_data = json.load(f)
        # Example usage:
        analysis = get_wave_spawns_data(stage_data,stage_id.replace(".json",""),log=True)

        # timeline = get_waves_data(
        #     stage_data, stage_id.replace(".json", ""), log=True)
        # write_path = os.path.join(
        #     script_dir, 'ro_wave_timelines', folder, stage_id)
        # if timeline:
        #     with open(write_path, 'w+', encoding='utf-8') as f:
        #         json.dump(timeline, f, ensure_ascii=False, indent=4)
