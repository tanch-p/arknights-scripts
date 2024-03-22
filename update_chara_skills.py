import json
import os

status_ailments = ["stun", "sluggish", "sleep",
                   "silence", "levitate", "cold",
                   "root", "tremble", "fragile", "berserk",
                   "dying", "buffres", "dt.element",
                   "shield", "strong", "magicfragile",
                   "invisible", "camou", "protect",
                   "dt.apoptosis2", "steal", "weightless",
                   "charged", "barrier", "overdrive", "inspire"]

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
        if 'sktok' in skill:
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
        blackboard = levels[-1]['blackboard']
        skill_ailments = [
            ailment for ailment in status_ailments if cn_skill_table[skill]["levels"][0]["description"] and ailment in cn_skill_table[skill]["levels"][0]["description"]]
        return_dict[skill] = {"chara_list": chara_list, "levels": levels, "blackboard": blackboard + [
            {"key": ailment, "value": None, "prob": 1, "target_air": False, "condition": None} for ailment in skill_ailments]}
    return_dict = chara_skills | return_dict

with open('chara_skills.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)