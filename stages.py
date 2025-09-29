import json
import os
from operator import itemgetter
from waves_new import get_waves_data, get_runes_data, get_wave_spawns_data
from tiles import get_list_of_tiles, get_special_tiles


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

TRAPS_TO_EXCLUDE = ["trap_042_tidectrl", "trap_061_creep", "trap_062_magicstart",
                    "trap_063_magicturn", "trap_050_blizzard", "trap_092_vgctrl",
                    "trap_036_storm", "trap_162_lrctrl", "trap_766_duelwal",
                    "trap_767_duelcdt", "trap_106_smtree", 'trap_251_buftrp', 'trap_239_dyffgd', 'trap_240_dyffdd']
ENEMIES_TO_IGNORE = ['enemy_2086_skzdwx', 'enemy_2087_skzdwy',
                     'enemy_2088_skzdwz', 'enemy_2062_smcar']
STAGES_WITH_ENEMY_REF_TO_IGNORE = {"level_rogue1_4-2": ["enemy_1025_reveng_2"],
                                   "level_rogue4_b-8": ["enemy_3001_upeopl", 'enemy_2093_skzams'],
                                   "level_rogue4_4-4": ["enemy_1221_dzomg_b", "enemy_1220_dzoms_b"],
                                   "level_rogue3_b-4-b": ["enemy_2054_smdeer"],
                                   "level_rogue4_3-2": ["enemy_1271_nhkodo_a"],
                                   "level_rogue5_b-4": ["enemy_1128_spmage_2"]}
