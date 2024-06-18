import json
import os
from chara_skills import replace_substrings

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

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
cn_patch_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/char_patch_table.json")
en_patch_table_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/char_patch_table.json")
jp_patch_table_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/char_patch_table.json")
cn_uniequip_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/uniequip_table.json")
cn_battle_equip_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/battle_equip_table.json")
jp_uniequip_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/uniequip_table.json")
jp_battle_equip_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/battle_equip_table.json")
en_uniequip_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/uniequip_table.json")
en_battle_equip_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/battle_equip_table.json")


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
with open(cn_patch_table_path, encoding='utf-8') as f:
    cn_patch_table = json.load(f)
with open(en_patch_table_path, encoding='utf-8') as f:
    en_patch_table = json.load(f)
with open(jp_patch_table_path, encoding='utf-8') as f:
    jp_patch_table = json.load(f)
with open(cn_uniequip_path, encoding='utf-8') as f:
    cn_uniequip_table = json.load(f)
with open(cn_battle_equip_path, encoding='utf-8') as f:
    cn_battle_equip_table = json.load(f)
with open(jp_uniequip_path, encoding='utf-8') as f:
    jp_uniequip_table = json.load(f)
with open(jp_battle_equip_path, encoding='utf-8') as f:
    jp_battle_equip_table = json.load(f)
with open(en_uniequip_path, encoding='utf-8') as f:
    en_uniequip_table = json.load(f)
with open(en_battle_equip_path, encoding='utf-8') as f:
    en_battle_equip_table = json.load(f)

with open('chara_skills.json', encoding='utf-8') as f:
    chara_skills = json.load(f)
with open('chara_talents.json', encoding='utf-8') as f:
    chara_talents = json.load(f)
with open('uniequip.json', encoding='utf-8') as f:
    curr_uniequip = json.load(f)

# talents
return_dict = {}
for id in chara_talents:
    levels_data = chara_talents[id]
    if not id in en_char_table:
        return_dict[id] = levels_data
        continue
    if en_char_table[id]['talents']:
        talents = []
        for talent_index, talent in enumerate(en_char_table[id]['talents']):
            talent_holder = chara_talents[id]['talents'][talent_index]
            if not talent_holder['name_en']:
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_ja"] = replace_substrings(
                    jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
                talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_en"] = replace_substrings(en_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
            talents.append(talent_holder)
    return_dict[id] = levels_data

for id in cn_patch_table['patchChars']:
    levels_data = chara_talents[id]
    if not id in en_patch_table['patchChars']:
        return_dict[id] = levels_data
        continue
    if en_patch_table['patchChars'][id]['talents']:
        talents = []
        for talent_index, talent in enumerate(en_patch_table['patchChars'][id]['talents']):
            talent_holder = chara_talents[id]['talents'][talent_index]
            if not talent_holder['name_en']:
                max_candidate_index = len(talent['candidates'])-1
                maxed_talent = talent['candidates'][max_candidate_index]
                talent_holder["name_ja"] = jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_ja"] = replace_substrings(
                    jp_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
                talent_holder["name_en"] = en_char_table[id]['talents'][talent_index]['candidates'][max_candidate_index]["name"]
                talent_holder["desc_en"] = replace_substrings(en_char_table[id]['talents'][
                    talent_index]['candidates'][max_candidate_index]["description"], maxed_talent['blackboard'])
            talents.append(talent_holder)
    return_dict[id] = levels_data

