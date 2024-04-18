import json
import os

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

# append new skills to skill tags json
    new_skill_list = [skill for skill in dict.keys(
        cn_skill_table) if skill not in set(dict.keys(chara_skills))]
    return_dict = {}
    for skill in new_skill_list:
        if 'sktok' in skill or 'skcom' in skill:
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
        debuffs = [
            key for key in debuffs_list if cn_skill_table[skill]["levels"][0]["description"] and key in cn_skill_table[skill]["levels"][0]["description"]]
        buffs = [
            key for key in buffs_list if cn_skill_table[skill]["levels"][0]["description"] and key in cn_skill_table[skill]["levels"][0]["description"]]

        # for key in debuffs:
        #     in_bb = False
        #     for item in blackboard:
        #         if item['key'] == key:
        #             in_bb = True
        #             item = {
        #                 "key": key, "value": item['value'], "prob": 1, "target_air": False, "condition": None}
        #     if not in_bb:
        #         blackboard.append(
        #             {"key": key, "value": None, "prob": 1, "target_air": False, "condition": None})
        # for key in buffs:
        #     in_bb = False
        #     for item in blackboard:
        #         if item['key'] == key:
        #             in_bb = True
        #             item = {
        #                 "key": key, "value": item['value'], "prob": 1, "target_air": False, "condition": None}
        #     if not in_bb:
        #         blackboard.append(
        #             {"key": key, "value": None, "prob": 1, "condition": None})
        return_dict[skill] = {"chara_list": chara_list,
                              "levels": levels, "tags":[], "blackboard": blackboard}
        # if skill == 'skchr_mm_1':
        #     print(debuffs)
    return_dict = chara_skills | return_dict

with open('chara_skills.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)