STAGES_TO_SKIP = ['ro4_b_4_c', 'ro4_b_4_d', 'ro4_b_5_c', 'ro4_b_5_d']
STAGES_WITH_REF_TO_REPLACE = {'level_rogue4_b-4': 'level_rogue4_b-4-c',
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
                              'level_rogue4_2-6': 'levelreplacers/level_rogue4_2-6_r1',
                              'level_rogue4_3-1': 'levelreplacers/level_rogue4_3-1_r2',
                              'level_rogue4_3-2': 'levelreplacers/level_rogue4_3-2_r2',
                              'level_rogue4_3-3': 'levelreplacers/level_rogue4_3-3_r2',
                              'level_rogue4_3-4': 'levelreplacers/level_rogue4_3-4_r2',
                              'level_rogue4_3-5': 'levelreplacers/level_rogue4_3-5_r2',
                              'level_rogue4_3-6': 'levelreplacers/level_rogue4_3-6_r2',
                              'level_rogue4_3-7': 'levelreplacers/level_rogue4_3-7_r1',
                              'level_rogue4_4-1': 'levelreplacers/level_rogue4_4-1_r2',
                              'level_rogue4_4-2': 'levelreplacers/level_rogue4_4-2_r2',
                              'level_rogue4_4-3': 'levelreplacers/level_rogue4_4-3_r2',
                              'level_rogue4_4-4': 'levelreplacers/level_rogue4_4-4_r2',
                              'level_rogue4_4-5': 'levelreplacers/level_rogue4_4-5_r2',
                              'level_rogue4_4-6': 'levelreplacers/level_rogue4_4-6_r2',
                              'level_rogue4_4-7': 'levelreplacers/level_rogue4_4-7_r2',
                              'level_rogue4_4-8': 'levelreplacers/level_rogue4_4-8_r1',
                              'level_rogue4_4-9': 'levelreplacers/level_rogue4_4-9_r1',
                              'level_rogue4_5-1': 'levelreplacers/level_rogue4_5-1_r2',
                              'level_rogue4_5-2': 'levelreplacers/level_rogue4_5-2_r2',
                              'level_rogue4_5-3': 'levelreplacers/level_rogue4_5-3_r2',
                              'level_rogue4_5-4': 'levelreplacers/level_rogue4_5-4_r2',
                              'level_rogue4_5-5': 'levelreplacers/level_rogue4_5-5_r2',
                              'level_rogue4_5-6': 'levelreplacers/level_rogue4_5-6_r2',
                              'level_rogue4_5-7': 'levelreplacers/level_rogue4_5-7_r2',
                              'level_rogue4_5-8': 'levelreplacers/level_rogue4_5-8_r1',
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
STAGES_WITH_NAME_TO_REPLACE = {

}


def is_unhandled_alert(levelId, key, rogue_topic):
    levels_to_ignore = ['level_rogue1_1-5', 'level_rogue2_b-7', 'level_rogue3_3-4', 'level_rogue3_4-3' 'level_rogue4_5-1',
                        'level_rogue4_t-5', 'level_rogue4_6-1', 'level_rogue4_7-1', 'level_rogue4_b-2-c']
    if levelId in levels_to_ignore:
        return False
    if rogue_topic == "ro3" and key == "enemy_1106_byokai":
        return False
    return True


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

enemy_database_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
with open("talent_overwrite_list.json", encoding="utf-8") as f:
    talent_overwrite_list = json.load(f)
with open(enemy_database_path, encoding="utf-8") as f:
    enemy_database = json.load(f)
with open("enemy_database.json", encoding="utf-8") as f:
    my_enemy_db = json.load(f)
with open("stage_name_overwrite_table.json", encoding="utf-8") as f:
    stage_name_overwrite_table = json.load(f)

alerts = []


def get_rogue_topic(folder):
    if folder == "ro1":
        return 'rogue_phantom'
    if folder == "ro2":
        return 'rogue_mizuki'
    if folder == "ro3":
        return 'rogue_sami'
    if folder == "ro4":
        return 'rogue_skz'
    if folder == "ro5":
        return 'rogue_yan'


def get_trimmed_stage_data(stage_data, meta_info, extrainfo, rogue_topic=None):
    levelId = meta_info['levelId']

    wave_data = get_wave_spawns_data(stage_data, levelId, log=True)
    enemy_list, elite_enemy_list = itemgetter(
        "enemy_list", "elite_enemy_list")(wave_data)
    sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
    sp_terrain = sp_tiles
    if sp_terrain is not None and len(sp_terrain) == 0:
        sp_terrain = None

    trimmed_stage_info = {
        "id": meta_info["id"],
        "levelId": levelId,
        "tags": stage_data["mapData"]["tags"],
        "category": extrainfo[levelId].get('category', None) if levelId in extrainfo else None,
        "characterLimit": stage_data["options"]["characterLimit"],
        "initialCost": stage_data["options"]["initialCost"],
        "maxCost": 99,
        "costIncreaseTime": stage_data["options"]["costIncreaseTime"],
        "code": meta_info["code"],
        "name_zh":  meta_info["name_zh"],
        "name_ja": meta_info["name_ja"],
        "name_en": meta_info["name_en"],
        "description_zh": meta_info["description_zh"],
        "description_ja": meta_info["description_ja"],
        "description_en": meta_info["description_en"],
        "addInfo_zh": replace_chevrons(extrainfo[levelId].get('addInfo_zh', None)) if levelId in extrainfo else None,
        "addInfo_ja": replace_chevrons(extrainfo[levelId].get('addInfo_ja', None)) if levelId in extrainfo else None,
        "addInfo_en": replace_chevrons(extrainfo[levelId].get('addInfo_en', None)) if levelId in extrainfo else None,
        "eliteDesc_zh":  replace_chevrons(extrainfo[levelId].get('eliteDesc_zh', None)) if levelId in extrainfo else None,
        "eliteDesc_ja": replace_chevrons(extrainfo[levelId].get('eliteDesc_ja', None)) if levelId in extrainfo else None,
        "eliteDesc_en": replace_chevrons(extrainfo[levelId].get('eliteDesc_en', None)) if levelId in extrainfo else None,
        "all_mods": extrainfo[levelId].get('all_mods', None) if levelId in extrainfo else None,
        "n_mods": extrainfo[levelId].get('normal_mods', None) if levelId in extrainfo else None,
        "elite_mods": extrainfo[levelId].get('elite_mods', None) if levelId in extrainfo else None,
        "floors": extrainfo[levelId].get('floors', None) if levelId in extrainfo else None,
        "sp_terrain": sp_terrain,
        "sp_enemy": extrainfo[levelId].get('sp_enemy', None) if levelId in extrainfo else None,
        "n_count": extrainfo[levelId].get('enemy_counts', None) if levelId in extrainfo else None,
        "e_count": extrainfo[levelId].get('elite_enemy_counts', None) if levelId in extrainfo else None,
        "traps": []
    }

    # runes
    holder = {}
    normal_group_name, elite_group_name, enemies_to_replace, predefine_changes, forbid_locations, max_cost = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace', 'predefine_changes', 'forbid_locations', 'max_cost')(get_runes_data(stage_data['runes'], levelId, stage_data['mapData']))
    if len(enemies_to_replace) > 0:
        holder['enemy_replace'] = enemies_to_replace
    if len(predefine_changes) > 0:
        holder['predefine_changes'] = predefine_changes
    if len(forbid_locations) > 0:
        holder['forbid_locations'] = forbid_locations
    if len(holder) > 0:
        trimmed_stage_info['elite_runes'] = holder
    trimmed_stage_info['maxCost'] = max_cost
    traps = []
    token_cards = []
    systems = {}

    # handle level_predefine_tokens_random_spawn_on_tile in ro5
    # currently all level_predefine_tokens_random_spawn_on_tile have difficultyMask ALL
    if rogue_topic == 'ro5' and stage_data['runes']:
        if levelId not in ['level_rogue5_t-6']:
            for rune in stage_data['runes']:
                if rune['key'] == 'level_predefine_tokens_random_spawn_on_tile':
                    targets = next(
                        (item['valueStr'] for item in rune['blackboard'] if item['key'] == 'token_key'), None)
                    if targets is not None:
                        targets = targets.split("|")
                    tiles_keys = next(
                        (item['valueStr'] for item in rune['blackboard'] if item['key'] == 'tile'), None)
                    if tiles_keys is not None:
                        tiles_keys = tiles_keys.split("|")
                        for tile_key in tiles_keys:
                            tile_list = get_list_of_tiles(stage_data, tile_key)
                            if len(tile_list) > 0:
                                if not rune['key'] in systems:
                                    systems[rune['key']] = {'tiles': {}}
                                if not tile_key in systems[rune['key']]['tiles']:
                                    systems[rune['key']]['tiles'][tile_key] = [
                                        {"pos": tile['position'],
                                         "blackboard": tile['blackboard']} for tile in tile_list]
                                for target in targets:
                                    systems[rune['key']][target] = tiles_keys

    if stage_data['predefines']:
        for item in stage_data['predefines']['tokenInsts']:
            key = item['inst']['characterKey']
            if not key in TRAPS_TO_EXCLUDE:
                traps.append({
                    "key": key,
                    "alias": item['alias'],
                    "pos": item['position'],
                    "direction": item['direction'],
                    "level": item['inst']['level'],
                    'skillIndex': item['skillIndex'],
                    "mainSkillLvl": item['mainSkillLvl'],
                    "hidden": item["hidden"],
                    "overrideSkillBlackboard": item["overrideSkillBlackboard"] if 'overrideSkillBlackboard' in item else None
                })
        for item in stage_data['predefines']['tokenCards']:
            if item['hidden']:
                continue
            token_cards.append({
                "key":  item['inst']['characterKey'],
                "count": item['initialCnt']
            })
    trimmed_stage_info['traps'] = traps
    trimmed_stage_info['token_cards'] = token_cards
    trimmed_stage_info['systems'] = systems

    enemies = []
    enemy_refs = stage_data["enemyDbRefs"]
    alt_data = None
    if levelId in STAGES_WITH_REF_TO_REPLACE:
        stage_data_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{rogue_topic}/{STAGES_WITH_REF_TO_REPLACE[levelId]}.json",
        )
        with open(stage_data_path, encoding="utf-8") as f:
            alt_data = json.load(f)
        enemy_refs = alt_data["enemyDbRefs"]
    refs_to_ignore = []
    if levelId in STAGES_WITH_ENEMY_REF_TO_IGNORE:
        refs_to_ignore = STAGES_WITH_ENEMY_REF_TO_IGNORE[levelId]
    for enemy in enemy_refs:
        enemy_id = enemy['id']
        if enemy_id in ENEMIES_TO_IGNORE or enemy_id in refs_to_ignore:
            continue
        if enemy['useDb'] is False:
            enemy_id = enemy["overwrittenData"]['prefabKey']['m_value']
            if not (levelId in talent_overwrite_list and enemy['id'] in talent_overwrite_list[levelId]):
                if is_unhandled_alert(levelId, enemy_id, rogue_topic):
                    alerts.append(f"useDb is False {enemy['id']} in {levelId}")
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
                if 'notCountInTotal' in enemy["overwrittenData"] and enemy["overwrittenData"]["notCountInTotal"]["m_defined"] and enemy["overwrittenData"]["notCountInTotal"]["m_value"]:
                    if my_enemy_db[enemy_id]['notCountInTotal'] is False:
                        overwrittenData['notCountInTotal'] = True
                        alerts.append(
                            f"notCountInTotal, {enemy['id']}, {my_enemy_db[enemy_id]['name_zh']}, {levelId})")
                        if not 'talentBlackboard' in overwrittenData:
                            overwrittenData['talentBlackboard'] = []
                        overwrittenData['talentBlackboard'].append(
                            {"key": "not_count_in_total", "tooltip": {
                                "en": ["$【Non-Key Target】$Will not prevent ending of battle even when still on field"],
                                "ja": ["$【非重要目標】$戦場にいても作戦終了に影響しない"],
                                "zh": ["$【非首要目标】$该目标在场不会阻止战斗结束"]
                            }})
                if enemy["overwrittenData"]["rangeRadius"]["m_defined"]:
                    overwrittenData["range"] = enemy["overwrittenData"][
                        "rangeRadius"
                    ]["m_value"]
                if "levelType" in enemy["overwrittenData"] and enemy["overwrittenData"]["levelType"]["m_defined"]:
                    overwrittenData["levelType"] = enemy["overwrittenData"][
                        "levelType"
                    ]["m_value"]
                if levelId in talent_overwrite_list and enemy['id'] in talent_overwrite_list[levelId]:
                    if not 'talentBlackboard' in overwrittenData:
                        overwrittenData['talentBlackboard'] = []
                    overwrittenData['talentBlackboard'] += talent_overwrite_list[levelId][enemy['id']]
                elif enemy['overwrittenData']['talentBlackboard'] or enemy['overwrittenData']['skills']:
                    if levelId not in talent_overwrite_list and enemy['id'] != 'enemy_1106_byokai_b':
                        if is_unhandled_alert(levelId, enemy_id, rogue_topic):
                            alerts.append(
                                f"talent overwrite, {enemy['id']}, {my_enemy_db[enemy_id]['name_zh']}, {levelId})")

                    if enemy['id'] == 'enemy_1106_byokai_b' and rogue_topic == 'ro3':
                        overwrittenData['talentBlackboard'] = talent_overwrite_list['rogue_3'][enemy['id']]

                if enemy['overwrittenData']['talentBlackboard']:
                    if not 'talentBlackboard' in overwrittenData:
                        overwrittenData['talentBlackboard'] = []
                    for item in enemy['overwrittenData']['talentBlackboard']:
                        if item['key'].casefold() == 'yinyang.dynamic' and item['value'] == 0:
                            overwrittenData['talentBlackboard'].append(
                                talent_overwrite_list['yinyang'])
                        elif levelId == 'level_rogue2_b-7' and item['key'] == 'Combat.enemy_key':
                            overwrittenData['talentBlackboard'].append(
                                {'key': "transform", "value": item['valueStr']})
                        elif levelId == 'level_rogue4_b-8' and item['key'] == 'summon.enemy_key':
                            overwrittenData['talentBlackboard'].append(
                                {'key': "transform", "value": item['valueStr']})
                        elif item['key'] == 'parasitic':
                            overwrittenData['talentBlackboard'].append(
                                {"key": "parasitic"})
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
    return trimmed_stage_info


