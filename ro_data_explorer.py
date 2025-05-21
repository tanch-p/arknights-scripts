from os import walk
import pprint
import os
import json
from walk import get_all_file_paths

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


folders = ['ro1','ro2', 'ro3', 'ro4']

for folder in folders:
    path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
    )
    file_paths = get_all_file_paths(path)
    for file_path in file_paths:
        with open(file_path, encoding="utf-8") as f:
            stage_data = json.load(f)
        levelId = file_path.split("/")[-1]
        # print(stage_data['runes'])

