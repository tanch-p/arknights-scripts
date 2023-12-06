import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_enemy_handbook_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/enemy_handbook_table.json"
)
en_enemy_handbook_path = os.path.join(
    script_dir, "en_US/gamedata/excel/enemy_handbook_table.json"
)
jp_enemy_handbook_path = os.path.join(
    script_dir, "ja_JP/gamedata/excel/enemy_handbook_table.json"
)
enemy_database_path = os.path.join(
    script_dir, "zh_CN/gamedata/levels/enemydata/enemy_database.json"
)

with open(cn_enemy_handbook_path, encoding="utf-8") as f:
    cn_enemy_handbook = json.load(f)
with open(en_enemy_handbook_path, encoding="utf-8") as f:
    en_enemy_handbook = json.load(f)
with open(jp_enemy_handbook_path, encoding="utf-8") as f:
    jp_enemy_handbook = json.load(f)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)

with open("enemy_database.json", encoding="utf-8") as f:
    existing_data = json.load(f)

new_data = {}
for key in cn_enemy_handbook['enemyData']:
    data = {}
    cn_enemy_info = cn_enemy_handbook['enemyData'][key]
    enemyId = cn_enemy_info["enemyId"]
    enemyIndex = cn_enemy_info["enemyIndex"]
    if not enemyId in existing_data:
        enemyDatabase = enemy_database["enemies"]
        enemyStats = next(
            enemyData["Value"]
            for enemyData in enemyDatabase
            if enemyData["Key"] == key
        )
        # attackType = MELEE | RANGED | ALL | NONE
        attackType = enemyStats[0]['enemyData']['applyWay']['m_value'].lower()
        attackAttribute = "phys"
        damageType = cn_enemy_info['damageType']
        if "MAGIC" in damageType:
            attackAttribute = "arts"
        elif "NO_DAMAGE" in damageType:
            attackAttribute = None
            attackType = "no_attack"
        normal_attack = {"atk_type": [
            attackType, attackAttribute], "hits": 1}

        enemyTags = enemyStats[0]['enemyData']['enemyTags']['m_value'] or []
        if "drone" in enemyTags:
            enemyTags.append("flying")
        enemyTags.append(enemyStats[0]['enemyData']['levelType']['m_value']
                            if enemyStats[0]['enemyData']['levelType']['m_defined'] else 'NORMAL')

        status_immune = []
        if enemyStats[0]["enemyData"]["attributes"]["stunImmune"]["m_value"]:
            status_immune.append("stun")
        if enemyStats[0]["enemyData"]["attributes"]["silenceImmune"]["m_value"]:
            status_immune.append("silence")
        if enemyStats[0]["enemyData"]["attributes"]["sleepImmune"]["m_value"]:
            status_immune.append("sleep")
        if enemyStats[0]["enemyData"]["attributes"]["frozenImmune"]["m_value"]:
            status_immune.append("freeze")
        if enemyStats[0]["enemyData"]["attributes"]["levitateImmune"]["m_value"]:
            status_immune.append("levitate")

        data["id"] = enemyIndex
        data["key"] = key
        data['sortId'] = cn_enemy_info['sortId']
        data["name_zh"] = cn_enemy_info["name"]
        data["name_ja"] = (
            jp_enemy_handbook[key]["name"] if key in jp_enemy_handbook else ""
        )
        data["name_en"] = (
            en_enemy_handbook[key]["name"] if key in en_enemy_handbook else ""
        )
        data["stats"] = [
            {
                "hp": stat["enemyData"]["attributes"]["maxHp"]["m_value"]
                if stat["enemyData"]["attributes"]["maxHp"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["maxHp"]["m_value"],
                "atk": stat["enemyData"]["attributes"]["atk"]["m_value"]
                if stat["enemyData"]["attributes"]["atk"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["atk"]["m_value"],
                "def": stat["enemyData"]["attributes"]["def"]["m_value"]
                if stat["enemyData"]["attributes"]["def"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["def"]["m_value"],
                "res": stat["enemyData"]["attributes"][
                    "magicResistance"
                ]["m_value"]
                if stat["enemyData"]["attributes"]["magicResistance"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["magicResistance"][
                    "m_value"
                ],
                "aspd": stat["enemyData"]["attributes"]["baseAttackTime"][
                    "m_value"
                ]
                if stat["enemyData"]["attributes"]["baseAttackTime"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["baseAttackTime"][
                    "m_value"
                ],
                "range": stat["enemyData"]["rangeRadius"]["m_value"]
                if stat["enemyData"]["rangeRadius"]["m_defined"]
                else enemyStats[0]["enemyData"]["rangeRadius"]["m_value"],
                "weight": stat["enemyData"]["attributes"]["massLevel"]["m_value"]
                if stat["enemyData"]["attributes"]["massLevel"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["massLevel"][
                    "m_value"
                ],
                "lifepoint": enemyStats[0]["enemyData"]["lifePointReduce"][
                    "m_value"
                ],
                "ms": stat["enemyData"]["attributes"]["moveSpeed"]["m_value"]
                if stat["enemyData"]["attributes"]["moveSpeed"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["moveSpeed"][
                    "m_value"
                ]
            }
            for stat in enemyStats
        ]
        data["special"] = []
        data["status_immune"] = status_immune
        data["normal_attack"] = normal_attack
        data["type"] = enemyTags
        data["type"].insert(0, attackType)
        new_data[key] = data

with open("enemy_database.json", "w", encoding="utf-8") as f:
    data_to_write = existing_data | new_data
    json.dump(data_to_write, f, ensure_ascii=False, indent=4)