def generate_roguelike_stages():
    cn_roguelike_topic_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
    )
    en_roguelike_topic_path = os.path.join(
        script_dir, "global_data/en_US/gamedata/excel/roguelike_topic_table.json"
    )
    jp_roguelike_topic_path = os.path.join(
        script_dir, "global_data/ja_JP/gamedata/excel/roguelike_topic_table.json"
    )

    with open(cn_roguelike_topic_path, encoding="utf-8") as f:
        cn_roguelike_topic_table = json.load(f)
    with open(en_roguelike_topic_path, encoding="utf-8") as f:
        en_roguelike_topic_table = json.load(f)
    with open(jp_roguelike_topic_path, encoding="utf-8") as f:
        jp_roguelike_topic_table = json.load(f)

    with open("is_stages_extrainfo.json", encoding="utf-8") as f:
        extrainfo = json.load(f)

    data = {}
    stage_name_lookup = {}
    stages_list = []
    roguelike_topics = [
        {"topic": "rogue_1", "folder": "ro1"},
        {"topic": "rogue_2", "folder": "ro2"},
        {"topic": "rogue_3", "folder": "ro3"},
        {"topic": "rogue_4", "folder": "ro4"},
        {"topic": "rogue_5", "folder": "ro5"},
    ]

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
                print(levelId)
                folder = topic_dict["folder"]
                stage_data_path = os.path.join(
                    script_dir,
                    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{levelId}.json",
                )
                with open(stage_data_path, encoding="utf-8") as f:
                    stage_data = json.load(f)

                # for reverse lookup in website
                rogue_topic = get_rogue_topic(folder)
                if levelId == 'level_rogue4_b-9':
                    url_key = 'ro4_b_9'
                    stage_name_lookup[url_key] = {
                        "lang": "ALL", "key": levelId, "topic": rogue_topic}
                else:
                    name_zh = stage_info_cn["name"]
                    name_ja = stage_info_jp["name"].replace(" ", "_")
                    name_en = stage_info_en["name"].replace(" ", "_")
                    if levelId in stage_name_overwrite_table:
                        name_zh = stage_name_overwrite_table[levelId]['name_zh']
                    zh_url_key = stage_info_cn["code"] + '_' + name_zh
                    stage_name_lookup[zh_url_key] = {
                        "lang": "zh", "key": levelId, "topic": rogue_topic}
                    if TOPIC_IN_GLOBAL:
                        en_url_key = stage_info_en["code"] + '_' + name_en
                        ja_url_key = stage_info_jp["code"] + '_' + name_ja
                        stage_name_lookup[en_url_key] = {
                            "lang": "en", "key": levelId, "topic": rogue_topic}
                        stage_name_lookup[ja_url_key] = {
                            "lang": "ja", "key": levelId, "topic": rogue_topic}
                meta_info = {
                    "id": stage_info_cn["id"],
                    "levelId": levelId,
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
                }
                trimmed_stage_info = get_trimmed_stage_data(
                    stage_data, meta_info, extrainfo, folder)
                data[levelId] = trimmed_stage_info
                stages_list.append(trimmed_stage_info)

    # for stage navigation ro1 ro2 ro3...
    for topic_dict in roguelike_topics:
        stage_nav = {}
        write_path = os.path.join(
            script_dir, topic_dict['folder']+".json")
        rogue_topic = get_rogue_topic(topic_dict['folder'])
        for stage in stages_list:
            if rogue_topic in stage['tags']:
                stage_name = stage['name_zh']
                levelId = stage['levelId']
                if levelId in stage_name_overwrite_table:
                    info = stage_name_overwrite_table[levelId]
                    stage_nav[levelId] = {
                        "code": stage['code'],
                        "name_zh": info['name_zh'],
                        "name_ja": info['name_ja'],
                        "name_en": info['name_en'],
                    }
                else:
                    stage_nav[levelId] = {
                        "code": stage['code'],
                        "name_zh": stage_name,
                        "name_ja": stage['name_ja'],
                        "name_en": stage['name_en'],
                    }
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(stage_nav, f, ensure_ascii=False, indent=4)

    for levelId in data:
        write_path = os.path.join(
            script_dir, 'ro_stage_data', levelId+".json")
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(data[levelId], f, ensure_ascii=False, indent=1)

    # with open("is_stages_list_read.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    with open("is_stages_list.json", "w", encoding="utf-8") as f:
        json.dump(stages_list, f, ensure_ascii=False, separators=(',', ':'))

    with open("stage_name_lookup_table.json", "w", encoding="utf-8") as f:
        json.dump(stage_name_lookup, f, ensure_ascii=False, indent=4)


