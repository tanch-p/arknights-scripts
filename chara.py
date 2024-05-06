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

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)

with open('chara_skills.json', encoding='utf-8') as f:
    chara_skills = json.load(f)
with open('chara_talents.json', encoding='utf-8') as f:
    chara_talents = json.load(f)
with open('uniequip.json', encoding='utf-8') as f:
    uniequip_dict = json.load(f)
data = []

filtered_cn_char_table = {key: cn_char_table[key] for key in cn_char_table.keys(
) if not "token" in key and not "trap" in key}


for id in filtered_cn_char_table:
    character_dict = filtered_cn_char_table[id]
    skills = []
    talents = []
    for skill in character_dict['skills']:
        blackboard = chara_skills[skill['skillId']
                                  ]['blackboard'] if skill['skillId'] in chara_skills else []
        skills.append({"skillId": skill['skillId'], 
                       "name_zh": chara_skills[skill['skillId']]['name_zh'],
                       "name_ja": chara_skills[skill['skillId']]['name_ja'],
                       "name_en": chara_skills[skill['skillId']]['name_en'],
                       "skillType": chara_skills[skill['skillId']]['skillType'],
                       "durationType": chara_skills[skill['skillId']]['durationType'],
                       "levels": chara_skills[skill['skillId']]['levels'], 
                       "tags": chara_skills[skill['skillId']]['tags'] if skill['skillId'] in chara_skills else [], 
                       "blackboard": blackboard})
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
            talent_holder['tags'] = chara_talents[id]['talents'][talent_index]['tags'] if id in chara_talents else []
            talent_holder['blackboard'] = chara_talents[id]['talents'][talent_index]['blackboard'] if id in chara_talents else []
            talents.append(talent_holder)

    uniequip_list = []
    for equip_id in uniequip_dict:
        if uniequip_dict[equip_id]['charId'] == id:
            uniequip_list.append(uniequip_dict[equip_id])

    return_dict = {"id": id, "appellation": character_dict['appellation'], "name_zh": character_dict['name'], "name_en": "", "name_ja": "",
                   "nationId": character_dict['nationId'], "groupId": character_dict['groupId'], "teamId": character_dict['teamId'], "tagList": [],
                   "isSpChar": character_dict['isSpChar'], "rarity": character_dict['rarity'],
                   "profession": character_dict['profession'], "subProfessionId": character_dict['subProfessionId'],
                   "skills": skills, "talents": talents, "tagList": [], 'uniequip': uniequip_list}
    if id in en_char_table:
        return_dict['name_ja'] = jp_char_table[id]['name']
        return_dict['name_en'] = en_char_table[id]['name']
    data.append(return_dict)

with open('characters.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# append new charas to char talent tags json
    new_chara_list = [id for id in dict.keys(
        filtered_cn_char_table) if id not in set(dict.keys(chara_talents))]
    return_dict = {}
    for id in new_chara_list:
        talents = []
        if filtered_cn_char_table[id]['talents']:
            for talent_index, talent in enumerate(filtered_cn_char_table[id]['talents']):
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder = {
                    "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                    "description_zh": maxed_talent["description"], "description_en": "", "description_ja": "", "tags": [], "blackboard": maxed_talent['blackboard']}
                if id in en_char_table:
                    talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["description_ja"] = jp_char_table[id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                    talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["description_en"] = en_char_table[id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                talents.append(talent_holder)
        return_dict[id] = {
            "appellation": filtered_cn_char_table[id]['appellation'], "talents": talents}
    return_dict = chara_talents | return_dict

with open('chara_talents.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)


# schema has to take care of the following requirements:
# can affect air? target ground? enemy types
# roguelike artifacts
# summons
# values with a range will always take minimum
# probability
# condition
