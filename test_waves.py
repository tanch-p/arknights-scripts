from waves import get_wave_data
from operator import itemgetter
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

test_cases = [
    # {
    #     "path": "ro2/level_rogue2_3-5.json",
    #     'id': "level_rogue2_3-5",
    #     "all_possible_enemy_count": [47],
    #             "sp_count": [48],
    #             "elite_sp_count": [47],
    # },
    # {
    #     "path": "ro2/level_rogue2_1-1.json",
    #             'id': "level_rogue2_1-1",
    #             "all_possible_enemy_count": [22, 23, 24, 25, 26, 27, 29, 31],
    #             "sp_count": [28, 30, 32],
    #             "elite_sp_count": None,
    # },
    # {
    #     "path": "ro1/level_rogue1_4-6.json",
    #     'id': "level_rogue1_4-6",
    #             "all_possible_enemy_count": [19, 20, 21, 22, 23],
    #     "sp_count": [24],
    #             "elite_sp_count": None,
    # },
    # {
    #     "path": "ro3/level_rogue3_1-2.json",
    #     'id': "level_rogue3_1-2",
    #             "all_possible_enemy_count": [31],
    #     "sp_count": [32],
    #             "elite_sp_count": [32],
    # },
    #     {
    #     "path": "ro3/level_rogue3_3-2.json",
    #     'id': "level_rogue3_3-2",
    #             "all_possible_enemy_count": [33,34],
    #     "sp_count": [35],
    #             "elite_sp_count": None,
    # },
    # {
    #     "path": "ro4/level_rogue4_4-10.json",
    #     'id': "level_rogue4_4-10",
    #             "all_possible_enemy_count": [42],
    #     "sp_count": [43],
    #             "elite_sp_count": None,
    # },
    {
        "path": "ro4/level_rogue4_b-8.json",
        'id': "level_rogue4_b-8",
                "all_possible_enemy_count": [55],
        "sp_count": None,
                "elite_sp_count": None,
    },
]
# level_rogue3_b-1-b
# level_rogue3_1-2
# level_rogue3_1-3
# level_rogue3_1-4
# level_rogue3_2-1
# level_rogue3_2-2
# level_rogue3_2-4
# level_rogue3_3-2
# level_rogue3_3-4
# level_rogue3_4-2
# level_rogue3_4-4
# level_rogue3_4-7
# level_rogue3_5-1
# level_rogue3_5-2
# level_rogue3_5-4
# level_rogue3_5-5

for case in test_cases:
    stage_data_path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{case['path']}",
    )
    with open(stage_data_path, encoding="utf-8") as f:
        stage_data = json.load(f)
        wave_data = get_wave_data(stage_data, case['id'], log=True)
        enemy_list, elite_enemy_list, sp_count, elite_sp_count, all_possible_enemy_count = itemgetter(
            "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "all_possible_enemy_count")(wave_data)
        assert (sp_count) == case['sp_count']
        assert (elite_sp_count) == case['elite_sp_count']
        assert (all_possible_enemy_count) == case['all_possible_enemy_count']
