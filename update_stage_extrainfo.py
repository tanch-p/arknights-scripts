from operator import itemgetter
from runes import get_runes
from tiles import get_special_tiles
from waves_new import get_wave_spawns_data
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


def update_current_stages():
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
            wave_data = get_wave_spawns_data(stage_data, key, log=True)
            enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
                "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
            extra_info = extra_info_list[key]
            sp_enemy = extra_info['sp_enemy']
            if sp_enemy is None and sp_count is not None:
                sp_enemy = {
                    "normal": ' / '.join([str(i) for i in sp_count]),
                    "elite": ' / '.join([str(i) for i in elite_sp_count]) if elite_sp_count is not None else None,
                }
            if sp_enemy is not None:
                if sp_enemy['normal'] == sp_enemy['elite']:
                    sp_enemy['elite'] = None
            sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
            sp_terrain = sp_tiles if not key in ['level_rogue2_b-10'] else extra_info[
                'sp_terrain']
            if sp_terrain is not None and len(sp_terrain) == 0:
                sp_terrain = None

            runes_data = get_runes(
                stage_data['runes']) if stage_data['runes'] else None
            all_mods = None
            elite_mods = None
            normal_mods = None
            if runes_data:
                all_mods, elite_mods, normal_mods = itemgetter(
                    'all_mods', 'elite_mods', 'normal_mods')((runes_data))
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
                "all_mods": extra_info['all_mods'] or all_mods, #all mods is just for reference
                "normal_mods": extra_info['normal_mods'],
                "elite_mods": extra_info['elite_mods'],
                "enemy_counts": enemy_counts if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['enemy_counts'],
                "sp_count": sp_count,
                "elite_enemy_counts": elite_enemy_counts if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['elite_enemy_counts'],
                "elite_sp_count": elite_sp_count,
                "sp_enemy": extra_info['sp_enemy'],
                "sp_terrain": sp_terrain,
                "enemy_list": enemy_list if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['enemy_list'],
                "elite_enemy_list": elite_enemy_list if not extra_info['levelId'] in STAGES_TO_IGNORE else extra_info['elite_enemy_list']
            }

        data[key] = trimmed_stage_info

    with open("is_stages_extrainfo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_new_ro_stages():
    data = {}
    for stage in stages_list:
        key = stage['levelId']
        if not stage['levelId'] in extra_info_list:
            if 'rogue1' in key:
                folder = "ro1"
            elif 'rogue2' in key:
                folder = "ro2"
            elif 'rogue3' in key:
                folder = "ro3"
            elif 'rogue4' in key:
                folder = "ro4"
            elif 'rogue5' in key:
                folder = "ro5"

            stage_data_path = os.path.join(
                script_dir,
                f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{key}.json",
            )
            with open(stage_data_path, encoding="utf-8") as f:
                stage_data = json.load(f)
                wave_data = get_wave_spawns_data(stage_data, key, log=True)
                enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
                    "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
                sp_enemy = {
                    "normal": ' / '.join([str(i) for i in sp_count]),
                    "elite": ' / '.join([str(i) for i in elite_sp_count]) if elite_sp_count is not None else None,
                } if sp_count is not None else None
                if sp_enemy is not None:
                    if sp_enemy['normal'] == sp_enemy['elite']:
                        sp_enemy['elite'] = None
                sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
                sp_terrain = sp_tiles
                if sp_terrain is not None and len(sp_terrain) == 0:
                    sp_terrain = None

                runes_data = get_runes(
                    stage_data['runes']) if stage_data['runes'] else None
                all_mods = None
                elite_mods = None
                normal_mods = None
                if runes_data:
                    all_mods, elite_mods, normal_mods = itemgetter(
                        'all_mods', 'elite_mods', 'normal_mods')((runes_data))

                trimmed_stage_info = {
                    "levelId": stage['levelId'],
                    "code": stage['code'],
                    "name_zh": stage['name_zh'],
                    "name_ja": stage['name_ja'],
                    "name_en": stage['name_en'],
                    "category": stage['category'],
                    "floors": stage['floors'],
                    "addInfo_zh": stage['addInfo_zh'],
                    "addInfo_ja": stage['addInfo_ja'],
                    "addInfo_en": stage['addInfo_en'],
                    "eliteDesc_zh": stage['eliteDesc_zh'],
                    "eliteDesc_ja": stage['eliteDesc_ja'],
                    "eliteDesc_en": stage['eliteDesc_en'],
                    "all_mods": all_mods,
                    "normal_mods": normal_mods,
                    "elite_mods": elite_mods,
                    "enemy_counts": enemy_counts ,
                    "sp_count": sp_count,
                    "elite_enemy_counts": elite_enemy_counts,
                    "elite_sp_count": elite_sp_count,
                    "sp_enemy": sp_enemy,
                    "sp_terrain": sp_terrain,
                    "enemy_list": enemy_list,
                    "elite_enemy_list": elite_enemy_list
                }
            data[stage['levelId']] = trimmed_stage_info
    data = extra_info_list | data

    with open("is_stages_extrainfo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_new_event_stages():
    stages_list=[{
        
    }]
    data = {}
    for stage in stages_list:
        key = stage['levelId']
        if not stage['levelId'] in extra_info_list:
            if 'rogue1' in key:
                folder = "ro1"
            elif 'rogue2' in key:
                folder = "ro2"
            elif 'rogue3' in key:
                folder = "ro3"
            elif 'rogue4' in key:
                folder = "ro4"
            elif 'rogue5' in key:
                folder = "ro5"

            stage_data_path = os.path.join(
                script_dir,
                f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{key}.json",
            )
            with open(stage_data_path, encoding="utf-8") as f:
                stage_data = json.load(f)
                wave_data = get_wave_spawns_data(stage_data, key, log=True)
                enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
                    "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
                sp_enemy = {
                    "normal": ' / '.join([str(i) for i in sp_count]),
                    "elite": ' / '.join([str(i) for i in elite_sp_count]) if elite_sp_count is not None else None,
                } if sp_count is not None else None
                if sp_enemy is not None:
                    if sp_enemy['normal'] == sp_enemy['elite']:
                        sp_enemy['elite'] = None
                sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
                sp_terrain = sp_tiles
                if sp_terrain is not None and len(sp_terrain) == 0:
                    sp_terrain = None

                runes_data = get_runes(
                    stage_data['runes']) if stage_data['runes'] else None
                all_mods = None
                elite_mods = None
                normal_mods = None
                if runes_data:
                    all_mods, elite_mods, normal_mods = itemgetter(
                        'all_mods', 'elite_mods', 'normal_mods')((runes_data))

                trimmed_stage_info = {
                    "levelId": stage['levelId'],
                    "code": stage['code'],
                    "name_zh": stage['name_zh'],
                    "name_ja": stage['name_ja'],
                    "name_en": stage['name_en'],
                    "category": stage['category'],
                    "floors": stage['floors'],
                    "addInfo_zh": stage['addInfo_zh'],
                    "addInfo_ja": stage['addInfo_ja'],
                    "addInfo_en": stage['addInfo_en'],
                    "eliteDesc_zh": stage['eliteDesc_zh'],
                    "eliteDesc_ja": stage['eliteDesc_ja'],
                    "eliteDesc_en": stage['eliteDesc_en'],
                    "all_mods": all_mods,
                    "normal_mods": normal_mods,
                    "elite_mods": elite_mods,
                    "enemy_counts": enemy_counts ,
                    "sp_count": sp_count,
                    "elite_enemy_counts": elite_enemy_counts,
                    "elite_sp_count": elite_sp_count,
                    "sp_enemy": sp_enemy,
                    "sp_terrain": sp_terrain,
                    "enemy_list": enemy_list,
                    "elite_enemy_list": elite_enemy_list
                }
            data[stage['levelId']] = trimmed_stage_info
    data = extra_info_list | data

    with open("is_stages_extrainfo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # update_current_stages()
    # add_new_event_stages()
    pass

if __name__ == "__main__":
    main()
