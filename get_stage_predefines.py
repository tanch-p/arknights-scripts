import os
from os import walk
import json
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
en_skill_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/skill_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")
jp_skill_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/skill_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(en_skill_table_path, encoding='utf-8') as f:
    en_skill_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)
with open(jp_skill_table_path, encoding='utf-8') as f:
    jp_skill_table = json.load(f)

KEYS_TO_EXCLUDE = ["trap_051_vultres", "trap_042_tidectrl", "trap_079_allydonq", "trap_061_creep", "trap_038_dsbell", "trap_037_airsup", "trap_062_magicstart",
                   "trap_063_magicturn", "trap_106_smtree", "trap_050_blizzard", "trap_092_vgctrl", "trap_036_storm", "trap_764_skzshp", "trap_162_lrctrl", "trap_766_duelwal", "trap_767_duelcdt"]

folders = ["ro1", "ro2", "ro3", 'ro5']
token_list = []
# 1 get all token keys
for folder in folders:
    files = []
    path = os.path.join(
        script_dir,
        f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}",
    )
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend([f for (
            dirpath, dirnames, filenames) in os.walk(path) for f in filenames])
        break
    files.sort()
    for stage_id in files:
        if 'r1' in stage_id:
            continue
        stage_data_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{stage_id}",
        )
        with open(stage_data_path, encoding="utf-8") as f:
            stage_data = json.load(f)
        if stage_data['predefines']:
            for item in stage_data['predefines']['tokenInsts']:
                key = item['inst']['characterKey']
                print(stage_id)
                if item['inst']['phase'] != 'PHASE_0':
                    print(key, " phase not 0")
                if item['mainSkillLvl'] != 1:
                    print(key, " mainSkillLvl not 1")
                # if item['overrideSkillBlackboard'] is not None:
                #     print(key, " overrideSkillBlackboard not null")
                if key in KEYS_TO_EXCLUDE:
                    continue
                if not key in token_list:
                    token_list.append(key)

token_list = sorted(token_list)
data = {}
for key in token_list:
    holder = {}
    character_dict = cn_char_table[key]

    # data checker
    if len(character_dict['phases']) > 1:
        print(key, "phases more than 1")
    level1 = character_dict['phases'][-1]["attributesKeyFrames"][0]['data']
    level30 = character_dict['phases'][-1]["attributesKeyFrames"][1]['data']
    has_levels = level1 != level30

    in_global = key in en_char_table
    skills = []
    talents = []
    for skill in character_dict['skills']:
        skills.append(skill['skillId'])
    status_immune = []
    if level1["stunImmune"]:
        status_immune.append("stun")
    if level1["silenceImmune"]:
        status_immune.append("silence")
    if level1["sleepImmune"]:
        status_immune.append("sleep")
    if level1["frozenImmune"]:
        status_immune.append("freeze")
    if level1["levitateImmune"]:
        status_immune.append("levitate")
    if level1["disarmedCombatImmune"]:
        status_immune.append("tremble")
    if level1["fearedImmune"]:
        status_immune.append("fear")
    holder["name_zh"] = cn_char_table[key]["name"]
    holder["name_ja"] = (
        jp_char_table[key]["name"] if in_global else ""
    )
    holder["name_en"] = (
        en_char_table[key]["name"] if in_global else ""
    )
    holder['desc_zh'] = cn_char_table[key]['description']
    holder["desc_ja"] = (
        jp_char_table[key]["description"] if in_global else ""
    )
    holder["desc_en"] = (
        en_char_table[key]["description"] if in_global else ""
    )
    holder["stats"] = [
        {
            "hp": level1['maxHp'],
            "atk": level1['atk'],
            "def": level1['def'],
            "res": level1[
                "magicResistance"
            ],
            'blockCnt': level1['blockCnt'],
            "aspd": level1["baseAttackTime"],
            "rangeId": character_dict['phases'][-1]['rangeId']
        }
    ]
    if has_levels:
        holder["stats"].append({
            "hp": level30['maxHp'],
            "atk": level30['atk'],
            "def": level30['def'],
            "res": level30[
                "magicResistance"
            ],
            'blockCnt': level30['blockCnt'],
            "aspd": level30["baseAttackTime"],
            "rangeId": character_dict['phases'][-1]['rangeId']
        })
    holder["special"] = skills
    holder["status_immune"] = status_immune
    data[key] = holder


with open("stage_predefines.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
