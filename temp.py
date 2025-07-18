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
# testing_chars = ['char_4116_blkkgt', 'char_003_kalts', 'char_4048_doroth', '']

enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open("enemy_database.json", encoding="utf-8") as f:
    my_enemy_db = json.load(f)


# for enemy in enemy_database['enemies']:
#     key = enemy['Key']
#     for stats in enemy['Value']:
#         if stats['enemyData']['attributes']['epDamageResistance']['m_value'] != 0 or stats['enemyData']['attributes']['epResistance']['m_value'] != 0:
#             print(key)

for [key,enemy] in my_enemy_db.items():
    db_enemy = next(item for item in enemy_database['enemies'] if item['Key'] == key, None)
    (db_enemy['Value'][0]['enemyData']['notCountInTotal'])
    enemy['notCountInTotal'] = db_enemy['Value'][0]['enemyData']['notCountInTotal']['m_value'] if db_enemy['Value'][0]['enemyData']['notCountInTotal']['m_defined'] else False

with open("enemy_database.json", "w", encoding="utf-8") as f:
    data_to_write = my_enemy_db
    json.dump(data_to_write, f, ensure_ascii=False, indent=4)