import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
en_enemy_database_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/levels/enemydata/enemy_database.json"
)
jp_enemy_database_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/levels/enemydata/enemy_database.json"
)

with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open(en_enemy_database_path, encoding="utf-8") as f:
    en_enemy_database = json.load(f)
with open(jp_enemy_database_path, encoding="utf-8") as f:
    jp_enemy_database = json.load(f)

with open("enemy_database.json", encoding="utf-8") as f:
    existing_data = json.load(f)

enemies = {}
for key in existing_data:
    data = existing_data[key]
    jp_db_enemy = next(
        (item for item in jp_enemy_database['enemies'] if item['Key'] == key), None)
    en_db_enemy = next(
        (item for item in en_enemy_database['enemies'] if item['Key'] == key), None)
    data["name_ja"] = (
        jp_db_enemy['Value'][0]['enemyData']["name"]["m_value"] if jp_db_enemy else ""
    )
    data["name_en"] = (
        en_db_enemy['Value'][0]['enemyData']["name"]["m_value"] if en_db_enemy else ""
    )
    enemies[key] = data

with open("enemy_database.json", "w", encoding="utf-8") as f:
    data_to_write = enemies
    json.dump(data_to_write, f, ensure_ascii=False, indent=4)
