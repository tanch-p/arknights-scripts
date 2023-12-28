import json
import os

STAT_KEY_CONVERSION_TABLE = {
    "maxHp": "hp",
    "baseAttackTime": "aspd",
    "magicResistance": "res",
    "massLevel": "weight",
    "moveSpeed": "ms"
}

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_roguelike_topic_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
en_roguelike_topic_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/roguelike_topic_table.json"
)
jp_roguelike_topic_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/roguelike_topic_table.json"
)
enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)

with open(cn_roguelike_topic_path, encoding="utf-8") as f:
    cn_roguelike_topic_table = json.load(f)
with open(en_roguelike_topic_path, encoding="utf-8") as f:
    en_roguelike_topic_table = json.load(f)
with open(jp_roguelike_topic_path, encoding="utf-8") as f:
    jp_roguelike_topic_table = json.load(f)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open("enemy_database.json", encoding="utf-8") as f:
    my_enemy_db = json.load(f)
with open("is_stages_extrainfo.json", encoding="utf-8") as f:
    extrainfo = json.load(f)
with open("talent_overwrite_list.json", encoding="utf-8") as f:
    talent_overwrite_list = json.load(f)
stages_list = []

roguelike_topics = [
    # {"topic": "rogue_1", "folder": "ro1"},
    {"topic": "rogue_2", "folder": "ro2"},
    {"topic": "rogue_3", "folder": "ro3"},
]

