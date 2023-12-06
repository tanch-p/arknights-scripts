import json
import os
import sqlite3

status_ailments = ["stun", "sluggish", "sleep",
                   "silence", "levitate", "cold",
                   "root", "fragile", "berserk",
                   "dying", "buffres", "dt.element",
                   "shield", "strong", "magicfragile",
                   "invisible", "camou", "protect",
                   "dt.apoptosis2", "steal", "weightless",
                   "charged", "barrier", "overdrive", "inspire"]

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/skill_table.json")
cn_uniequip_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/uniequip_table.json")
cn_battle_equip_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/battle_equip_table.json")
en_char_table_path = os.path.join(
    script_dir, "en_US/gamedata/excel/character_table.json")
en_skill_table_path = os.path.join(
    script_dir, "en_US/gamedata/excel/skill_table.json")
jp_char_table_path = os.path.join(
    script_dir, "ja_JP/gamedata/excel/character_table.json")
jp_skill_table_path = os.path.join(
    script_dir, "ja_JP/gamedata/excel/skill_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(cn_uniequip_path, encoding='utf-8') as f:
    cn_uniequip_table = json.load(f)
with open(cn_battle_equip_path, encoding='utf-8') as f:
    cn_battle_equip_table = json.load(f)
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
with open('character_talent_tags.json', encoding='utf-8') as f:
    chara_talents = json.load(f)

data = []

filtered_cn_char_table = {key: cn_char_table[key] for key in cn_char_table.keys(
) if not "token" in key and not "trap" in key}


for id in filtered_cn_char_table:
    character_dict = filtered_cn_char_table[id]
    skills = []
    talents = []
    for skill in character_dict['skills']:
        blackboard = chara_skills[skill['skillId']]['blackboard']
        skills.append({"skillId": skill['skillId'], "blackboard": blackboard})
    if character_dict['talents']:
        for talent_index, talent in enumerate(character_dict['talents']):
            max_candidate_index = len(talent['candidates'])-1
            maxed_talent = talent['candidates'][max_candidate_index]
            talent_holder = {
                "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                "description_zh": maxed_talent["description"], "description_en": "", "description_ja": ""}
            if id in en_char_table:
                talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["description_en"] = en_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"]
                talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["description_ja"] = jp_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"]
            talent_holder['blackboard'] = chara_talents[id]['talents'][talent_index]['blackboard']
            talents.append(talent_holder)

    uniequip_list = []
    if id in cn_uniequip_table['charEquip']:
        uniequip_list = cn_uniequip_table['charEquip'][id]

    return_dict = {"id": id, "appellation": character_dict['appellation'], "name_zh": character_dict['name'], "name_en": "", "name_ja": "",
                   "nationId": character_dict['nationId'], "groupId": character_dict['groupId'], "tagList": [],
                   "isSpChar": character_dict['isSpChar'], "rarity": character_dict['rarity'],
                   "profession": character_dict['profession'], "subProfessionId": character_dict['subProfessionId'],
                   "skills": skills, "talents": talents, "tagList": [], "uniequip": uniequip_list}
    if id in en_char_table:
        return_dict['name_en'] = en_char_table[id]['name']
        return_dict['name_ja'] = jp_char_table[id]['name']
    data.append(return_dict)

with open('characters.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# append new charas to char talent tags json
    new_chara_list = [id for id in dict.keys(
        filtered_cn_char_table) if id not in set(dict.keys({}))]
    return_dict = {}
    for id in new_chara_list:
        talents = []
        if filtered_cn_char_table[id]['talents']:
            for talent_index, talent in enumerate(filtered_cn_char_table[id]['talents']):
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder = {
                    "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                    "description_zh": maxed_talent["description"], "description_en": "", "description_ja": ""}
                if id in en_char_table:
                    talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["description_en"] = en_char_table[id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                    talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["description_ja"] = jp_char_table[id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                skill_ailments = [
                    ailment for ailment in status_ailments if ailment in maxed_talent["description"]]
                talent_holder['blackboard'] = [
                    {"key": ailment, "value": None, "prob": 1, "target_air": False, } for ailment in skill_ailments]
                talents.append(talent_holder)

        return_dict[id] = {
            "appellation": filtered_cn_char_table[id]['appellation'], "talents": talents}

with open('character_talent_tags.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)

# append new skills to skill tags json
    new_skill_list = [skill for skill in dict.keys(
        cn_skill_table) if skill not in set(dict.keys({}))]
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
        skill_ailments = [
            ailment for ailment in status_ailments if cn_skill_table[skill]["levels"][0]["description"] and ailment in cn_skill_table[skill]["levels"][0]["description"]]
        return_dict[skill] = {"chara_list": chara_list, "blackboard": [
            {"key": ailment, "value": None, "prob": 1, "target_air": False, } for ailment in skill_ailments], "levels": levels}

with open('chara_skills.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)


# schema has to take care of the following requirements:
# can affect air? target ground? enemy types
# roguelike artifacts
# summons
