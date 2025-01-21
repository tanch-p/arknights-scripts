import json
import os
from operator import itemgetter
from waves_new import get_waves_data


def replace_chevrons(text_list):
    if text_list and type(text_list) is list:
        replaced_texts = [text.replace("<", "&lt;").replace(
            ">", "&gt;") for text in text_list]
        return replaced_texts
    return text_list


STAT_KEY_CONVERSION_TABLE = {
    "maxHp": "hp",
    "baseAttackTime": "aspd",
    "magicResistance": "res",
    "massLevel": "weight",
    "moveSpeed": "ms"
}

TRAPS_TO_EXCLUDE = ["trap_051_vultres", "trap_042_tidectrl", "trap_061_creep", "trap_038_dsbell", "trap_037_airsup", "trap_062_magicstart",
                    "trap_063_magicturn", "trap_106_smtree", "trap_050_blizzard", "trap_092_vgctrl", "trap_036_storm", "trap_162_lrctrl", "trap_766_duelwal", "trap_767_duelcdt"]

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


def get_rogue_topic(folder):
    if folder == "ro1":
        return 'rogue_phantom'
    if folder == "ro2":
        return 'rogue_mizuki'
    if folder == "ro3":
        return 'rogue_sami'
    if folder == "ro4":
        return 'rogue_skz'


def get_timeline_enemy_counts(timeline):
    enemies_total = {}
    all_count = []
    bonus = {}
    for count in timeline:
        if count != 'bonus':
            all_count.append(int(count))
            for data in timeline[count]:
                tag = data['tags'].join("|")
                if not tag in bonus:
                    bonus[tag] = count+1
                enemies = {}
                for wave in data['waves']:
                    for time in wave['timeline']:
                        for action in wave['timeline'][time]:
                            if not action['key'] in enemies:
                                enemies[action['key']] = 0
                            enemies[action['key']] += 1
                for key in enemies:
                    if not key in enemies_total:
                        enemies_total[key] = []
                    if not enemies[key] in enemies_total[key]:
                        enemies_total[key].append(enemies[key])
    return {"enemies": enemies_total, "bonus": bonus}


data = {}
stage_name_lookup = {}
stages_list = []
roguelike_topics = [
    {"topic": "rogue_1", "folder": "ro1"},
    {"topic": "rogue_2", "folder": "ro2"},
    {"topic": "rogue_3", "folder": "ro3"},
    {"topic": "rogue_4", "folder": "ro4"},
]

STAGES_WITH_ENEMY_REF_TO_IGNORE = {"level_rogue4_b-8": ["enemy_3001_upeopl", 'enemy_2093_skzams'], "level_rogue4_4-4": ["enemy_1221_dzomg_b",
                                   "enemy_1220_dzoms_b"], "level_rogue3_b-4-b": ["enemy_2054_smdeer"]}
