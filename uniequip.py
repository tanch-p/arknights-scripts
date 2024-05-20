import json
import os
from chara_skills import replace_substrings

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_uniequip_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/uniequip_table.json")
cn_battle_equip_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/battle_equip_table.json")
jp_battle_equip_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/battle_equip_table.json")
en_battle_equip_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/battle_equip_table.json")

with open(cn_uniequip_path, encoding='utf-8') as f:
    cn_uniequip_table = json.load(f)
with open(cn_battle_equip_path, encoding='utf-8') as f:
    cn_battle_equip_table = json.load(f)
with open(jp_battle_equip_path, encoding='utf-8') as f:
    jp_battle_equip_table = json.load(f)
with open(en_battle_equip_path, encoding='utf-8') as f:
    en_battle_equip_table = json.load(f)


def get_new_trait(parts):
    for part in parts:
        if not part["isToken"] and (part["target"] == "TRAIT" or part['target'] == 'DISPLAY'):
            if part["addDesc_zh"]:
                return {"addDesc_zh": part["addDesc_zh"], "addDesc_ja": part["addDesc_ja"], "addDesc_en": part["addDesc_en"],
                        "overrideDesc_zh": "", "overrideDesc_ja": "", "overrideDesc_en": ""}
            if part["overrideDesc_zh"]:
                return {"addDesc_zh": "", "addDesc_ja": "", "addDesc_en": "",
                        "overrideDesc_zh": part["overrideDesc_zh"], "overrideDesc_ja": part["overrideDesc_ja"], "overrideDesc_en": part["overrideDesc_en"]}


with open('uniequip.json', encoding='utf-8') as f:
    curr_uniequip = json.load(f)

new_equips = [id for id in dict.keys(
    cn_uniequip_table['equipDict']) if id not in set(dict.keys({}))]
return_dict = {}
for equip_id in new_equips:
    equip = cn_uniequip_table['equipDict'][equip_id]
    char_id = equip['charId']
    battle_equip = cn_battle_equip_table[equip_id] if equip_id in cn_battle_equip_table else None
    in_global = equip_id in en_battle_equip_table
    combat_data = None
    if battle_equip:
        phases = []
        blackboard = []
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
                                          "addDesc_zh": replace_substrings(max_candidate['additionalDescription'], max_candidate['blackboard']), "addDesc_en": replace_substrings(max_candidate_en['additionalDescription'], max_candidate['blackboard']) if in_global else "", "addDesc_ja": replace_substrings(max_candidate_jp['additionalDescription'], max_candidate['blackboard']) if in_global else "",
                                          "overrideDesc_zh": replace_substrings(max_candidate['overrideDescripton'], max_candidate['blackboard']), "overrideDesc_en": replace_substrings(max_candidate_en['overrideDescripton'], max_candidate['blackboard']) if in_global else "", "overrideDesc_ja": replace_substrings(max_candidate_jp['overrideDescripton'], max_candidate['blackboard']) if in_global else ""})
                    if phase_idx == 2:
                        blackboard = blackboard + max_candidate['blackboard']

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
                                          "upgradeDesc_zh": replace_substrings(max_candidate['upgradeDescription'], max_candidate['blackboard']), "upgradeDesc_en": replace_substrings(max_candidate_en['upgradeDescription'], max_candidate['blackboard']) if in_global else "", "upgradeDesc_ja": replace_substrings(max_candidate_jp['upgradeDescription'], max_candidate['blackboard']) if in_global else "",
                                          })

                    if phase_idx == 2:
                        blackboard = blackboard + max_candidate['blackboard']
            phases.append({'parts': concise_parts, 'attributeBlackboard': phase['attributeBlackboard'],
                           'tokenAttributeBlackboard': phase['tokenAttributeBlackboard'], })
        combat_data = {'phases': phases,
                       "tags": [], "blackboard": blackboard}

    return_dict[equip_id] = {
        "uniEquipId": equip['uniEquipId'], "typeIcon": equip['typeIcon'], 'charId': char_id, "combatData": combat_data}

return_dict = curr_uniequip | return_dict

with open('uniequip2.json', 'w', encoding='utf-8') as f:
    json.dump(return_dict, f, ensure_ascii=False, indent=4)