for topic_dict in roguelike_topics:
    for stage_key in cn_roguelike_topic_table["details"][topic_dict["topic"]]["stages"]:
        stage_info_cn = cn_roguelike_topic_table["details"][topic_dict["topic"]][
            "stages"
        ][stage_key]
        try:
            stage_info_jp = jp_roguelike_topic_table["details"][topic_dict["topic"]][
                "stages"
            ][stage_key]
            stage_info_en = en_roguelike_topic_table["details"][topic_dict["topic"]][
                "stages"
            ][stage_key]
            TOPIC_IN_GLOBAL = True
        except KeyError:
            TOPIC_IN_GLOBAL = False
        if not ("_n_" in stage_info_cn["id"] and stage_info_cn["isElite"] == 0):
            levelId = stage_info_cn["levelId"].split("/")[-1]
            folder = topic_dict["folder"]
            stage_data_path = os.path.join(
                script_dir,
                f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{levelId}.json",
            )
            with open(stage_data_path, encoding="utf-8") as f:
                stage_data = json.load(f)

            trimmed_stage_info = {
                "id": stage_info_cn["id"],
                "levelId": levelId,
                "tags": stage_data["mapData"]["tags"],
                "category": extrainfo[levelId]['category'] if levelId in extrainfo else None,
                "characterLimit": stage_data["options"]["characterLimit"],
                "initialCost": stage_data["options"]["initialCost"],
                "costIncreaseTime": stage_data["options"]["costIncreaseTime"],
                "code": stage_info_cn["code"],
                "name_zh": stage_info_cn["name"],
                "name_ja": stage_info_jp["name"].replace(" ", "_") if TOPIC_IN_GLOBAL else None,
                "name_en": stage_info_en["name"].replace(" ", "_") if TOPIC_IN_GLOBAL else None,
                "description_zh": stage_info_cn["description"].replace("\\n", "\n"),
                "description_ja": stage_info_jp["description"].replace("\\n", "\n")
                if TOPIC_IN_GLOBAL
                else None,
                "description_en": stage_info_en["description"].replace("\\n", "\n")
                if TOPIC_IN_GLOBAL
                else None,
                "addInfo_zh": extrainfo[levelId]['addInfo_zh'] if levelId in extrainfo else None,
                "addInfo_ja": extrainfo[levelId]['addInfo_ja'] if levelId in extrainfo else None,
                "addInfo_en": extrainfo[levelId]['addInfo_en'] if levelId in extrainfo else None,
                "eliteDesc_zh":  extrainfo[levelId]['eliteDesc_zh'] if levelId in extrainfo else None,
                "eliteDesc_ja": extrainfo[levelId]['eliteDesc_ja'] if levelId in extrainfo else None,
                "eliteDesc_en": extrainfo[levelId]['eliteDesc_en'] if levelId in extrainfo else None,
                "elite_mods": extrainfo[levelId]['elite_mods'] if levelId in extrainfo else None,
                "routes": extrainfo[levelId]['routes'] if levelId in extrainfo else None,
                "floors": extrainfo[levelId]['floors'] if levelId in extrainfo else None,
                "sp_terrain": extrainfo[levelId]['sp_terrain'] if levelId in extrainfo else None,
                "sp_enemy": extrainfo[levelId]['sp_enemy'] if levelId in extrainfo else None,
            }
            enemy_list = extrainfo[levelId]['enemy_list'] if levelId in extrainfo else None
            elite_enemy_list = extrainfo[levelId]['elite_enemy_list'] if levelId in extrainfo else None
            enemies = []
            for enemy in stage_data["enemyDbRefs"]:
                if enemy['id'] == 'enemy_2062_smcar':
                    continue
                if enemy['id'] in my_enemy_db or enemy['id'] == 'enemy_1106_byokai_b':
                    enemy_id = enemy['id']
                    if enemy['id'] not in my_enemy_db:
                        enemy_id = enemy["overwrittenData"]['prefabKey']['m_value']
                    overwrittenData = {}
                    if enemy["overwrittenData"]:
                        for key in enemy["overwrittenData"]["attributes"]:
                            if enemy["overwrittenData"]["attributes"][key]["m_defined"]:
                                if key in STAT_KEY_CONVERSION_TABLE:
                                    overwrittenData[STAT_KEY_CONVERSION_TABLE[key]] = enemy["overwrittenData"][
                                        "attributes"
                                    ][key]["m_value"]
                                else:
                                    overwrittenData[key] = enemy["overwrittenData"][
                                        "attributes"
                                    ][key]["m_value"]
                        if enemy["overwrittenData"]["lifePointReduce"]["m_defined"]:
                            overwrittenData["lifepoint"] = enemy[
                                "overwrittenData"
                            ]["lifePointReduce"]["m_value"]
                        if enemy["overwrittenData"]["rangeRadius"]["m_defined"]:
                            overwrittenData["range"] = enemy["overwrittenData"][
                                "rangeRadius"
                            ]["m_value"]
                        if enemy['overwrittenData']['talentBlackboard']:
                            if enemy['id'] == 'enemy_1106_byokai_b' and folder == 'ro3':
                                overwrittenData['talentBlackboard'] = talent_overwrite_list['rogue_3'][enemy['id']]
                            elif levelId in talent_overwrite_list and enemy['id'] in talent_overwrite_list[levelId]:
                                overwrittenData['talentBlackboard'] = talent_overwrite_list[levelId][enemy['id']]
                    if len(overwrittenData) == 0:
                        overwrittenData = None
                    min_count = 0
                    max_count = 0
                    elite_min_count = None
                    elite_max_count = None
                    if enemy_list is not None:
                        for enemy_info in enemy_list:
                            if enemy_info['key'] == enemy['id']:
                                min_count = enemy_info['min_count']
                                max_count = enemy_info['max_count']
                    if elite_enemy_list is not None:
                        for enemy_info in elite_enemy_list:
                            if enemy_info['key'] == enemy['id']:
                                elite_min_count = enemy_info['min_count']
                                elite_max_count = enemy_info['max_count']

                    enemies.append(
                        {
                            "id": enemy_id,
                            "level": enemy["level"],
                            "min_count": min_count,
                            "max_count": max_count,
                            "elite_min_count": elite_min_count,
                            "elite_max_count": elite_max_count,
                            "overwrittenData": overwrittenData,
                        }
                    )
            trimmed_stage_info["enemies"] = enemies
            stages_list.append(trimmed_stage_info)

with open("is_stages_list_read.json", "w", encoding="utf-8") as f:
    json.dump(stages_list, f, ensure_ascii=False, indent=4)


with open("is_stages_list.json", "w", encoding="utf-8") as f:
    json.dump(stages_list, f, ensure_ascii=False, separators=(',', ':'))