STAGES_TO_SKIP = ['ro4_b_4_c', 'ro4_b_4_d', 'ro4_b_5_c', 'ro4_b_5_d']
STAGES_WITH_ENEMY_REF_TO_REPLACE = {'level_rogue4_b-4': 'level_rogue4_b-4-c',
                                    'level_rogue4_b-4-b': 'level_rogue4_b-4-d',
                                    'level_rogue4_b-5': 'level_rogue4_b-5-c',
                                    'level_rogue4_b-5-b': 'level_rogue4_b-5-d',
                                    'level_rogue4_1-1': 'levelreplacers/level_rogue4_1-1_r2',
                                    'level_rogue4_1-2': 'levelreplacers/level_rogue4_1-2_r2',
                                    'level_rogue4_1-3': 'levelreplacers/level_rogue4_1-3_r2',
                                    'level_rogue4_1-4': 'levelreplacers/level_rogue4_1-4_r2',
                                    'level_rogue4_2-1': 'levelreplacers/level_rogue4_2-1_r2',
                                    'level_rogue4_2-2': 'levelreplacers/level_rogue4_2-2_r2',
                                    'level_rogue4_2-3': 'levelreplacers/level_rogue4_2-3_r2',
                                    'level_rogue4_2-4': 'levelreplacers/level_rogue4_2-4_r2',
                                    'level_rogue4_2-5': 'levelreplacers/level_rogue4_2-5_r2',
                                    'level_rogue4_3-1': 'levelreplacers/level_rogue4_3-1_r2',
                                    'level_rogue4_3-2': 'levelreplacers/level_rogue4_3-2_r2',
                                    'level_rogue4_3-3': 'levelreplacers/level_rogue4_3-3_r2',
                                    'level_rogue4_3-4': 'levelreplacers/level_rogue4_3-4_r2',
                                    'level_rogue4_3-5': 'levelreplacers/level_rogue4_3-5_r2',
                                    'level_rogue4_3-6': 'levelreplacers/level_rogue4_3-6_r2',
                                    'level_rogue4_4-1': 'levelreplacers/level_rogue4_4-1_r2',
                                    'level_rogue4_4-2': 'levelreplacers/level_rogue4_4-2_r2',
                                    'level_rogue4_4-3': 'levelreplacers/level_rogue4_4-3_r2',
                                    'level_rogue4_4-4': 'levelreplacers/level_rogue4_4-4_r2',
                                    'level_rogue4_4-5': 'levelreplacers/level_rogue4_4-5_r2',
                                    'level_rogue4_4-6': 'levelreplacers/level_rogue4_4-6_r2',
                                    'level_rogue4_4-7': 'levelreplacers/level_rogue4_4-7_r2',
                                    'level_rogue4_5-1': 'levelreplacers/level_rogue4_5-1_r2',
                                    'level_rogue4_5-2': 'levelreplacers/level_rogue4_5-2_r2',
                                    'level_rogue4_5-3': 'levelreplacers/level_rogue4_5-3_r2',
                                    'level_rogue4_5-4': 'levelreplacers/level_rogue4_5-4_r2',
                                    'level_rogue4_5-5': 'levelreplacers/level_rogue4_5-5_r2',
                                    'level_rogue4_5-6': 'levelreplacers/level_rogue4_5-6_r2',
                                    'level_rogue4_5-7': 'levelreplacers/level_rogue4_5-7_r2',
                                    'level_rogue4_6-1': 'levelreplacers/level_rogue4_6-1_r2',
                                    'level_rogue4_6-2': 'levelreplacers/level_rogue4_6-2_r2',
                                    'level_rogue4_7-1': 'levelreplacers/level_rogue4_7-1_r1',
                                    'level_rogue4_7-2': 'levelreplacers/level_rogue4_7-2_r1',
                                    'level_rogue4_b-1': 'levelreplacers/level_rogue4_b-1_r1',
                                    'level_rogue4_b-1-b': 'levelreplacers/level_rogue4_b-1-b_r1',
                                    'level_rogue4_b-1-c': 'levelreplacers/level_rogue4_b-1-c_r1',
                                    'level_rogue4_b-2': 'levelreplacers/level_rogue4_b-2_r1',
                                    'level_rogue4_b-2-b': 'levelreplacers/level_rogue4_b-2-b_r1',
                                    'level_rogue4_b-2-c': 'levelreplacers/level_rogue4_b-2-c_r1',
                                    'level_rogue4_b-3': 'levelreplacers/level_rogue4_b-3_r1',
                                    'level_rogue4_b-3-b': 'levelreplacers/level_rogue4_b-3-b_r1',
                                    'level_rogue4_b-3-c': 'levelreplacers/level_rogue4_b-3-c_r1',
                                    'level_rogue4_b-6': 'levelreplacers/level_rogue4_b-6_r1',
                                    'level_rogue4_ev-1': 'levelreplacers/level_rogue4_ev-1_r1',
                                    'level_rogue4_ev-2': 'levelreplacers/level_rogue4_ev-2_r1',
                                    'level_rogue4_t-1': 'levelreplacers/level_rogue4_t-1_r1',
                                    'level_rogue4_t-2': 'levelreplacers/level_rogue4_t-2_r1',
                                    'level_rogue4_t-3': 'levelreplacers/level_rogue4_t-3_r1',
                                    'level_rogue4_t-4': 'levelreplacers/level_rogue4_t-4_r1',
                                    'level_rogue4_t-5': 'levelreplacers/level_rogue4_t-5_r1',
                                    'level_rogue4_t-6': 'levelreplacers/level_rogue4_t-6_r1',
                                    'level_rogue4_t-7': 'levelreplacers/level_rogue4_t-7_r1',
                                    'level_rogue4_t-8': 'levelreplacers/level_rogue4_t-8_r1', }

