import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_enemy_handbook_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/enemy_handbook_table.json"
)
en_enemy_handbook_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/enemy_handbook_table.json"
)
jp_enemy_handbook_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/enemy_handbook_table.json"
)
enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)

with open(cn_enemy_handbook_path, encoding="utf-8") as f:
    cn_enemy_handbook = json.load(f)
with open(en_enemy_handbook_path, encoding="utf-8") as f:
    en_enemy_handbook = json.load(f)
with open(jp_enemy_handbook_path, encoding="utf-8") as f:
    jp_enemy_handbook = json.load(f)

with open("enemy_database.json", encoding="utf-8") as f:
    existing_data = json.load(f)

enemies = {}
for key in existing_data:
    data = existing_data[key]

    data["name_ja"] = (
        jp_enemy_handbook[key]["name"] if key in jp_enemy_handbook else ""
    )
    data["name_en"] = (
        en_enemy_handbook[key]["name"] if key in en_enemy_handbook else ""
    )
    enemies[key] = data

with open("enemy_database.json", "w", encoding="utf-8") as f:
    data_to_write = enemies
    json.dump(data_to_write, f, ensure_ascii=False, indent=4)