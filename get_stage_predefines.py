import os
from os import walk
import json
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

folder = "ro4"

files = []
path = os.path.join(
    script_dir,
    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
)
for (dirpath, dirnames, filenames) in walk(path):
    files.extend([f for (
        dirpath, dirnames, filenames) in os.walk(path) for f in filenames])
    break
data = {}
files.sort()
for stage_id in files:
    stage_data_path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{stage_id}",
    )
    with open(stage_data_path, encoding="utf-8") as f:
        stage_data = json.load(f)
    temp = {}
    for item in stage_data['predefines']['tokenInsts']:
        key = item['alias']
        hiddenGroup = None
        randomSpawnGroupKey = None
        randomSpawnGroupPackKey = None
        weight = 0
        for wave in stage_data['waves']:
            for fragment in wave['fragments']:
                for action in fragment['actions']:
                    if action['key'] == key:
                        hiddenGroup = action['hiddenGroup']
                        randomSpawnGroupKey = action['randomSpawnGroupKey']
                        randomSpawnGroupPackKey = action['randomSpawnGroupPackKey']
                        weight = action['weight']
        temp[key] = {
            "position": {
                "x": item['position']['col'],
                "y": item['position']['row']
            },
            "hidden": item['hidden'],
            "hiddenGroup": hiddenGroup,
            "randomSpawnGroupKey": randomSpawnGroupKey,
            "randomSpawnGroupPackKey": randomSpawnGroupPackKey,
            "weight": weight,
            # "inst": item['inst'],
            "skillIndex": item['skillIndex'],
            "mainSkillLvl": item['mainSkillLvl'],
        }

    data[stage_id] = temp

with open("stage_predefines.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