def generate_normal_stages(topic):
    cn_stage_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/stage_table.json"
    )
    en_stage_table_path = os.path.join(
        script_dir, "global_data/en_US/gamedata/excel/stage_table.json"
    )
    jp_stage_table_path = os.path.join(
        script_dir, "global_data/ja_JP/gamedata/excel/stage_table.json"
    )
    cn_zone_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/zone_table.json"
    )
    en_zone_table_path = os.path.join(
        script_dir, "global_data/en_US/gamedata/excel/zone_table.json"
    )
    jp_zone_table_path = os.path.join(
        script_dir, "global_data/ja_JP/gamedata/excel/zone_table.json"
    )
    cn_story_review_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/story_review_table.json"
    )
    en_story_review_table_path = os.path.join(
        script_dir, "global_data/en_US/gamedata/excel/story_review_table.json"
    )
    jp_story_review_table_path = os.path.join(
        script_dir, "global_data/ja_JP/gamedata/excel/story_review_table.json"
    )
    activity_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/activity_table.json"
    )

    with open(cn_stage_table_path, encoding="utf-8") as f:
        cn_stage_table = json.load(f)
    with open(en_stage_table_path, encoding="utf-8") as f:
        en_stage_table = json.load(f)
    with open(jp_stage_table_path, encoding="utf-8") as f:
        jp_stage_table = json.load(f)
    with open(cn_zone_table_path, encoding="utf-8") as f:
        cn_zone_table = json.load(f)
    with open(en_zone_table_path, encoding="utf-8") as f:
        en_zone_table = json.load(f)
    with open(jp_zone_table_path, encoding="utf-8") as f:
        jp_zone_table = json.load(f)
    with open(cn_story_review_table_path, encoding="utf-8") as f:
        cn_story_review_table = json.load(f)
    with open(en_story_review_table_path, encoding="utf-8") as f:
        en_story_review_table = json.load(f)
    with open(jp_story_review_table_path, encoding="utf-8") as f:
        jp_story_review_table = json.load(f)
    with open(activity_table_path, encoding="utf-8") as f:
        activity_table = json.load(f)

    data = {}
    activities_with_story = [id for id in cn_story_review_table if cn_story_review_table[id]['entryType'] in [
        'MAINLINE', 'ACTIVITY', 'MINI_ACTIVITY']]
    activities = []
    stages = {}

    for stageId in cn_stage_table['stages']:
        TOPIC_IN_GLOBAL = stageId in en_stage_table['stages']
        stage_info = cn_stage_table['stages'][stageId]
        if stage_info['isStoryOnly'] or stage_info['stageType'] in ['CLIMB_TOWER', 'CAMPAIGN', 'GUIDE']:
            # Ignore Climb tower for now
            continue
        if stage_info['difficulty'] != "NORMAL":
            continue
        if stage_info['appearanceStyle'] == "TRAINING":
            continue
        if 'multi' in stageId or 'easy' in stageId:
            continue
        activity_id = stage_info['zoneId']
        if stage_info['stageType'] == 'ACTIVITY':
            activity_id = activity_table['zoneToActivity'][activity_id] if activity_id in activity_table['zoneToActivity'] else None
            if not activity_id:
                activity_id = next(
                    (id for id in activities_with_story if id in stage_info['zoneId']), stage_info['zoneId'])
        item = next(
            (item for item in activities if item['id'] == activity_id), None)
        if not item:
            activities.append(
                {
                    "id": activity_id,
                    "type": stage_info['stageType'],
                    "name": {
                        "zh": cn_story_review_table[activity_id]['name'] if activity_id in cn_story_review_table else None,
                        "ja": jp_story_review_table[activity_id]['name'] if activity_id in jp_story_review_table else None,
                        "en": en_story_review_table[activity_id]['name'] if activity_id in en_story_review_table else None,
                    },
                    "zones": [

                    ]
                })
        file_path = stage_info['levelId'].lower()
        stage_data_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/{file_path}.json",
        )
        print(stageId)
        try:
            with open(stage_data_path, encoding="utf-8") as f:
                stage_data = json.load(f)
        except FileNotFoundError as e:
            print(f"{file_path} not found")
        if not stage_data:
            continue
        meta_info = {
            "id": stageId,
            "levelId": stageId,
            "code": stage_info['code'],
            "name_zh":  stage_info['name'],
            "name_ja":  jp_stage_table['stages'][stageId]['name'] if TOPIC_IN_GLOBAL else None,
            "name_en":  en_stage_table['stages'][stageId]['name'] if TOPIC_IN_GLOBAL else None,
            "description_zh": stage_info['description'].replace("\\n", "\n") if stage_info['description'] else None,
            "description_ja": jp_stage_table['stages'][stageId]['description'].replace("\\n", "\n")
            if TOPIC_IN_GLOBAL and stage_info['description']
            else None,
            "description_en": en_stage_table['stages'][stageId]['description'].replace("\\n", "\n")
            if TOPIC_IN_GLOBAL and stage_info['description']
            else None,
        }

        wave_data = get_wave_spawns_data(stage_data, stageId, log=True)
        enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
            "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
        sp_tiles = get_special_tiles(stage_data['mapData']['tiles'])
        sp_terrain = sp_tiles
        if sp_terrain is not None and len(sp_terrain) == 0:
            sp_terrain = None
        
        with open("activity_stages_extrainfo.json", encoding="utf-8") as f:
            extrainfo = json.load(f)

        trimmed_stage_info = get_trimmed_stage_data(
            stage_data, meta_info, extrainfo)
        data[stageId] = trimmed_stage_info
        zoneId = stage_info['zoneId']
        if not zoneId in stages:
            zone_in_global = zoneId in jp_zone_table['zones']
            zoneNameFirst = {
                "zh": cn_zone_table['zones'][zoneId]['zoneNameFirst'],
                "ja": jp_zone_table['zones'][zoneId]['zoneNameFirst'] if zone_in_global else None,
                "en": en_zone_table['zones'][zoneId]['zoneNameFirst'] if zone_in_global else None,
            }
            if zoneNameFirst['zh'] is None:
                zoneNameFirst = None
            zoneNameSecond = {
                "zh": cn_zone_table['zones'][zoneId]['zoneNameSecond'],
                "ja": jp_zone_table['zones'][zoneId]['zoneNameSecond'] if zone_in_global else None,
                "en": en_zone_table['zones'][zoneId]['zoneNameSecond'] if zone_in_global else None,
            }
            stages[zoneId] = {
                'zoneNameFirst': zoneNameFirst,
                'zoneNameSecond': zoneNameSecond,
                "stages": []
            }
        stages[zoneId]['stages'].append({
            "stageId": stageId,
            "code": stage_info['code'],
            "name": {
                "zh": stage_info['name'],
                "ja":  jp_stage_table['stages'][stageId]['name'] if TOPIC_IN_GLOBAL else None,
                "en":  en_stage_table['stages'][stageId]['name'] if TOPIC_IN_GLOBAL else None,
            }
        })
    for zoneId in stages:
        activity_id = activity_table['zoneToActivity'][zoneId] if zoneId in activity_table['zoneToActivity'] else None
        if not activity_id:
            activity_id = next(
                (id for id in activities_with_story if id in zoneId), zoneId)
        if activity_id:
            item = next(
                (item for item in activities if item['id'] == activity_id), None)
            if item:
                label = None
                if len(item['zones']) == 0:
                    label = 'n'
                elif len(item['zones']) == 1:
                    label = 'ex'
                elif len(item['zones']) == 2:
                    label = 's'
                elif len(item['zones']) == 3:
                    label = ''
                item['zones'].append({
                    "label": label,
                    "zoneId": zoneId,
                    'zoneNameFirst': stages[zoneId]['zoneNameFirst'],
                    'zoneNameSecond': stages[zoneId]['zoneNameSecond'],
                    "stages": stages[zoneId]['stages']
                })
    for stageId in data:
        write_path = os.path.join(
            script_dir, 'all_stage_data', stageId+".json")
        with open(write_path, 'w+', encoding='utf-8') as f:
            json.dump(data[stageId], f, ensure_ascii=False, indent=1)
    with open("all_stages_list.json", "w", encoding="utf-8") as f:
        json.dump(stages, f, ensure_ascii=False, indent=4)
    with open("activities_list.json", "w", encoding="utf-8") as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)


def main():
    option = input("Choose an option: \n1 for rogue\n2 for normal")
    if option == "1":
        generate_roguelike_stages()
    elif option == "2":
        generate_normal_stages()
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
