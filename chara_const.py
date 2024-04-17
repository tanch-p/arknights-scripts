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

cn_handbook_info_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/handbook_info_table.json")
cn_team_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/handbook_team_table.json")
en_handbook_info_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/handbook_info_table.json")
en_team_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/handbook_team_table.json")
jp_handbook_info_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/handbook_info_table.json")
jp_team_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/handbook_team_table.json")

with open(cn_handbook_info_path, encoding='utf-8') as f:
    cn_handbook_info = json.load(f)
with open(cn_team_table_path, encoding='utf-8') as f:
    cn_team_table = json.load(f)
with open(en_handbook_info_path, encoding='utf-8') as f:
    en_handbook_info = json.load(f)
with open(en_team_table_path, encoding='utf-8') as f:
    en_team_table = json.load(f)
with open(jp_handbook_info_path, encoding='utf-8') as f:
    jp_handbook_info = json.load(f)
with open(jp_team_table_path, encoding='utf-8') as f:
    jp_team_table = json.load(f)

data = {
    "groups": {}
}

for key in cn_team_table:
    data['groups'][key] = {"zh": cn_team_table[key]['powerName'], "en": en_team_table[key]
                           ['powerName'], "ja": jp_team_table[key]['powerName']}


with open('chara_const.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
