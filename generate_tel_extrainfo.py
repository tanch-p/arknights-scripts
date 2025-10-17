import os
import json
from operator import itemgetter

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


"""
Tel Arrow Color Indexes
0 - orange
1 - green
2 - pink
3 - yellow
-1 - blue

Direction - direction stairs is towards

"""

def get_all_files(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.abspath(os.path.join(root, file)))
    return file_paths


folders = ['ro5']


def get_row_col(tile_index, map_data):
    for rowIdx, row in enumerate(map_data):
        for colidx, col in enumerate(row):
            if tile_index == col:
                return {"row": rowIdx, "col": colidx}


def get_tel_data(stage_data):
    tels = {}
    count = 0
    map_data = stage_data['mapData']['map']
    tiles = stage_data['mapData']['tiles']
    for tile_index, tile in enumerate(tiles):
        if tile['tileKey'] == 'tile_telin':
            count += 1
            tels[tile_index] = ({"tileKey": tile['tileKey'], "colorIndex": 0, "direction": "", "type": "arrow",  "position": get_row_col(
                tile_index, map_data)})
        if tile['tileKey'] == 'tile_telout':
            tels[tile_index] = ({"tileKey": tile['tileKey'], "colorIndex": 0, "direction": "", "type": "arrow", "position": get_row_col(
                tile_index, map_data)})
    return tels


data = {}
for folder in folders:
    files = []
    path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
    )
    all_files = get_all_files(path)
    all_files.sort()
    for file_path in all_files:
        if "r1." in file_path or "r2." in file_path or "dlc1" in file_path:
            continue
        with open(file_path, encoding="utf-8") as f:
            stage_data = json.load(f)
        stage_id = file_path.split("/")[-1]
        tel_data = get_tel_data(stage_data)
        if len(tel_data) == 0:
            continue
        data[stage_id.replace(".json","")] = get_tel_data(stage_data)

write_path = os.path.join(
    script_dir, 'tel_extrainfo_new.json')
with open(write_path, 'w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
