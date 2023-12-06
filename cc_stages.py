import json
import os
from os import walk

STAT_KEY_CONVERSION_TABLE = {
    "maxHp": "hp",
    "baseAttackTime": "aspd",
    "magicResistance": "res",
    "massLevel": "weight",
    "moveSpeed": "ms"
}
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_rune_path = os.path.join(
    script_dir, "zh_CN\\gamedata\\levels\\obt\\rune"
)
enemy_database_path = os.path.join(
    script_dir, "zh_CN\\gamedata\\levels\\enemydata/enemy_database.json"
)

with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open("enemy_database.json", encoding="utf-8") as f:
    my_enemy_db = json.load(f)

stages_list = []

cc_stages = []

for (dirpath, dirnames, filenames) in walk(cn_rune_path):
    cc_stages.extend(filenames)
    break

for cc_stage in cc_stages:
    with open(cn_rune_path+"\\"+cc_stage, encoding="utf-8") as f:
        rune_stage_info = json.load(f)
        trimmed_stage_info = {
            "id": cc_stage,
            "cc_type": "perma" if "01" in cc_stage else "daily",
            "tags": rune_stage_info["mapData"]["tags"],
            "characterLimit": rune_stage_info["options"]["characterLimit"],
            "initialCost": rune_stage_info["options"]["initialCost"],
            "costIncreaseTime": rune_stage_info["options"]["costIncreaseTime"],
            "code": None,
            "name_zh": None,
            "name_ja": None,
            "name_en": None,
            "inner_name_zh": None,
            "inner_name_ja": None,
            "inner_name_en": None,
            "routes": None,
            "sp_terrain": None,
            "contracts": None,
        }

        enemies = []
        for enemy in rune_stage_info["enemyDbRefs"]:
            if enemy['id'] in my_enemy_db:
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
                if len(overwrittenData) == 0:
                    overwrittenData = None

                enemies.append(
                    {
                        "id": enemy["id"],
                        "level": enemy["level"],
                        # "min_count": min_count,
                        # "max_count": max_count,
                        # "elite_min_count": elite_min_count,
                        # "elite_max_count": elite_max_count,
                        "overwrittenData": overwrittenData,
                    }
                )
        trimmed_stage_info["enemies"] = enemies
        stages_list.append(trimmed_stage_info)

with open("cc_stages_list.json", "w", encoding="utf-8") as f:
    json.dump(stages_list, f, ensure_ascii=False, indent=4)
