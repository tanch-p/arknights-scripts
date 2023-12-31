import os
import json
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

with open('characters.json', encoding='utf-8') as f:
    char_table = json.load(f)

list = []
for chara in char_table:
    if not chara['subProfessionId'] in list:
        list.append(chara['subProfessionId'])

return_dict = [ele for ele in list]

with open('temp.json','w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)

enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)

# for enemy in enemy_database['enemies']:
#     key = enemy['Key']
#     for stats in enemy['Value']:
#         if stats['enemyData']['attributes']['epDamageResistance']['m_value'] != 0 or stats['enemyData']['attributes']['epResistance']['m_value'] != 0:
#             print(key)

