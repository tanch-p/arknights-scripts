import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)

filtered_cn_char_table = {key: cn_char_table[key] for key in cn_char_table.keys(
) if not "token" in key and not "trap" in key}

tokens_list = []
for id in filtered_cn_char_table:
    character_dict = filtered_cn_char_table[id]
    if character_dict['displayTokenDict'] is not None:
        tokens =[key for key in character_dict['displayTokenDict']]
        tokens_list += tokens

print(tokens_list)
data = {}
for id in tokens_list:


    return_dict = {"id": id, "appellation": character_dict['appellation'], "name_zh": character_dict['name'], "name_ja": "", "name_en": "",
                   "desc_zh": character_dict['description'].replace("<$ba","<ba"), "desc_ja": "", "desc_en": "",
                   "nationId": character_dict['nationId'], "groupId": character_dict['groupId'], "teamId": character_dict['teamId'], "position": character_dict['position'], "tagList": [],
                   "isSpChar": character_dict['isSpChar'], "rarity": character_dict['rarity'],
                   "profession": character_dict['profession'], "subProfessionId": character_dict['subProfessionId'], "stats": stats,
                    "talents": talents, "tagList": [], 'uniequip': uniequip_list}
    if id in en_char_table:
        return_dict['name_ja'] = jp_char_table[id]['name']
        return_dict['name_en'] = en_char_table[id]['name']
        return_dict['desc_ja'] = jp_char_table[id]['description'].replace("<$ba","<ba")
        return_dict['desc_en'] = en_char_table[id]['description'].replace("<$ba","<ba")
    data[id] = return_dict

with open('tokens.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)