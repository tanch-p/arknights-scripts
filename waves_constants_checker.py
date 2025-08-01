import json
import pprint
import os
from os import walk

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

# README
# 1. randomSpawnGroupKey between fragments are separate.
# 2. hiddenGroups can also have randomSpawnGroupKey
# 3. bonus wave may not be wave #2 but in fragment... as in level_rogue2_5-8
# 4.

folders = ['ro1', 'ro2', 'ro3', 'ro4', 'ro5']

files = []

for folder in folders:
    path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
    )
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend([os.path.join(dirpath, f) for (
            dirpath, dirnames, filenames) in os.walk(path) for f in filenames])
        break

for file_path in files:
    with open(file_path, encoding="utf-8") as f:
        stage_data = json.load(f)
        for tile in stage_data['mapData']['tiles']:
            if tile['passableMask'] != "FLY_ONLY" and tile['passableMask'] != "ALL":
                print(tile)
        for wave in stage_data['waves']:
            for frag_index, fragment in enumerate(wave['fragments']):
                for action in fragment['actions']:
                    valid = True
                    # if action['hiddenGroup'] is not None and action['randomSpawnGroupKey'] is not None and action['actionType'] != 'ACTIVATE_PREDEFINED' and action['weight'] != 100:
                    #     valid=False
                    if action['managedByScheduler'] is False:
                        print('managedByScheduler is false', file_path)
                        valid = False
                    if action['blockFragment'] is True:
                        print('blockFragment is True', file_path)
                        valid = False
                    if action['randomType'] != 'ALWAYS':
                        print('randomType is not ALWAYS', file_path)
                        valid = False
                    if action['refreshType'] != 'ALWAYS':
                        print('refreshType is not ALWAYS', file_path)
                        valid = False
                    if action['forceBlockWaveInBranch'] is True:
                        print('forceBlockWaveInBranch is True', file_path)
                        valid = False
                    if not valid:
                        # pp.pprint(action)
                        pass
