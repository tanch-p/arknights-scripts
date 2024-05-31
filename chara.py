import json
import os
from chara_skills import replace_substrings

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

stat_convert = {'maxHp': "hp", "magicResistance": "res", "attackSpeed": "aspd",
                "moveSpeed": "ms", "respawnTime": "respawnTime", "atk": 'atk', "def": "def", "cost": "cost"}

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json")
en_char_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/character_table.json")
jp_char_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/character_table.json")
cn_patch_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/char_patch_table.json")
en_patch_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/char_patch_table.json")
jp_patch_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/char_patch_table.json")

with open(cn_char_table_path, encoding='utf-8') as f:
    cn_char_table = json.load(f)
with open(cn_skill_table_path, encoding='utf-8') as f:
    cn_skill_table = json.load(f)
with open(en_char_table_path, encoding='utf-8') as f:
    en_char_table = json.load(f)
with open(jp_char_table_path, encoding='utf-8') as f:
    jp_char_table = json.load(f)
with open(cn_patch_table_path, encoding='utf-8') as f:
    cn_patch_table = json.load(f)
with open(en_patch_table_path, encoding='utf-8') as f:
    en_patch_table = json.load(f)
with open(jp_patch_table_path, encoding='utf-8') as f:
    jp_patch_table = json.load(f)

with open('chara_skills.json', encoding='utf-8') as f:
    chara_skills = json.load(f)
with open('chara_talents.json', encoding='utf-8') as f:
    chara_talents = json.load(f)
with open('uniequip.json', encoding='utf-8') as f:
    uniequip_dict = json.load(f)
with open('tokens.json', encoding='utf-8') as f:
    tokens_dict = json.load(f)
data = []

filtered_cn_char_table = {key: cn_char_table[key] for key in cn_char_table.keys(
) if not "token" in key and not "trap" in key and key != "char_512_aprot"}

subProfessionIds = []

