from os import walk
import pprint
import os
import json
from walk import get_all_file_paths

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

parsed_rune_keys = ['enemy_attribute_mul', 'ebuff_attribute', 'enemy_attribute_add', 'char_attribute_mul', 'char_attribute_add', 'enemy_skill_blackb_add', 'enemy_skill_blackb_mul', 'enemy_dynamic_ability_new', 'level_hidden_group_enable', 'level_hidden_group_disable', 'level_enemy_replace', 'level_predefines_enable', 'global_forbid_location', 'env_gbuff_new',
                    'env_system_new', 'enemy_talent_blackb_mul', 'enemy_talent_blackb_add', 'level_predefines_skill_replace', 'enemy_attackradius_mul', 'map_tile_blackb_mul', 'global_cost_recovery_mul', 'default_key', 'char_respawntime_mul', 'char_skill_cd_add', 'enemy_skill_cd_mul', 'enemy_skill_init_cd_mul', 'cbuff_max_cost', 'char_skill_cd_mul', 'global_lifepoint', 'char_skill_blackb_mul']

cn_stage_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/stage_table.json"
)
activity_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/activity_table.json"
)

with open(cn_stage_table_path, encoding="utf-8") as f:
    cn_stage_table = json.load(f)
with open(activity_table_path, encoding="utf-8") as f:
    activity_table = json.load(f)


list = []
for stageId in cn_stage_table['stages']:
    stage_info = cn_stage_table['stages'][stageId]
    if not stage_info['levelId']:
        continue
    file_path = stage_info['levelId'].lower()
    stage_data_path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/{file_path}.json",
    )
    try:
        with open(stage_data_path, encoding="utf-8") as f:
            stage_data = json.load(f)
    except FileNotFoundError as e:
        # print(f"{file_path} not found")
        pass
    if not stage_data:
        continue

    if not stage_info['stageType'] in list:
        list.append(stage_info['stageType'])
    # if (stage_data['runes']):
    #     for rune in stage_data['runes']:
    #         if rune['difficultyMask'] not in ['FOUR_STAR', 'NORMAL', "ALL"]:
    #             print(rune['difficultyMask'])
    #             print(levelId)
    #         key = rune['key']
    #         if not key in parsed_rune_keys:
    #             print(levelId)
    #             print(key)

    #         # if('add' in key):
    #         if key == 'enemy_dynamic_ability_new':
    #             print(levelId)
    #             print(key)

print(list)