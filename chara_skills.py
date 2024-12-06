import json
import os
import re


def replace_key(string):
    string = string.replace("ABILITY_RANGE_FORWARD_EXTEND",
                            "ability_range_forward_extend")
    string = string.replace("HP_RECOVERY_PER_SEC_BY_MAX_HP_RATIO",
                            "hp_recovery_per_sec_by_max_hp_ratio")
    string = string.replace("HP_RECOVERY_PER_SEC",
                            "hp_recovery_per_sec")
    return string


def replace_substrings(text, blackboard):
    if text is None:
        return text
    # Define the regular expression pattern
    pattern = r'\{(.*?)\}'

    # Define a function to replace the matched substrings
    def replace_match(match):
        # Extract the substring inside the curly braces
        value = match.group(1)
        key = value
        if ":" in key:
            key = key.split(":")[0]
        key = key.replace("-","")
        board = next(
            (n for n in blackboard if n['key'] == key), None)
        if board:
            if '%' in value:
                value = abs(round(board['value'] * 100))
                if board['key'] == 'damage_scale' and board['value'] > 1:
                    value -= 100
                value = f"{value}%"
            else:
                if isinstance(board['value'], float) and f"{board['value']}"[-1] != "0":
                    value = f"{abs(board['value'])}"
                else:
                    value = f"{abs(round(board['value']))}"
            return value
        else:
            print('unchanged key',value)
            return "{"+value+"}"
        # Replace the matched substring with the value

    # Replace the substrings using the regular expression and the replace_match function
    text = replace_key(text)
    result = re.sub(pattern, replace_match, text)
    result = re.sub(r'<([A-Z][^>]*)>', r'&lt;\1&gt;', result)
    
    return result.replace("<$ba", "<ba")


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

with open('chara_skills.json', encoding='utf-8') as f:
    chara_skills = json.load(f)


# append new skills to skill tags json
    new_skill_list = [skill for skill in dict.keys(
        cn_skill_table) if skill not in set(dict.keys(chara_skills))]
    return_dict = {}
    for skill in new_skill_list:
        in_global = skill in en_skill_table
        if 'sktok' in skill or 'skcom_withdraw' in skill:
            continue
        chara_list = []
        for id in cn_char_table:
            for skill_dict in cn_char_table[id]["skills"]:
                if skill_dict["skillId"] == skill:
                    chara_list.append(cn_char_table[id]['name'])
        levels = cn_skill_table[skill]['levels']

        if len(levels) > 6:
            l7 = levels[6]
            m1 = None
            m2 = None
            m3 = None
            if len(levels) > 8:
                m1 = levels[7]
                m2 = levels[8]
                m3 = levels[9]
            levels = [l7, m1, m2, m3]
            levels = [i for i in levels if i is not None]
        return_levels = []
        index = 5
        for level in levels:

            index += 1
            description_zh = replace_substrings(
                cn_skill_table[skill]['levels'][index]['description'], cn_skill_table[skill]['levels'][index]['blackboard'])
            description_ja = replace_substrings(
                jp_skill_table[skill]['levels'][index]['description'], cn_skill_table[skill]['levels'][index]['blackboard']) if in_global else ""
            description_en = replace_substrings(
                en_skill_table[skill]['levels'][index]['description'], cn_skill_table[skill]['levels'][index]['blackboard']) if in_global else ""
            data = {
                "rangeId": level['rangeId'],
                "description_zh": description_zh,
                "description_ja": description_ja,
                "description_en": description_en,
                "spData": level['spData'],
                "duration": level['duration'],
                "blackboard": level['blackboard']
            }
            return_levels.append(data)

        blackboard = levels[-1]['blackboard']
        return_dict[skill] = {"name_zh": cn_skill_table[skill]['levels'][0]['name'],
                              "name_ja": jp_skill_table[skill]['levels'][0]['name'] if in_global else "",
                              "name_en": en_skill_table[skill]['levels'][0]['name'] if in_global else "",
                              "chara_list": chara_list,
                              "skillType": cn_skill_table[skill]['levels'][0]['skillType'],
                              "durationType": cn_skill_table[skill]['levels'][0]['durationType'],
                              "spType": cn_skill_table[skill]['levels'][0]['spData']['spType'],
                              "levels": return_levels,
                              "tags": [], "blackboard": blackboard}
    return_dict = chara_skills | return_dict

with open('chara_skills.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)
