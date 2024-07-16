import os
from os import walk
import json
from waves_new import get_timeline

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


folders = ['ro2', 'ro3', 'ro4']
stages_to_ignore = ['level_rogue1_1-4','level_rogue1_3-8', 'level_rogue2_2-5',
                    'level_rogue3_3-3', 'level_rogue3_ev-9']
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
        # if not 'level_rogue3_1-2.json' in stage_id:
        #     continue
        print(stage_id)
        write_path = os.path.join(
            script_dir, 'ro_wave_timelines', folder, stage_id)
        timeline = get_timeline(folder, stage_id, log=False)
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(timeline, f, ensure_ascii=False, separators=(',', ':'))