for topic_dict in roguelike_topics:
    for stage_key in cn_roguelike_topic_table["details"][topic_dict["topic"]]["stages"]:
        to_skip = False
        for item in STAGES_TO_SKIP:
            if stage_key == item:
                to_skip = True
                break
        if to_skip:
            continue
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
                "name_zh":  stage_info_cn["name"] if levelId != 'level_rogue4_b-9' else '「」',
                "name_ja": (stage_info_jp["name"] if levelId != 'level_rogue4_b-9' else '「」').replace(" ", "_") if TOPIC_IN_GLOBAL else None,
                "name_en": (stage_info_en["name"] if levelId != 'level_rogue4_b-9' else '「」').replace(" ", "_") if TOPIC_IN_GLOBAL else None,
                "description_zh": stage_info_cn["description"].replace("\\n", "\n"),
                "description_ja": stage_info_jp["description"].replace("\\n", "\n")
                if TOPIC_IN_GLOBAL
                else None,
                "description_en": stage_info_en["description"].replace("\\n", "\n")
                if TOPIC_IN_GLOBAL
                else None,
                "addInfo_zh": replace_chevrons(extrainfo[levelId]['addInfo_zh']) if levelId in extrainfo else None,
                "addInfo_ja": replace_chevrons(extrainfo[levelId]['addInfo_ja']) if levelId in extrainfo else None,
                "addInfo_en": replace_chevrons(extrainfo[levelId]['addInfo_en']) if levelId in extrainfo else None,
                "eliteDesc_zh":  replace_chevrons(extrainfo[levelId]['eliteDesc_zh']) if levelId in extrainfo else None,
                "eliteDesc_ja": replace_chevrons(extrainfo[levelId]['eliteDesc_ja']) if levelId in extrainfo else None,
                "eliteDesc_en": replace_chevrons(extrainfo[levelId]['eliteDesc_en']) if levelId in extrainfo else None,
                "n_mods": extrainfo[levelId]['normal_mods'] if levelId in extrainfo else None,
                "elite_mods": extrainfo[levelId]['elite_mods'] if levelId in extrainfo else None,
                "routes": extrainfo[levelId]['routes'] if levelId in extrainfo else None,
                "floors": extrainfo[levelId]['floors'] if levelId in extrainfo else None,
                "sp_terrain": extrainfo[levelId]['sp_terrain'] if levelId in extrainfo else None,
                "sp_enemy": extrainfo[levelId]['sp_enemy'] if levelId in extrainfo else None,
                "n_count": extrainfo[levelId]['all_possible_enemy_count'] if levelId in extrainfo else None,
                "e_count": extrainfo[levelId]['all_possible_elite_enemy_count'] if levelId in extrainfo else None,
                "traps": []
            }

            # for reverse lookup in website
            rogue_topic = get_rogue_topic(folder)
            if levelId == 'level_rogue4_b-9':
                url_key = 'ro4_b_9'
                stage_name_lookup[url_key] = {
                    "lang": "ALL", "key": levelId, "topic": rogue_topic}
            else:
                zh_url_key = stage_info_cn["code"] + \
                    '_' + stage_info_cn["name"]
                stage_name_lookup[zh_url_key] = {
                    "lang": "zh", "key": levelId, "topic": rogue_topic}
                if TOPIC_IN_GLOBAL:
                    en_url_key = stage_info_en["code"] + \
                        '_' + stage_info_en["name"].replace(" ", "_")
                    ja_url_key = stage_info_jp["code"] + \
                        '_' + stage_info_jp["name"].replace(" ", "_")
                    stage_name_lookup[en_url_key] = {
                        "lang": "en", "key": levelId, "topic": rogue_topic}
                    stage_name_lookup[ja_url_key] = {
                        "lang": "ja", "key": levelId, "topic": rogue_topic}

            traps = []

            def find_item_by_key(lst, search_value): return next(
                (item for item in lst if item['key'] == search_value), None)
            if stage_data['predefines']:
                for item in stage_data['predefines']['tokenInsts']:
                    key = item['inst']['characterKey']
                    # if key == "trap_760_skztzs":
                    if not key in TRAPS_TO_EXCLUDE:
                        trap = find_item_by_key(traps, key)
                        if trap:
                            if trap['mainSkillLvl'] != item['mainSkillLvl'] and item['hidden'] != trap['hidden']:
                                if not 'eliteSkillLvl' in trap:
                                    if trap['hidden']:
                                        trap['eliteSkillLvl'] = trap['mainSkillLvl']
                                        trap['mainSkillLvl'] = item['mainSkillLvl']
                                    else:
                                        trap['eliteSkillLvl'] = item['mainSkillLvl']
                        else:
                            traps.append({
                                "key": key,
                                "level": item['inst']['level'],
                                "mainSkillLvl": item['mainSkillLvl'],
                                "hidden": item["hidden"],
                            })
            traps = [dict(t) for t in {tuple(d.items()) for d in traps}]
            for trap in traps:
                trap.pop('hidden', None)
            trimmed_stage_info['traps'] = traps

            enemy_list = extrainfo[levelId]['enemy_list'] if levelId in extrainfo else None
            elite_enemy_list = extrainfo[levelId]['elite_enemy_list'] if levelId in extrainfo else None
            enemies = []
            print(levelId)
            enemy_refs = stage_data["enemyDbRefs"]
            alt_data = None
            if levelId in STAGES_WITH_ENEMY_REF_TO_REPLACE:
                stage_data_path = os.path.join(
                    script_dir,
                    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{STAGES_WITH_ENEMY_REF_TO_REPLACE[levelId]}.json",
                )
                with open(stage_data_path, encoding="utf-8") as f:
                    alt_data = json.load(f)
                enemy_refs = alt_data["enemyDbRefs"]
            refs_to_ignore = []
            if levelId in STAGES_WITH_ENEMY_REF_TO_IGNORE:
                refs_to_ignore = STAGES_WITH_ENEMY_REF_TO_IGNORE[levelId]
            for enemy in enemy_refs:
                enemy_id = enemy['id']
                if enemy_id in refs_to_ignore:
                    continue
                if enemy_id == 'enemy_2062_smcar':
                    continue
                if enemy['useDb'] is False and not levelId in ['level_rogue2_b-7', 'level_rogue2_ev-3']:
                    enemy_id = enemy["overwrittenData"]['prefabKey']['m_value']
                if enemy_id in my_enemy_db:
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
                        if enemy["overwrittenData"]["levelType"]["m_defined"]:
                            overwrittenData["levelType"] = enemy["overwrittenData"][
                                "levelType"
                            ]["m_value"]
                        if enemy['overwrittenData']['talentBlackboard'] or enemy['overwrittenData']['skills']:
                            if levelId not in talent_overwrite_list and enemy['id'] != 'enemy_1106_byokai_b':
                                print(
                                    'talent overwrite', enemy['id'], my_enemy_db[enemy_id]['name_zh'], levelId)
                            if enemy['id'] == 'enemy_1106_byokai_b' and folder == 'ro3':
                                overwrittenData['talentBlackboard'] = talent_overwrite_list['rogue_3'][enemy['id']]
                            elif levelId in talent_overwrite_list and enemy['id'] in talent_overwrite_list[levelId]:
                                overwrittenData['talentBlackboard'] = talent_overwrite_list[levelId][enemy['id']]
                        if enemy['overwrittenData']['talentBlackboard']:
                            for item in enemy['overwrittenData']['talentBlackboard']:
                                if item['key'] == 'parasitic' and item['valueStr'] == "true":
                                    if not 'talentBlackboard' in overwrittenData:
                                        overwrittenData['talentBlackboard'] = [
                                        ]
                                    overwrittenData['talentBlackboard'].append(
                                        {"key": "parasitic"})
                    # if levelId == 'level_rogue4_2-7' and (enemy['id'] == 'enemy_10003_trwlpl' or enemy['id'] == 'enemy_10003_trwlpl_2'):
                    #     overwrittenData['talentBlackboard'] = talent_overwrite_list[levelId][enemy['id']]
                    if len(overwrittenData) == 0:
                        overwrittenData = None
                    '''
                    LOGIC FOR ENEMY LIST
                    if elite_enemy_list is none, just take enemy_list
                    '''
                    min_count = 0
                    max_count = 0
                    elite_min_count = 0
                    elite_max_count = 0
                    if enemy_list is not None:
                        for enemy_info in enemy_list:
                            if enemy_info['key'] == enemy['id']:
                                min_count = enemy_info['min_count']
                                max_count = enemy_info['max_count']
                    if elite_enemy_list is not None:
                        for elite_enemy_info in elite_enemy_list:
                            if elite_enemy_info['key'] == enemy['id']:
                                elite_min_count = elite_enemy_info['min_count']
                                elite_max_count = elite_enemy_info['max_count']
                    else:
                        elite_min_count = min_count
                        elite_max_count = max_count
                    enemies.append(
                        {
                            "id": enemy['id'],
                            'prefabKey': enemy_id,
                            "level": enemy["level"],
                            "min_count": min_count,
                            "max_count": max_count,
                            "elite_min_count": elite_min_count,
                            "elite_max_count": elite_max_count,
                            "overwrittenData": overwrittenData,
                        }
                    )

            trimmed_stage_info["enemies"] = enemies
            map_waves_data = get_waves_data(
                alt_data or stage_data, levelId, log=False)
            trimmed_stage_info.update(map_waves_data)
            data[levelId] = trimmed_stage_info
            stages_list.append(trimmed_stage_info)

