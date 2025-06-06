from operator import itemgetter
from runes import parse_runes
from tiles import get_special_tiles
from waves import get_wave_data
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

with open("is_stages_extrainfo.json", encoding="utf-8") as f:
    extra_info_list = json.load(f)

with open("is_stages_list.json", encoding="utf-8") as f:
    stages_list = json.load(f)

STAGES_TO_IGNORE = ['level_rogue4_b-4', 'level_rogue4_b-4-b',
                    'level_rogue4_b-5', 'level_rogue4_b-5-b']

data = {}
for key in extra_info_list:
    if 'rogue1' in key:
        folder = "ro1"
    elif 'rogue2' in key:
        folder = "ro2"
    elif 'rogue3' in key:
        folder = "ro3"
    else:
        folder = "ro4"

    stage_data_path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{key}.json",
    )
    with open(stage_data_path, encoding="utf-8") as f:
        stage_data = json.load(f)
        wave_data = get_wave_data(
            stage_data, key, log=False)
        enemy_list, elite_enemy_list, sp_count, elite_sp_count, all_possible_enemy_count, all_possible_elite_enemy_count = itemgetter(
            "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "all_possible_enemy_count", "all_possible_elite_enemy_count")(wave_data)
        extra_info = extra_info_list[key]
        sp_enemy = extra_info['sp_enemy']
        if sp_enemy is None and sp_count is not None:
            sp_enemy = {
                "normal": ' / '.join([str(i) for i in sp_count]),
                "elite": ' / '.join([str(i) for i in elite_sp_count]) if elite_sp_count is not None else None,
                "fixed": len(sp_count) == len(all_possible_enemy_count)
            }
        if sp_enemy is not None:
            if sp_enemy['normal'] == sp_enemy['elite']:
                sp_enemy['elite'] = None
        # print(sp_enemy)
        # normal_runes = parse_runes(
        #     stage_data['runes'], 'normal') if stage_data['runes'] else None
        # normal_runes = normal_runes['runes'] if normal_runes and 'runes' in normal_runes else None
        elite_runes = extra_info['elite_mods'],
        if elite_runes[0] is None:
            runes_data = parse_runes(
                stage_data['runes'], 'elite') if stage_data['runes'] else None
            if runes_data:
                # pp.pprint(runes_data['other_runes'])
                pass
        sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
        sp_terrain = sp_tiles if 'rogue3' in key or 'rogue4' in key else extra_info[
            'sp_terrain']
        if sp_terrain is not None and len(sp_terrain) == 0:
            sp_terrain = None

        # elite_mods = extra_info['elite_mods']
        # new_mods = []
        # if elite_mods:
        #     for effect in elite_mods:
        #         new_effect = {}
        #         new_effect['targets'] = effect['targets']
        #         mods = []
        #         for statKey in effect['mods']:
        #             if statKey == "special":
        #                 new_effect['special'] = effect['mods'][statKey]
        #             elif 'fixed' in statKey:
        #                 mods.append(
        #                     {"key": statKey, "value": effect['mods'][statKey], "mode": "add"})
        #             elif "_" in statKey:
        #                 print(statKey)
        #             else:
        #                 mods.append(
        #                     {"key": statKey, "value": effect['mods'][statKey], "mode": "mul"})
        #         if len(mods) > 0:
        #             new_effect['mods'] = mods
        #         new_mods.append(new_effect)
        # if len(new_mods) == 0:
        #     new_mods = None
    trimmed_stage_info = {
        "levelId": extra_info['levelId'],
        "code": extra_info['code'],
        "name_zh": extra_info['name_zh'],
        "name_ja": extra_info['name_ja'],
        "name_en": extra_info['name_en'],
        "category": extra_info['category'],
        "floors": extra_info['floors'],
        "addInfo_zh": extra_info['addInfo_zh'],
        "addInfo_ja": extra_info['addInfo_ja'],
        "addInfo_en": extra_info['addInfo_en'],
        "eliteDesc_zh": extra_info['eliteDesc_zh'],
        "eliteDesc_ja": extra_info['eliteDesc_ja'],
        "eliteDesc_en": extra_info['eliteDesc_en'],
        "normal_mods": extra_info['normal_mods'],
        "elite_mods": new_mods,
        "all_possible_enemy_count": all_possible_enemy_count if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['all_possible_enemy_count'],
        "sp_count": sp_count,
        "all_possible_elite_enemy_count": all_possible_elite_enemy_count if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['all_possible_elite_enemy_count'],
        "elite_sp_count": elite_sp_count,
        "sp_enemy": extra_info['sp_enemy'],
        "sp_terrain": sp_terrain,
        "enemy_list": enemy_list if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['enemy_list'],
        "elite_enemy_list": elite_enemy_list if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['elite_enemy_list']
    }

    data[key] = trimmed_stage_info

# ? for adding new stages
# for stage in stages_list:
#     key = stage['levelId']
#     if not stage['levelId'] in extra_info_list:
#         if 'rogue1' in key:
#             folder = "ro1"
#         elif 'rogue2' in key:
#             folder = "ro2"
#         elif 'rogue3' in key:
#             folder = "ro3"
#         else:
#             folder = "ro4"

#         stage_data_path = os.path.join(
#             script_dir,
#             f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{key}.json",
#         )
#         with open(stage_data_path, encoding="utf-8") as f:
#             stage_data = json.load(f)
#             wave_data = get_wave_data(stage_data, key, log=True)
#             print(wave_data)
#             enemy_list, elite_enemy_list, sp_count, elite_sp_count, all_possible_enemy_count,all_possible_elite_enemy_count = itemgetter(
#                 "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "all_possible_enemy_count","all_possible_elite_enemy_count")(wave_data)
#             sp_enemy = {
#                 "normal": ' / '.join([str(i) for i in sp_count]),
#                 "elite": ' / '.join([str(i) for i in elite_sp_count]) if elite_sp_count is not None else None,
#                 "fixed": len(sp_count) == len(all_possible_enemy_count)
#             } if sp_count is not None else None
#             if sp_enemy is not None:
#                 if sp_enemy['normal'] == sp_enemy['elite']:
#                     sp_enemy['elite'] = None
#             # normal_runes = parse_runes(
#             #             stage_data['runes'], 'normal') if stage_data['runes'] else None
#             # normal_runes = normal_runes['runes'] if normal_runes and 'runes' in normal_runes else None
#             runes_data = parse_runes(
#                 stage_data['runes'],'elite') if stage_data['runes'] else None
#             runes = runes_data['runes'] if runes_data else None
#             sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
#             sp_terrain = sp_tiles if 'rogue3' in key or 'rogue4' in key else None
#             if sp_terrain is not None and len(sp_terrain) == 0:
#                 sp_terrain = None
#             trimmed_stage_info = {
#                 "levelId": stage['levelId'],
#                 "code": stage['code'],
#                 "name_zh": stage['name_zh'],
#                 "name_ja": stage['name_ja'],
#                 "name_en": stage['name_en'],
#                 "category": stage['category'],
#                 "floors": stage['floors'],
#                 "addInfo_zh": stage['addInfo_zh'],
#                 "addInfo_ja": stage['addInfo_ja'],
#                 "addInfo_en": stage['addInfo_en'],
#                 "eliteDesc_zh": stage['eliteDesc_zh'],
#                 "eliteDesc_ja": stage['eliteDesc_ja'],
#                 "eliteDesc_en": stage['eliteDesc_en'],
#                 "normal_mods": None,
#                 "elite_mods": runes,
#                  "all_possible_enemy_count": all_possible_enemy_count,
#     "sp_count": sp_count,
#     "all_possible_elite_enemy_count":all_possible_elite_enemy_count,
#     "elite_sp_count": elite_sp_count,
#     "sp_enemy": sp_enemy,
#     "sp_terrain": sp_terrain,
#     "enemy_list": enemy_list,
#     "elite_enemy_list": elite_enemy_list
#             }
#             data[stage['levelId']] = trimmed_stage_info
# data = extra_info_list | data

with open("is_stages_extrainfo.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
