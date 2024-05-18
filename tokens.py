import json
import os
from chara_skills import replace_substrings
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_skill_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/skill_table.json")
jp_skill_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/skill_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_skill_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/skill_table.json")
jp_skill_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/skill_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)
with open(en_skill_table_path, encoding='utf-8') as f:
    en_skill_table = json.load(f)
with open(jp_skill_table_path, encoding='utf-8') as f:
    jp_skill_table = json.load(f)

filtered_cn_char_table = {key: cn_char_table[key] for key in cn_char_table.keys(
) if not "token" in key and not "trap" in key}

tokens_list = []
for id in filtered_cn_char_table:
    chara_dict = filtered_cn_char_table[id]
    if chara_dict['displayTokenDict'] is not None:
        tokens =[key for key in chara_dict['displayTokenDict']]
        tokens_list += tokens

print(tokens_list)
data = {}
for id in tokens_list:
    in_global = id in en_char_table
    token_dict = cn_char_table[id]
    stats = {}
    stats['rangeId'] = token_dict['phases'][-1]['rangeId']
    stats['level'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['level']
    stats['hp'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["maxHp"]
    stats['atk'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["atk"]
    stats['def'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["def"]
    stats['res'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["magicResistance"]
    stats['cost'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["cost"]
    stats['blockCnt'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["blockCnt"]
    stats['aspd'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["baseAttackTime"]
    stats['respawnTime'] = token_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["respawnTime"]

    skills = []
    token_skills = [skill['skillId'] for skill in token_dict['skills'] if skill['skillId'] is not None ]
    token_skills = list(set(token_skills))
    if token_skills:
        token_skills.sort()
    for skillId in token_skills:
        skill = cn_skill_table[skillId]
        level = skill['levels'][-1]
        blackboard = level['blackboard']
        desc = cn_skill_table[skillId]['levels'][-1]['description']
        if desc:
            skills.append({"skillId": skillId,
                        "name_zh": cn_skill_table[skillId]['levels'][-1]['name'],
                        "name_ja":  jp_skill_table[skillId]['levels'][-1]['name'] if in_global else "",
                        "name_en":  en_skill_table[skillId]['levels'][-1]['name'] if in_global else "",
                        "iconId": skill['iconId'],
                        "rangeId" : level['rangeId'],
                        "desc_zh": replace_substrings(cn_skill_table[skillId]['levels'][-1]['description'],blackboard) if desc else "", 
                        "desc_ja": replace_substrings(jp_skill_table[skillId]['levels'][-1]['description'],blackboard) if in_global and desc  else "",
                        "desc_en": replace_substrings(en_skill_table[skillId]['levels'][-1]['description'],blackboard) if in_global and desc else "",
                        "skillType": level['skillType'],
                        "durationType": level['durationType'],
                        "spType": level['spData']['spType'],
                        'spData': level['spData']})
    talents = []
    if token_dict['talents']:
        for talent_index, talent in enumerate(token_dict['talents']):
            if not talent['candidates']:
                continue
            max_candidate_index = len(talent['candidates'])-1
            maxed_talent = talent['candidates'][max_candidate_index]
            talent_holder = {
                "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                "desc_zh": replace_substrings(maxed_talent["description"],maxed_talent['blackboard']), 
                "desc_ja": "", "desc_en": ""}
            if in_global:
                talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_ja"] = replace_substrings(jp_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"],maxed_talent['blackboard'])
                talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_en"] = replace_substrings(en_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"],maxed_talent['blackboard'])
            if maxed_talent['name']:
                talents.append(talent_holder)

    return_dict = {"id": id, "name_zh": token_dict['name'], "name_ja": "", "name_en": "",
                   "desc_zh": token_dict['description'].replace("<$ba","<ba"), "desc_ja": "", "desc_en": "",
                   "position": token_dict['position'], "tagList": [],
                   "stats": stats,
                    "skills": skills,
                    "talents":talents}
    if id in en_char_table:
        return_dict['name_ja'] = jp_char_table[id]['name']
        return_dict['name_en'] = en_char_table[id]['name']
        return_dict['desc_ja'] = jp_char_table[id]['description'].replace("<$ba","<ba")
        return_dict['desc_en'] = en_char_table[id]['description'].replace("<$ba","<ba")
    data[id] = return_dict

with open('tokens.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)