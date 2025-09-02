import json
import os
from operator import itemgetter
from stages import get_trimmed_stage_data

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_crisisv2_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/crisis_v2_table.json"
)
en_crisisv2_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/crisis_v2_table.json"
)
jp_crisisv2_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/crisis_v2_table.json"
)

with open(cn_crisisv2_path, encoding="utf-8") as f:
    cn_crisisv2_table = json.load(f)
with open(en_crisisv2_path, encoding="utf-8") as f:
    en_crisisv2_table = json.load(f)
with open(jp_crisisv2_path, encoding="utf-8") as f:
    jp_crisisv2_table = json.load(f)


def get_crisis_runes(runes):
    return


def get_crisis_stage_info():
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
                extrainfo = {}
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
                trimmed_stage_info = get_trimmed_stage_data(
                    stage_data, meta_info, extrainfo)

                # handle runes
                trimmed_stage_info['systems']['contracts'] = {
                    "fixedRuneSeriesName": {
                        "zh": stage_info['fixedRuneSeriesName'],
                        "ja": jp_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['fixedRuneSeriesName'] if TOPIC_IN_GLOBAL else None,
                        "en": en_crisisv2_table['recalRuneData']['seasons'][season]['stages'][stage_id]['fixedRuneSeriesName'] if TOPIC_IN_GLOBAL else None,},
                    "runes": get_crisis_runes(stage_info['runes'])}

                data[stage_id] = trimmed_stage_info

    except Exception as e:
        pass

    for stage_id in data:
        write_path = os.path.join(
            script_dir, 'all_stage_data', stage_id+".json")
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(data[stage_id], f, ensure_ascii=False, indent=1)
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_crisis_stage_info()
