import json
import os
from operator import itemgetter
from stages import get_trimmed_stage_data
from tiles import get_special_tiles
from waves_new import get_wave_spawns_data
from runes import get_crisis_runes
from chara_skills import replace_substrings

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_crisisv2_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/crisis_v2_table.json"
)
en_crisisv2_path = os.path.join(
    script_dir, "global_data/en/gamedata/excel/crisis_v2_table.json"
)
jp_crisisv2_path = os.path.join(
    script_dir, "global_data/jp/gamedata/excel/crisis_v2_table.json"
)

with open(cn_crisisv2_path, encoding="utf-8") as f:
    cn_crisisv2_table = json.load(f)
with open(en_crisisv2_path, encoding="utf-8") as f:
    en_crisisv2_table = json.load(f)
with open(jp_crisisv2_path, encoding="utf-8") as f:
    jp_crisisv2_table = json.load(f)


def update_crisis_runes():
    with open("crisis_runes.json", encoding="utf-8") as f:
        crisis_runes_table = json.load(f)

    return_dict = {}
    for season in cn_crisisv2_table['recalRuneData']['seasons']:
        season_data = cn_crisisv2_table['recalRuneData']['seasons'][season]
        for stage_id in season_data['stages']:
            if not stage_id in crisis_runes_table:
                return_dict[stage_id] = {}
            else:
                continue
            stage_info = season_data['stages'][stage_id]
            for rune_type in stage_info['runes']:
                rune_data = stage_info['runes'][rune_type]
                runes = [{"key": rune['key'], "blackboard": rune['blackboard']}
                         for rune in rune_data['packedRune']['runes']]
                mods = get_crisis_runes(runes)
                return_dict[stage_id][rune_data['runeId']] = {
                    "desc": rune_data['packedRune']['description'], "mods": mods, "runes": runes}

    with open("crisis_runes.json", "w", encoding="utf-8") as f:
        json.dump(crisis_runes_table | return_dict,
                  f, ensure_ascii=False, indent=2)
    return


def get_crisis_stage_info():
    with open("crisis_runes.json", encoding="utf-8") as f:
        crisis_runes_table = json.load(f)
    data = {}
    try:
        for season in cn_crisisv2_table['recalRuneData']['seasons']:
            TOPIC_IN_GLOBAL = 'recalRuneData' in en_crisisv2_table and season in en_crisisv2_table[
                'recalRuneData']['seasons']
            season_data = cn_crisisv2_table['recalRuneData']['seasons'][season]
            for stage_id in season_data['stages']:
                stage_info = season_data['stages'][stage_id]

                file_path = stage_info['levelId'].lower()
                stage_data_path = os.path.join(
                    script_dir,
                    f"cn_data/zh_CN/gamedata/levels/{file_path}.json",
                )
                print(stage_id, stage_info['levelId'].lower())
                try:
                    with open(stage_data_path, encoding="utf-8") as f:
                        stage_data = json.load(f)
                except FileNotFoundError as e:
                    print(f"{file_path} not found")
                if not stage_data:
                    continue
                meta_info = {
                    "id": stage_id,
                    "levelId": stage_id,
                    "code": stage_info['levelCode'],
                    "name_zh":  stage_info['levelName'],
                    "name_ja":  jp_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['levelName'] if TOPIC_IN_GLOBAL else None,
                    "name_en":  en_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['levelName'] if TOPIC_IN_GLOBAL else None,
                    "description_zh": stage_info['levelDesc'].replace("\\n", "\n") if stage_info['levelDesc'] else None,
                    "description_ja": jp_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['levelDesc'].replace("\\n", "\n")
                    if TOPIC_IN_GLOBAL and stage_info['description']
                    else None,
                    "description_en": en_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['levelDesc'].replace("\\n", "\n")
                    if TOPIC_IN_GLOBAL and stage_info['description']
                    else None,
                }
                wave_data = get_wave_spawns_data(
                    stage_data, stage_id, log=False)
                enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
                    "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
                sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
                sp_terrain = sp_tiles
                if sp_terrain is not None and len(sp_terrain) == 0:
                    sp_terrain = None
                extrainfo = {
                    stage_id: {
                        "enemy_counts": enemy_counts,
                        "elite_enemy_counts": elite_enemy_counts,
                        "sp_terrain": sp_terrain,
                        "enemy_list": enemy_list,
                        "elite_enemy_list": elite_enemy_list
                    }}
                trimmed_stage_info = get_trimmed_stage_data(
                    stage_data, meta_info, extrainfo)

                # handle runes
                runes = []
                for rune_type in stage_info['runes']:
                    rune_data = stage_info['runes'][rune_type]
                    rune_blackboard = [rune['blackboard'] for rune in rune_data['packedRune']['runes']]
                    flat_board = [item for sublist in rune_blackboard for item in sublist]
                    runes.append(
                        {
                            "runeId": rune_data['runeId'],
                            "score": rune_data['score'],
                            "sortId": rune_data['sortId'],
                            "essential": rune_data['essential'],
                            "exclusiveGroupId": rune_data['exclusiveGroupId'],
                            "runeIcon": rune_data['runeIcon'],
                            "description": {
                                "zh": replace_substrings(rune_data['packedRune']['description'],flat_board),
                                "ja": replace_substrings(jp_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['runes'][rune_type]['packedRune']['description'],flat_board) if TOPIC_IN_GLOBAL else None,
                                "en": replace_substrings(en_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['runes'][rune_type]['packedRune']['description'],flat_board) if TOPIC_IN_GLOBAL else None
                            },
                            "mods": crisis_runes_table[stage_id][rune_data['runeId']]['mods']
                        }
                    )

                trimmed_stage_info['systems']['crisis'] = {
                    "fixedRuneSeriesName": {
                        "zh": stage_info['fixedRuneSeriesName'],
                        "ja": jp_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['fixedRuneSeriesName'] if TOPIC_IN_GLOBAL else None,
                        "en": en_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['fixedRuneSeriesName'] if TOPIC_IN_GLOBAL else None, },
                    "runes": runes}

                data[stage_id] = trimmed_stage_info

    except FileNotFoundError as e:
        pass

    for stage_id in data:
        write_path = os.path.join(
            script_dir, 'all_stage_data', stage_id+".json")
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(data[stage_id], f, ensure_ascii=False, indent=1)
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    update_crisis_runes()
    get_crisis_stage_info()