with open('chara_talents.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)


# skills
return_dict = {}
for skill_id in chara_skills:
    data = chara_skills[skill_id]
    if not skill_id in en_skill_table:
        return_dict[skill_id] = data
        continue
    data['name_ja'] = jp_skill_table[skill_id]['levels'][0]['name']
    data['name_en'] = en_skill_table[skill_id]['levels'][0]['name']
    levels = chara_skills[skill_id]['levels']
    if len(levels) > 6:
        l7 = levels[6]
        m1 = None
        m2 = None
        m3 = None
        if len(levels) > 8:
            m1 = levels[7]
            m2 = levels[8]
            m3 = levels[9]
        levels = [l7, m1, m2, m3]
        levels = [i for i in levels if i is not None]
    index = 6
    for level_index, level in enumerate(levels):
        range_extend = 0
        for item in level['blackboard']:
            if item['key'] == "ability_range_forward_extend":
                range_extend = item['value']
        if range_extend >0:
            level['rangeExtend'] = range_extend
        if not level['description_ja']:
            level["description_ja"] = replace_substrings(
                jp_skill_table[skill_id]['levels'][index]['description'], jp_skill_table[skill_id]['levels'][index+level_index]['blackboard'])
            level["description_en"] = replace_substrings(
                en_skill_table[skill_id]['levels'][index]['description'], en_skill_table[skill_id]['levels'][index+level_index]['blackboard'])
    return_dict[skill_id] = data
return_dict = chara_skills | return_dict

with open('chara_skills.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)


# uniequip

return_dict = {}
for equip_id in curr_uniequip:
    equip = cn_uniequip_table['equipDict'][equip_id]
    char_id = equip['charId']
    battle_equip = en_battle_equip_table[equip_id] if equip_id in en_battle_equip_table else None
    in_global = equip_id in en_battle_equip_table
    combat_data = curr_uniequip[equip_id]['combatData']
    if battle_equip and not curr_uniequip[equip_id]['name_en']:
        phases = []
        tags = combat_data['tags']
        blackboard = combat_data['blackboard']
        for phase_idx, phase in enumerate(battle_equip['phases']):
            concise_parts = []
            for index, part in enumerate(phase['parts']):
                if not part['target'] in ['TALENT', 'TALENT_DATA_ONLY', 'TRAIT', 'TRAIT_DATA_ONLY', 'DISPLAY']:
                    print(part['target'])
                if 'TRAIT' in part['target'] or part['target'] == 'DISPLAY':
                    if part['addOrOverrideTalentDataBundle']['candidates'] is not None:
                        print('TRAIT or DISPLAY TalentDataBundle not NONE', equip_id)
                    max_candidate = part['overrideTraitDataBundle']['candidates'][-1]
                    max_candidate_en = en_battle_equip_table[equip_id][
                        'phases'][phase_idx]['parts'][index]['overrideTraitDataBundle']['candidates'][-1] if in_global else None
                    max_candidate_jp = jp_battle_equip_table[equip_id][
                        'phases'][phase_idx]['parts'][index]['overrideTraitDataBundle']['candidates'][-1] if in_global else None
                    if max_candidate['rangeId'] is not None:
                        print('TRAIT rangeId not NONE', equip_id)
                    concise_parts.append({"resKey": part['resKey'], "target": part['target'], "isToken": part['isToken'],
                                          "addDesc_zh": combat_data['phases'][phase_idx]['parts'][index]['addDesc_zh'], "addDesc_ja": replace_substrings(max_candidate_jp['additionalDescription'], max_candidate['blackboard']) if in_global else "", "addDesc_en": replace_substrings(max_candidate_en['additionalDescription'], max_candidate['blackboard']) if in_global else "",
                                          "overrideDesc_zh": combat_data['phases'][phase_idx]['parts'][index]['overrideDesc_zh'], "overrideDesc_ja": replace_substrings(max_candidate_jp['overrideDescripton'], max_candidate['blackboard']) if in_global else "", "overrideDesc_en": replace_substrings(max_candidate_en['overrideDescripton'], max_candidate['blackboard']) if in_global else ""})

                if 'TALENT' in part['target']:
                    if part['overrideTraitDataBundle']['candidates'] is not None:
                        print('TALENT TraitDataBundle not NONE', equip_id)
                    max_candidate = part['addOrOverrideTalentDataBundle']['candidates'][-1]
                    max_candidate_en = en_battle_equip_table[equip_id][
                        'phases'][phase_idx]['parts'][index]['addOrOverrideTalentDataBundle']['candidates'][-1] if in_global else None
                    max_candidate_jp = jp_battle_equip_table[equip_id][
                        'phases'][phase_idx]['parts'][index]['addOrOverrideTalentDataBundle']['candidates'][-1] if in_global else None
                    if max_candidate['description'] is not None:
                        print('TALENT description not NONE', equip_id)

                    concise_parts.append({"resKey": part['resKey'], "target": part['target'], "isToken": part['isToken'], "name_zh": max_candidate['name'], "name_ja": max_candidate_jp['name'] if in_global else "", "name_en": max_candidate_en['name'] if in_global else "",
                                          "displayRangeId": max_candidate['displayRangeId'], "rangeId": max_candidate['rangeId'], "talentIndex": max_candidate['talentIndex'],
                                          "upgradeDesc_zh": combat_data['phases'][phase_idx]['parts'][index]['upgradeDesc_zh'], "upgradeDesc_ja": replace_substrings(max_candidate_jp['upgradeDescription'], max_candidate['blackboard']) if in_global else "", "upgradeDesc_en": replace_substrings(max_candidate_en['upgradeDescription'], max_candidate['blackboard']) if in_global else "",
                                          })

            phases.append({'parts': concise_parts, 'attributeBlackboard': phase['attributeBlackboard'],
                           'tokenAttributeBlackboard': phase['tokenAttributeBlackboard'], })
        combat_data = {'phases': phases,
                       "tags": tags, "blackboard": blackboard}

    return_dict[equip_id] = {
        "uniEquipId": equip['uniEquipId'], "name_zh": equip['uniEquipName'], "name_ja": "", "name_en": "", "typeIcon": equip['typeIcon'], 'charId': char_id, "combatData": combat_data}
    if equip_id in en_uniequip_table['equipDict']:
        return_dict[equip_id]['name_ja'] = jp_uniequip_table['equipDict'][equip_id]['uniEquipName']
        return_dict[equip_id]['name_en'] = en_uniequip_table['equipDict'][equip_id]['uniEquipName']

return_dict = curr_uniequip | return_dict

with open('uniequip.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)
