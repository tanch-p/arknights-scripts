import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_enemy_handbook_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/enemy_handbook_table.json"
)

enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)

with open(cn_enemy_handbook_path, encoding="utf-8") as f:
    cn_enemy_handbook = json.load(f)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)

with open("enemy_database.json", encoding="utf-8") as f:
    existing_data = json.load(f)

for enemy in enemy_database["enemies"]:
    key = enemy["Key"]
    for value in enemy['Value']:
        if value['enemyData']['attributes']['disarmedCombatImmune']['m_value'] is True:
            print(key, " tremble immune")
        if value['enemyData']['attributes']['fearedImmune']['m_value'] is True:
            print(key, " fear immune")
        if value['enemyData']['attributes']['epDamageResistance']['m_value'] != 0:
            print(key, " epDamageResistance not 0")
        if value['enemyData']['attributes']['epResistance']['m_value'] != 0:
            print(key, " epResistance not 0")