# for stage navigation...
for topic_dict in roguelike_topics:
    stage_nav = {}
    write_path = os.path.join(
        script_dir, topic_dict['folder']+".json")
    rogue_topic = get_rogue_topic(topic_dict['folder'])
    for stage in stages_list:
        if rogue_topic in stage['tags']:
            stage_nav[stage['name_zh']] = {
                "levelId": stage['levelId'],
                "code": stage['code'],
                "name_zh": stage['name_zh'],
                "name_ja": stage['name_ja'],
                "name_en": stage['name_en'],
            }
    with open(write_path, 'w+', encoding='utf-8') as f:
        json.dump(stage_nav, f, ensure_ascii=False, indent=4)


for levelId in data:
    write_path = os.path.join(
        script_dir, 'ro_stage_data', levelId+".json")
    with open(write_path, 'w+', encoding='utf-8') as f:
        json.dump(data[levelId], f, ensure_ascii=False, indent=4)

# with open("is_stages_list_read.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)


# with open("is_stages_list.json", "w", encoding="utf-8") as f:
#     json.dump(stages_list, f, ensure_ascii=False, separators=(',', ':'))

with open("stage_name_lookup_table.json", "w", encoding="utf-8") as f:
    json.dump(stage_name_lookup, f, ensure_ascii=False, indent=4)
