import json
import os
import re
import math

buffs_list = [
    "berserk", "dying", "buffres",
    "shield", "strong", "invisible",
    "camou", "protect", "weightless",
    "charged", "barrier", "overdrive",
    "inspire"]
debuffs_list = ["stun", "sluggish", "sleep",
                "silence", "levitate", "cold",
                "magicfragile", "root", "tremble",
                "fragile", "dt.apoptosis2", "dt.burning2",
                "steal", "weightless"]
target_air_professions = ['']

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


def replace_substrings(text, blackboard):
    # Define the regular expression pattern
    pattern = r'\{(.*?)\}'

    # Define a function to replace the matched substrings
    def replace_match(match):
        # Extract the substring inside the curly braces
        matched_str = match.group(1)
        value = matched_str
        if ":" in matched_str:
            board = next(
                (n for n in blackboard if n['key'] in matched_str), None)
        else:
            board = next(
                (n for n in blackboard if n['key'] == matched_str), None)
        if board:
            if '%' in matched_str:
                value = f"{math.floor(board['value'] * 100)}%"
            else:
                if isinstance(board['value'], float) and f"{board['value']}"[-1] != "0":
                    value = f"{board['value']}"
                else:
                    value = f"{math.floor(board['value'])}"

        # Replace the matched substring with the value
        return value

    # Replace the substrings using the regular expression and the replace_match function
    result = re.sub(pattern, replace_match, text)

    return result


return_dict = {}
for skill in chara_skills:
    in_global = skill in en_skill_table
    if 'sktok' in skill or 'skcom_withdraw' in skill:
        continue
    levels = []

    index = 5
    for level in chara_skills[skill]['levels']:

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
        levels.append(data)

    return_dict[skill] = {"name_zh": cn_skill_table[skill]['levels'][0]['name'],
                          "name_ja": jp_skill_table[skill]['levels'][0]['name'] if in_global else "",
                          "name_en": en_skill_table[skill]['levels'][0]['name'] if in_global else "",
                          "chara_list": chara_skills[skill]['chara_list'], "skillType": cn_skill_table[skill]['levels'][0]['skillType'],
                          "target_air": None, 
                          "durationType": cn_skill_table[skill]['levels'][0]['durationType'], "levels": levels,
                          "tags": chara_skills[skill]['tags'], "blackboard": chara_skills[skill]['blackboard']}
print(len(return_dict))
print(len(chara_skills))
with open('chara_skills_temp.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)
