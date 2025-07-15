import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
en_skill_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/skill_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")
jp_skill_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/skill_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(en_skill_table_path, encoding='utf-8') as f:
    en_skill_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)
with open(jp_skill_table_path, encoding='utf-8') as f:
    jp_skill_table = json.load(f)

keys_to_parse = ['sktok_winfire','sktok_dhtl_1','sktok_dhtl_2','sktok_dhsb','sktok_dhdcr','sktok_spblls','sktok_aegiret_1','sktok_fttreant_1','sktok_cjgtow_1','sktok_cjbtow_1']

data = {}
for key in keys_to_parse:
    skill = cn_skill_table[key]
    in_global = key in en_skill_table

    levels = []
    for level in skill['levels']:
        levels.append({
            "rangeId": level['rangeId'],
            "spData": level['spData'],
            "duration": level['duration'],
            "blackboard": level['blackboard']
        })

    data[key] = {
        "name_zh": skill['levels'][0]['name'],
        "name_ja": jp_skill_table[key]['levels'][0]['name'] if in_global else "",
        "name_en": en_skill_table[key]['levels'][0]['name'] if in_global else "",
        "desc_zh": skill['levels'][0]['description'],
        "desc_ja": jp_skill_table[key]['levels'][0]['description'] if in_global else "",
        "desc_en": en_skill_table[key]['levels'][0]['description'] if in_global else "",
        "skillType": skill['levels'][0]['skillType'],
        "durationType": skill['levels'][0]['durationType'],
        "spType": skill['levels'][0]['spData']['spType'],
        "levels":levels
    }

with open('system_token_skills.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
