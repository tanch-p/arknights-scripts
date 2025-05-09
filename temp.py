from os import walk
import pprint
import os
import json

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
# cn_char_table_path = os.path.join(
#     script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
# with open(cn_char_table_path, encoding='utf-8') as f:
#     char_table = json.load(f)

# list = []
# for id in char_table:
#     chara_dict = char_table[id]
#     for pot in chara_dict['potentialRanks']:
#         if pot['buff']:
#             for item in pot['buff']['attributes']['attributeModifiers']:
#                 if not item['attributeType'] in list:
#                     list.append(item['attributeType'])

# print(list)
# return_dict = [ele for ele in list]

# with open('temp.json','w', encoding='utf-8') as f:
#     json.dump(return_dict, f, ensure_ascii=False, indent=4)

# enemy_database_path = os.path.join(
#     script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
# )
# with open(enemy_database_path, encoding="utf-8") as f:
#     enemy_database = json.load(f)

# for enemy in enemy_database['enemies']:
#     key = enemy['Key']
#     for stats in enemy['Value']:
#         if stats['enemyData']['attributes']['epDamageResistance']['m_value'] != 0 or stats['enemyData']['attributes']['epResistance']['m_value'] != 0:
#             print(key)

# with open('chara_talents.json', encoding='utf-8') as f:
#     chara_talents = json.load(f)

# return_dict = {}
# for id in chara_talents:
#     talents = []
#     for talent_index, talent in enumerate(chara_talents[id]['talents']):
#         talent_holder = {
#             "prefabKey": talent["prefabKey"], "name_zh": talent["name_zh"], "name_ja": talent['name_ja'], "name_en": talent['name_en'],
#             "desc_zh": talent["description_zh"], "desc_ja":  talent['description_ja'], "desc_en": talent['description_en'], "target_air": None, "tags": talent['tags'] , "blackboard": talent['blackboard']}
#         talents.append(talent_holder)
#     return_dict[id] = {
#         "appellation": chara_talents[id]['appellation'], "talents": talents}

# with open('chara_talents.json', 'w', encoding='utf-8') as f:
#     json.dump(return_dict, f, ensure_ascii=False, indent=4)

# handpicked 50 characters for testing
testing_chars = ['char_4116_blkkgt', 'char_003_kalts', 'char_4048_doroth', '']


#! for rewriting enemy database

with open("enemy_database.json", encoding="utf-8") as f:
    enemy_db = json.load(f)

new_data = {}

for key in enemy_db:
    enemy = enemy_db[key]
    forms = [{"title": None, "normal_attack": enemy['normal_attack']
              if 'normal_attack' in enemy else None, "status_immune": enemy['status_immune']}]
    stats = [{
        "hp": stat['hp'],
        "atk": stat['atk'],
        "def": stat['def'],
        "res": stat['res'],
        "aspd": stat['aspd'],
        "range": stat['range'],
        "weight": stat['weight'],
        "lifepoint": stat['lifepoint'],
        "ms": stat['ms'],
        "epDamageResistance": stat['epDamageResistance'],
        "epResistance": stat['epResistance'],
        "traits":[],
        "special": []
    } for stat in enemy['stats']]

    if 'forms' in enemy:
        forms = []
        special = []
        form_mods = []
        for form in enemy['forms']:
            special.append([form['special']])
            form_mods.append(form['mods'])
            forms.append(
                {"title": form['title'], 'normal_attack': form['normal_attack'],"status_immune": enemy['status_immune']})
        for stat in stats:
            stat['special'] = special
            stat['form_mods'] = form_mods
    else:
        for stat in stats:
            stat['traits'] = enemy['special']
    holder = {
        "id": enemy['id'],
        "key": enemy["key"],
        "name_zh": enemy['name_zh'],
        "name_ja": enemy["name_ja"],
        "name_en": enemy['name_en'],
        "stats": stats,
        "forms": forms,
        "type": enemy['type']
    }
    new_data[key] = holder

with open("enemy_database.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
