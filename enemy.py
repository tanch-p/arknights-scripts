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
en_enemy_database_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/levels/enemydata/enemy_database.json"
)
jp_enemy_database_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/levels/enemydata/enemy_database.json"
)


def get_status_immune_list(stat):
    list = []
    if stat["enemyData"]["attributes"]["stunImmune"]["m_value"]:
        list.append("stun")
    if stat["enemyData"]["attributes"]["silenceImmune"]["m_value"]:
        list.append("silence")
    if stat["enemyData"]["attributes"]["sleepImmune"]["m_value"]:
        list.append("sleep")
    if stat["enemyData"]["attributes"]["frozenImmune"]["m_value"]:
        list.append("freeze")
    if stat["enemyData"]["attributes"]["levitateImmune"]["m_value"]:
        list.append("levitate")
    if stat["enemyData"]["attributes"]["disarmedCombatImmune"]["m_value"]:
        list.append("tremble")
    if stat["enemyData"]["attributes"]["fearedImmune"]["m_value"]:
        list.append("fear")
    if stat["enemyData"]["attributes"]["palsyImmune"]["m_value"]:
        list.append("palsy")
    if stat["enemyData"]["attributes"]["attractImmune"]["m_value"]:
        list.append("attract")
    return list


with open(cn_enemy_handbook_path, encoding="utf-8") as f:
    cn_enemy_handbook = json.load(f)
with open(en_enemy_handbook_path, encoding="utf-8") as f:
    en_enemy_handbook = json.load(f)
with open(jp_enemy_handbook_path, encoding="utf-8") as f:
    jp_enemy_handbook = json.load(f)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open(en_enemy_database_path, encoding="utf-8") as f:
    en_enemy_database = json.load(f)
with open(jp_enemy_database_path, encoding="utf-8") as f:
    jp_enemy_database = json.load(f)

with open("enemy_database.json", encoding="utf-8") as f:
    existing_data = json.load(f)

new_data = {}
for entry in enemy_database["enemies"]:
    data = {}
    key = entry['Key']
    if not key in existing_data:
        IN_HANDBOOK = key in cn_enemy_handbook['enemyData']
        if not IN_HANDBOOK:
            continue
        cn_enemy_info = cn_enemy_handbook['enemyData'][key] if IN_HANDBOOK else None
        enemyIndex = cn_enemy_info["enemyIndex"] if IN_HANDBOOK else "-"
        enemyStats = entry['Value']
        jp_entry = next((enemy for enemy in jp_enemy_database["enemies"]
                        if enemy['Key'] == key), None)
        en_entry = next((enemy for enemy in en_enemy_database["enemies"]
                        if enemy['Key'] == key), None)
        # attackType = MELEE | RANGED | ALL | NONE
        attackType = enemyStats[0]['enemyData']['applyWay']['m_value'].lower()
        attackAttribute = "phys"
        damageType = cn_enemy_info['damageType'] if IN_HANDBOOK else ''
        if "MAGIC" in damageType:
            attackAttribute = "arts"
        elif "NO_DAMAGE" in damageType:
            attackAttribute = None
            attackType = "no_attack"
        normal_attack = {"atk_type": [
            attackType, attackAttribute], "hits": 1}
        is_flying = False
        enemyTags = enemyStats[0]['enemyData']['enemyTags']['m_value'] or []
        if key in cn_enemy_handbook:
            is_flying = any('飞行单位' in item['text'] for item in cn_enemy_handbook[key]
                            ['abilityList']) or '飞行单位' in cn_enemy_handbook[key]['description']
        if "drone" in enemyTags or is_flying:
            enemyTags.append("flying")
        enemyTags.append(enemyStats[0]['enemyData']['levelType']['m_value']
                         if enemyStats[0]['enemyData']['levelType']['m_defined'] else 'NORMAL')
        data["id"] = enemyIndex
        data["key"] = key
        data['sortId'] = cn_enemy_info['sortId'] if IN_HANDBOOK else None
        data["name_zh"] = enemyStats[0]['enemyData']['name']['m_value']
        data["name_ja"] = jp_entry['Value'][0]['enemyData']['name']['m_value'] if jp_entry else ""
        data["name_en"] = en_entry['Value'][0]['enemyData']['name']['m_value'] if en_entry else ""

        status_immune_list = get_status_immune_list(enemyStats[0])
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
                "lifepoint": enemyStats[0]["enemyData"]["lifePointReduce"]["m_value"]
                if enemyStats[0]["enemyData"]["lifePointReduce"]["m_defined"] else 1,
                "ms": stat["enemyData"]["attributes"]["moveSpeed"]["m_value"]
                if stat["enemyData"]["attributes"]["moveSpeed"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["moveSpeed"][
                    "m_value"
                ],
                "epDamageResistance": stat["enemyData"]["attributes"]["epDamageResistance"]["m_value"]
                if stat["enemyData"]["attributes"]["epDamageResistance"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["epDamageResistance"][
                    "m_value"
                ],
                "epResistance": stat["enemyData"]["attributes"]["epResistance"]["m_value"]
                if stat["enemyData"]["attributes"]["epResistance"]["m_defined"]
                else enemyStats[0]["enemyData"]["attributes"]["epResistance"][
                    "m_value"
                ],
                "traits": [],
                "special": [],
            }
            for stat in enemyStats
        ]
        data['forms'] = [{
            "title": None,
            "normal_attack": normal_attack,
            "status_immune": get_status_immune_list(enemyStats[0]) if len(get_status_immune_list(enemyStats[0])) > len(status_immune_list) else status_immune_list

        }]
        data["type"] = enemyTags
        data["type"].insert(0, attackType)
        new_data[key] = data

with open("enemy_database.json", "w", encoding="utf-8") as f:
    data_to_write = existing_data | new_data
    json.dump(data_to_write, f, ensure_ascii=False, indent=4)