for id in filtered_cn_char_table:
    character_dict = filtered_cn_char_table[id]
    if character_dict['subProfessionId'] not in subProfessionIds:
        subProfessionIds.append(character_dict['subProfessionId'])
    skills = []
    talents = []
    for skill in character_dict['skills']:
        blackboard = chara_skills[skill['skillId']
                                  ]['blackboard'] if skill['skillId'] in chara_skills else []
        skills.append({"skillId": skill['skillId'],
                       "name_zh": chara_skills[skill['skillId']]['name_zh'],
                       "name_ja": chara_skills[skill['skillId']]['name_ja'],
                       "name_en": chara_skills[skill['skillId']]['name_en'],
                       "skillType": chara_skills[skill['skillId']]['skillType'],
                       "durationType": chara_skills[skill['skillId']]['durationType'],
                       'spType': chara_skills[skill['skillId']]['spType'],
                       "levels": chara_skills[skill['skillId']]['levels'],
                       "tags": chara_skills[skill['skillId']]['tags'] if skill['skillId'] in chara_skills else [],
                       "blackboard": blackboard})
    if character_dict['talents']:
        for talent_index, talent in enumerate(character_dict['talents']):
            max_candidate_index = len(talent['candidates'])-1
            maxed_talent = talent['candidates'][max_candidate_index]
            talent_holder = {
                "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                "desc_zh": chara_talents[id]['talents'][talent_index]["desc_zh"] if id in chara_talents else maxed_talent['description'], "desc_en": "", "desc_ja": ""}
            if id in en_char_table:
                talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_en"] = chara_talents[id]['talents'][talent_index]["desc_en"]
                talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_ja"] = chara_talents[id]['talents'][talent_index]["desc_ja"]
            talent_holder['tags'] = chara_talents[id]['talents'][talent_index]['tags'] if id in chara_talents else []
            talent_holder['blackboard'] = chara_talents[id]['talents'][talent_index]['blackboard'] if id in chara_talents else []
            talents.append(talent_holder)

    uniequip_list = []
    for equip_id in uniequip_dict:
        if uniequip_dict[equip_id]['charId'] == id:
            uniequip_list.append(uniequip_dict[equip_id])
    uniequip_list.sort(key=lambda equip: equip['uniEquipId'])
    stats = {}
    stats['rangeId'] = character_dict['phases'][-1]['rangeId']
    stats['level'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['level']
    stats['hp'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["maxHp"]
    stats['atk'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["atk"]
    stats['def'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["def"]
    stats['res'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["magicResistance"]
    stats['cost'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["cost"]
    stats['blockCnt'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["blockCnt"]
    stats['aspd'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["baseAttackTime"]
    stats['respawnTime'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["respawnTime"]

    potential = []
    attribute_translate_table = {'COST': "cost", "RESPAWN_TIME": 'respawnTime', 'ATK': "atk",
                                 "MAX_HP": "hp", "ATTACK_SPEED": "aspd", "DEF": "def", "MAGIC_RESISTANCE": "res"}

    # potential
    for idx, pot in enumerate(character_dict['potentialRanks']):
        pot_dict = {
            "desc_zh": pot['description'],
            'desc_ja': jp_char_table[id]['potentialRanks'][idx]['description'] if id in en_char_table and idx < len(jp_char_table[id]['potentialRanks']) else "",
            'desc_en': en_char_table[id]['potentialRanks'][idx]['description'] if id in en_char_table and idx < len(jp_char_table[id]['potentialRanks']) else ""
        }

        attribute = {attribute_translate_table[pot['buff']['attributes']['attributeModifiers'][0]['attributeType']]: pot['buff']['attributes']['attributeModifiers'][0]['value']}if pot['buff'] else None
        pot_dict['attribute'] = attribute
        potential.append(pot_dict)

    # trust/favor
    favor_data = {}
    if character_dict['favorKeyFrames'] is not None:
        for key in character_dict['favorKeyFrames'][-1]['data']:
            if bool(character_dict['favorKeyFrames'][-1]['data'][key]):
                favor_data[stat_convert[key]
                           ] = character_dict['favorKeyFrames'][-1]['data'][key]

    # tokens
    tokens = []
    if character_dict['displayTokenDict'] is not None:
        tokens = [tokens_dict[key]
                  for key in character_dict['displayTokenDict']]

    # subprofession stuff
    desc_zh = character_dict['description'].replace("<$ba", "<ba")
    blackboard = []
    tags = []
    if character_dict['subProfessionId'] == "slower":
        blackboard.append({"key": "sluggish", "value": 0.8})
    if character_dict['subProfessionId'] == "chain":
        blackboard.append({"key": "sluggish", "value": 0.5})
    if character_dict['subProfessionId'] == "stalker":
        blackboard.append({"key": "phys_evasion", "value": 0.5})
        blackboard.append({"key": "arts_evasion", "value": 0.5})
        tags.append("lower_target_priority")
    if character_dict['subProfessionId'] == "loopshooter":
        tags.append("aspd_unrelated")
    if character_dict['subProfessionId'] == "fastshot":
        tags.append("priority_flying")
    if character_dict['subProfessionId'] == "longrange":
        tags.append("priority_low_def")
    if character_dict['subProfessionId'] == "siegesniper":
        tags.append("priority_highest_weight")
    if character_dict["subProfessionId"] == "librator" or character_dict['subProfessionId'] == "healer":
        tags.append("block_0")
        desc_zh = replace_substrings(
            character_dict['trait']['candidates'][-1]['overrideDescripton'], character_dict['trait']['candidates'][-1]['blackboard'])
    if character_dict['subProfessionId'] in ["executor", "merchant", "agent"] and id != "char_376_therex":
        tags.append("fast_redeploy")
    if character_dict['subProfessionId'] in ["pusher", "hookmaster"]:
        tags.append("position_all")
    if character_dict['subProfessionId'] in ["unyield", "musha"]:
        tags.append("no_healing")

    return_dict = {"id": id, "appellation": character_dict['appellation'], "name_zh": character_dict['name'], "name_ja": "", "name_en": "",
                   "desc_zh": desc_zh, "desc_ja": "", "desc_en": "",
                   "tags": tags, "blackboard": blackboard,
                   "nationId": character_dict['nationId'], "groupId": character_dict['groupId'], "teamId": character_dict['teamId'], "position": character_dict['position'],
                   "isSpChar": character_dict['isSpChar'], "rarity": character_dict['rarity'],
                   "profession": character_dict['profession'], "subProfessionId": character_dict['subProfessionId'], "stats": stats,
                   'potential': potential, "favorData": favor_data, "tokens": tokens,
                   "skills": skills, "talents": talents, 'uniequip': uniequip_list, }
    if id in en_char_table:
        desc_en = en_char_table[id]['description'].replace(
            "<$ba", "<ba")
        desc_ja = jp_char_table[id]['description'].replace(
            "<$ba", "<ba")
        if character_dict["subProfessionId"] == "librator" or character_dict['subProfessionId'] == "healer":
            desc_en = replace_substrings(
                en_char_table[id]['trait']['candidates'][-1]['overrideDescripton'], en_char_table[id]['trait']['candidates'][-1]['blackboard'])
            desc_ja = replace_substrings(
                jp_char_table[id]['trait']['candidates'][-1]['overrideDescripton'], jp_char_table[id]['trait']['candidates'][-1]['blackboard'])

        return_dict['name_ja'] = jp_char_table[id]['name']
        return_dict['name_en'] = en_char_table[id]['name']
        return_dict['desc_ja'] = desc_ja
        return_dict['desc_en'] = desc_en
    data.append(return_dict)

# patch table for amiya
for id in cn_patch_table['patchChars']:
    character_dict = cn_patch_table['patchChars'][id]
    in_global = id in en_patch_table['patchChars']
    skills = []
    talents = []
    for skill in character_dict['skills']:
        blackboard = chara_skills[skill['skillId']
                                  ]['blackboard'] if skill['skillId'] in chara_skills else []
        levels = chara_skills[skill['skillId']]['levels']
        for level in levels:
            del level['blackboard']
        skills.append({"skillId": skill['skillId'],
                       "name_zh": chara_skills[skill['skillId']]['name_zh'],
                       "name_ja": chara_skills[skill['skillId']]['name_ja'],
                       "name_en": chara_skills[skill['skillId']]['name_en'],
                       "skillType": chara_skills[skill['skillId']]['skillType'],
                       "durationType": chara_skills[skill['skillId']]['durationType'],
                       'spType': chara_skills[skill['skillId']]['spType'],
                       "levels": levels,
                       "tags": chara_skills[skill['skillId']]['tags'] if skill['skillId'] in chara_skills else [],
                       "blackboard": blackboard})
    if character_dict['talents']:
        for talent_index, talent in enumerate(character_dict['talents']):
            max_candidate_index = len(talent['candidates'])-1
            maxed_talent = talent['candidates'][max_candidate_index]
            talent_holder = {
                "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                "desc_zh": chara_talents[id]['talents'][talent_index]["desc_zh"] if id in chara_talents else maxed_talent['description'], "desc_en": "", "desc_ja": ""}
            if in_global:
                talent_holder["name_en"] = en_patch_table['patchChars'][id][
                    'talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_en"] = chara_talents[id]['talents'][talent_index]["desc_en"]
                talent_holder["name_ja"] = jp_patch_table['patchChars'][id][
                    'talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_ja"] = chara_talents[id]['talents'][talent_index]["desc_ja"]
            talent_holder['tags'] = chara_talents[id]['talents'][talent_index]['tags'] if id in chara_talents else []
            talent_holder['blackboard'] = chara_talents[id]['talents'][talent_index]['blackboard'] if id in chara_talents else []
            talents.append(talent_holder)

    uniequip_list = []
    for equip_id in uniequip_dict:
        if uniequip_dict[equip_id]['charId'] == id:
            uniequip_list.append(uniequip_dict[equip_id])
    uniequip_list.sort(key=lambda equip: equip['uniEquipId'])
    stats = {}
    stats['rangeId'] = character_dict['phases'][-1]['rangeId']
    stats['level'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['level']
    stats['hp'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["maxHp"]
    stats['atk'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["atk"]
    stats['def'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["def"]
    stats['res'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["magicResistance"]
    stats['cost'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["cost"]
    stats['blockCnt'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["blockCnt"]
    stats['aspd'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["baseAttackTime"]
    stats['respawnTime'] = character_dict['phases'][-1]['attributesKeyFrames'][-1]['data']["respawnTime"]

    potential = []
    attribute_translate_table = {'COST': "cost", "RESPAWN_TIME": 'respawnTime', 'ATK': "atk",
                                 "MAX_HP": "hp", "ATTACK_SPEED": "aspd", "DEF": "def", "MAGIC_RESISTANCE": "res"}

    # potential
    for idx, pot in enumerate(character_dict['potentialRanks']):
        pot_dict = {
            "desc_zh": pot['description'],
            'desc_ja': jp_patch_table['patchChars'][id]['potentialRanks'][idx]['description'] if in_global else "",
            'desc_en': en_patch_table['patchChars'][id]['potentialRanks'][idx]['description'] if in_global else ""
        }

        attribute = {attribute_translate_table[pot['buff']['attributes']['attributeModifiers'][0]['attributeType']]: pot['buff']['attributes']['attributeModifiers'][0]['value']}if pot['buff'] else None
        pot_dict['attribute'] = attribute
        potential.append(pot_dict)

    # trust/favor
    favor_data = {}
    if character_dict['favorKeyFrames'] is not None:
        for key in character_dict['favorKeyFrames'][-1]['data']:
            if bool(character_dict['favorKeyFrames'][-1]['data'][key]):
                favor_data[stat_convert[key]
                           ] = character_dict['favorKeyFrames'][-1]['data'][key]

    # tokens
    tokens = []
    if character_dict['displayTokenDict'] is not None:
        tokens = [tokens_dict[key]
                  for key in character_dict['displayTokenDict']]

    blackboard = []
    tags = []
    if character_dict['subProfessionId'] == "slower":
        blackboard.append({"key": "sluggish", "value": 0.8})

    return_dict = {"id": id, "appellation": character_dict['appellation'], "name_zh": character_dict['name'], "name_ja": "", "name_en": "",
                   "desc_zh": character_dict['description'].replace("<$ba", "<ba"), "desc_ja": "", "desc_en": "",
                   "tags": tags, "blackboard": blackboard,
                   "nationId": character_dict['nationId'], "groupId": character_dict['groupId'], "teamId": character_dict['teamId'], "position": character_dict['position'],
                   "isSpChar": character_dict['isSpChar'], "rarity": character_dict['rarity'],
                   "profession": character_dict['profession'], "subProfessionId": character_dict['subProfessionId'], "stats": stats,
                   'potential': potential,  "favorData": favor_data, "tokens": tokens,
                   "skills": skills, "talents": talents, 'uniequip': uniequip_list}
    if in_global:
        return_dict['name_ja'] = jp_patch_table['patchChars'][id]['name']
        return_dict['name_en'] = en_patch_table['patchChars'][id]['name']
        return_dict['desc_ja'] = jp_patch_table['patchChars'][id]['description'].replace(
            "<$ba", "<ba")
        return_dict['desc_en'] = en_patch_table['patchChars'][id]['description'].replace(
            "<$ba", "<ba")
    data.append(return_dict)

with open('characters_read.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open('characters.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


# append new charas to char talent tags json
    new_chara_list = [id for id in dict.keys(
        filtered_cn_char_table) if id not in set(dict.keys(chara_talents))]
    return_dict = {}
    for id in new_chara_list:
        talents = []
        if filtered_cn_char_table[id]['talents']:
            for talent_index, talent in enumerate(filtered_cn_char_table[id]['talents']):
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder = {
                    "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                    "desc_zh": replace_substrings(maxed_talent["description"], maxed_talent['blackboard']), "desc_ja": "", "desc_en": "", "tags": [], "blackboard": maxed_talent['blackboard']}
                if id in en_char_table:
                    talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["desc_ja"] = replace_substrings(
                        jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
                    talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["desc_en"] = replace_substrings(en_char_table[id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
                talents.append(talent_holder)
        return_dict[id] = {
            "appellation": filtered_cn_char_table[id]['appellation'], "talents": talents}

    # char patch table
    new_chara_list = [id for id in dict.keys(
        cn_patch_table['patchChars']) if id not in set(dict.keys(chara_talents))]
    for id in new_chara_list:
        talents = []
        if cn_patch_table['patchChars'][id]['talents']:
            for talent_index, talent in enumerate(cn_patch_table['patchChars'][id]['talents']):
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder = {
                    "prefabKey": maxed_talent["prefabKey"], "name_zh": maxed_talent["name"], "name_en": "", "name_ja": "",
                    "desc_zh": maxed_talent["description"], "desc_ja": "", "desc_en": "", "tags": [], "blackboard": maxed_talent['blackboard']}
                if id in en_patch_table['patchChars']:
                    talent_holder["name_ja"] = jp_patch_table['patchChars'][id][
                        'talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["desc_ja"] = jp_patch_table['patchChars'][id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                    talent_holder["name_en"] = en_patch_table['patchChars'][id][
                        'talents'][talent_index]['candidates'][max_candidate_index]["name"]
                    talent_holder["desc_en"] = en_patch_table['patchChars'][id]['talents'][
                        talent_index]['candidates'][max_candidate_index]["description"]
                talents.append(talent_holder)
        return_dict[id] = {
            "appellation": cn_patch_table['patchChars'][id]['appellation'], "talents": talents}
    return_dict = chara_talents | return_dict

with open('chara_talents.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)

print(subProfessionIds)

# schema has to take care of the following requirements:
# can affect air? target ground? enemy types
# roguelike artifacts
# summons
# values with a range will always take minimum
# probability
# condition
