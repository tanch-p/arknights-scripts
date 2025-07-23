from os import walk
import pprint
import os
import json
from walk import get_all_file_paths

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


folders = ['ro1','ro2', 'ro3', 'ro4','ro5']
parsed_rune_keys=['enemy_attribute_mul','ebuff_attribute','enemy_attribute_add','char_attribute_mul','char_attribute_add','enemy_skill_blackb_add','enemy_skill_blackb_mul','enemy_dynamic_ability_new','level_hidden_group_enable','level_hidden_group_disable','level_enemy_replace','level_predefines_enable','global_forbid_location','env_gbuff_new','env_system_new','enemy_talent_blackb_mul','enemy_talent_blackb_add','level_predefines_skill_replace','enemy_attackradius_mul','map_tile_blackb_mul','global_cost_recovery_mul','default_key','char_respawntime_mul','char_skill_cd_add','enemy_skill_cd_mul','enemy_skill_init_cd_mul','cbuff_max_cost','char_skill_cd_mul','global_lifepoint','char_skill_blackb_mul']

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
        if not 'rogue5' in levelId:
            continue
        # for enemy in stage_data['enemyDbRefs']:
        #     if enemy['useDb'] is False:
        #         print(levelId,enemy['id'])
        if(stage_data['runes']):
            for rune in stage_data['runes']:
                if rune['key']== 'level_predefine_tokens_random_spawn_on_tile':
                    keys = [item['key'] for item in rune['blackboard']]
                    if not 'tile' in keys:
                        print(levelId)
                # if rune['difficultyMask'] not in ['FOUR_STAR','NORMAL',"ALL"]:
                #     print(rune['difficultyMask'])
                #     print(levelId)
                # key = rune['key']
                # if not key in parsed_rune_keys:
                #     print(levelId)
                #     print(key)

                # # if('add' in key): 
                # if key == 'enemy_dynamic_ability_new':
                #     print(levelId)
                #     print(key)

