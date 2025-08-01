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
    talentBlackboard = []
    talentLength = 0
    skills = []
    skillsLength = 0
    for value in enemy['Value']:
        # if value['enemyData']['attributes']['palsyImmune']['m_value'] is True:
        #     print(key, " palsy immune")
        # if value['enemyData']['attributes']['attractImmune']['m_value'] is True:
        #     print(key, " attract immune")
        # if value['enemyData']['attributes']['epDamageResistance']['m_value'] != 0:
        #     print(key, " epDamageResistance not 0")
        # if value['enemyData']['attributes']['epResistance']['m_value'] != 0:
        #     print(key, " epResistance not 0")
        if value['enemyData']['attributes']['tauntLevel']['m_value'] != 0:
            print(key, f" tauntLevel {value['enemyData']['attributes']['tauntLevel']['m_value']}")
    #     if value['enemyData']['talentBlackboard'] is not None:
    #         for talent in value['enemyData']['talentBlackboard']:
    #             if not talent in talentBlackboard:
    #                 talentBlackboard.append(talent)
    #         if talentLength == 0 and len(talentBlackboard) > talentLength:
    #             talentLength = len(talentBlackboard)
    #     if value['enemyData']['skills'] is not None:
    #         for skill in value['enemyData']['skills']:
    #             if not skill in skills:
    #                 skills.append(skill)
    #         if skillsLength == 0 and len(skills) > skillsLength:
    #             skillsLength = len(skills)
    # if talentLength != len(talentBlackboard):
    #     print(key, " talentBlackboard diff across levels")
    # if skillsLength != len(skills):
    #     print(key, " skills diff across levels")