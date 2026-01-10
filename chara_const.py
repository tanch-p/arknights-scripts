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
                 "root", "tremble", "magicfragile"
                "fragile", "dt.apoptosis2", "dt.burning2",
                "steal", "weightless"]

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_handbook_info_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/handbook_info_table.json")
cn_team_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/handbook_team_table.json")
en_handbook_info_path = os.path.join(
    script_dir, "global_data/en/gamedata/excel/handbook_info_table.json")
en_team_table_path = os.path.join(
    script_dir, "global_data/en/gamedata/excel/handbook_team_table.json")
jp_handbook_info_path = os.path.join(
    script_dir, "global_data/jp/gamedata/excel/handbook_info_table.json")
jp_team_table_path = os.path.join(
    script_dir, "global_data/jp/gamedata/excel/handbook_team_table.json")

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
    'chara_handbook': {},
    "groups": {}
}

for key in cn_team_table:
    data['groups'][key] = {"zh": cn_team_table[key]['powerName'], "en": en_team_table[key]
                           ['powerName'], "ja": jp_team_table[key]['powerName']}
for key in cn_handbook_info['handbookDict']:
    race = {}
    birthplace = {}
    if 'npc' in key:
        continue
    cn_info = cn_handbook_info['handbookDict'][key]['storyTextAudio'][0]['stories'][0]['storyText']
    # if not '种族' in cn_info:
    #     print(key,"no 种族")
    if not '种族' in cn_info:
        race['zh'] = "其他"
        race['en'] = "Others"
        race['ja'] = "その他"
    else:
        race['zh'] = cn_info.split("【种族】")[1].split("\n")[0].strip()
        birthplace['zh'] = cn_info.split("【出身地】")[1].split("\n")[0].strip()
        if key in en_handbook_info['handbookDict']:
            race['en'] = en_handbook_info['handbookDict'][key]['storyTextAudio'][0]['stories'][0]['storyText'].split("[Race]")[
                1].split("\n")[0].strip()
            birthplace['en'] = en_handbook_info['handbookDict'][key]['storyTextAudio'][0]['stories'][0]['storyText'].split("[Place of Birth]")[
                1].split("\n")[0].strip()
            race['ja'] = jp_handbook_info['handbookDict'][key]['storyTextAudio'][0]['stories'][0]['storyText'].split("【種族】")[
                1].split("\n")[0].strip()
            birthplace['ja'] = jp_handbook_info['handbookDict'][key]['storyTextAudio'][0]['stories'][0]['storyText'].split("【出身地】")[
                1].split("\n")[0].strip()
        else:
            race['en'] = ''
            birthplace['en'] = ''
            race['ja'] = ''
            birthplace['ja'] = ''
    data['chara_handbook'][key] = {"race": race, "birthplace": birthplace}


with open('chara_const.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
