import json
import os

# split characters.json into diff languages
languages = ['zh', 'ja', 'en']

with open('characters.json', encoding='utf-8') as f:
    chara_list = json.load(f)

for lang in languages:
    data = []
    for chara_dict in chara_list:
        skills = []
        talents = []
        for skill in chara_dict['skills']:
            levels = []
            for level in skill['levels']:
                level_options = {
                    "rangeId": level['rangeId'],
                    "desc": level[f'description_{lang}'] if level[f'description_{lang}'] else level['description_zh'],
                    "spData": level['spData'],
                    "duration": level['duration']
                }
                if 'rangeExtend' in level:
                    level_options['rangeExtend'] = level['rangeExtend']
                levels.append(level_options)
            skills.append({"skillId": skill['skillId'],
                           "name": skill[f'name_{lang}'] if skill[f'name_{lang}'] else skill['name_zh'],
                           "skillType": skill['skillType'],
                           "durationType": skill['durationType'],
                           'spType': skill['spType'],
                           "levels": levels,
                           "tags": skill['tags'],
                           "blackboard": skill['blackboard']})
        if chara_dict['talents']:
            for talent in chara_dict['talents']:
                talent_holder = {
                    "prefabKey": talent["prefabKey"], "name": talent[f'name_{lang}'] if talent[f'name_{lang}'] else talent['name_zh'],
                    "desc": talent[f'desc_{lang}'] if talent[f'desc_{lang}'] else talent['desc_zh'], }
                talent_holder['rangeId'] = talent[
                    'rangeId'] if 'rangeId' in talent else None
                talent_holder['tags'] = talent['tags']
                talent_holder['blackboard'] = talent['blackboard']
                talents.append(talent_holder)
        uniequip_list = []
        for equip in chara_dict['uniequip']:
            new_equip = {"uniEquipId": equip['uniEquipId'],
                         "name": equip[f'name_{lang}'] if equip[f'name_{lang}'] else equip['name_zh'],
                         "typeIcon": equip['typeIcon'], "combatData": equip['combatData']}
            combatData = equip['combatData']
            if combatData:
                phases = []
                for phase in combatData['phases']:
                    concise_parts = []
                    for part in phase['parts']:
                        if 'TRAIT' in part['target'] or part['target'] == 'DISPLAY':
                            concise_parts.append({"resKey": part['resKey'], "target": part['target'], "isToken": part['isToken'],
                                                  "addDesc":  part[f'addDesc_{lang}'] if part[f'addDesc_{lang}'] else part['addDesc_zh'],
                                                  "overrideDesc": part[f'overrideDesc_{lang}'] if part[f'overrideDesc_{lang}'] else part['overrideDesc_zh']})

                        if 'TALENT' in part['target']:
                            concise_parts.append({"resKey": part['resKey'], "target": part['target'], "isToken": part['isToken'],
                                                  "name": part[f'name_{lang}'] if part[f'name_{lang}'] else part['name_zh'],
                                                  "displayRangeId": part['displayRangeId'], "rangeId": part['rangeId'], "talentIndex": part['talentIndex'],
                                                  "upgradeDesc": part[f'upgradeDesc_{lang}'] if part[f'upgradeDesc_{lang}'] else part['upgradeDesc_zh'],
                                                  })
                    phases.append(
                        {"parts": concise_parts, "attributeBlackboard": phase['attributeBlackboard'], "tokenAttributeBlackboard": phase['tokenAttributeBlackboard']})
                new_equip['combatData'] = {
                    "phases": phases, "tags": combatData['tags'], "blackboard": combatData['blackboard']}
            uniequip_list.append(new_equip)
        uniequip_list.sort(key=lambda equip: equip['uniEquipId'])
        stats = chara_dict['stats']

        potential = []

        # potential
        for pot in chara_dict['potential']:
            pot_dict = {"desc": pot[f'desc_{lang}'] if pot[f'desc_{lang}'] else pot['desc_zh'],
                        "attribute": pot['attribute']}
            potential.append(pot_dict)

        # trust/favor
        favor_data = chara_dict['favorData']

        # tokens
        tokens = []
        for token in chara_dict['tokens']:
            token_skills = []
            for skill in token['skills']:
                spData = {
                    "maxChargeTime": skill['spData']['maxChargeTime'],
                    "spCost": skill['spData']['spCost'],
                    "initSp": skill['spData']['initSp'],
                    "increment": skill['spData']['increment']
                }
                token_skills.append({"skillId": skill['skillId'],
                                     "name": skill[f'name_{lang}'] if skill[f'name_{lang}'] else skill['name_zh'],
                                     "iconId": skill["iconId"],
                                     "rangeId": skill['rangeId'],
                                     "desc": skill[f'desc_{lang}'] if skill[f'desc_{lang}'] else skill['desc_zh'],
                                     "skillType": skill['skillType'],
                                     "durationType": skill['durationType'],
                                     "spType": skill['spType'],
                                     'spData': spData})
            token_talents = []
            for talent in token['talents']:
                talent_holder = {
                    "prefabKey": talent["prefabKey"],
                    "name": talent[f'name_{lang}'] if talent[f'name_{lang}'] else talent['name_zh'],
                    "desc": talent[f'desc_{lang}'] if talent[f'desc_{lang}'] else talent['desc_zh'],
                }
                token_talents.append(talent_holder)
            token_dict = {"id": token['id'], "name": token[f'name_{lang}'] if token[f'name_{lang}'] else token['name_zh'],
                          "desc": token[f'desc_{lang}'] if token[f'desc_{lang}'] else token['desc_zh'],
                          "position": token['position'],
                          "stats": token['stats'],
                          "tags": token['tags'], "blackboard": token['blackboard'],
                          "skills": token_skills,
                          "talents": token_talents}
            tokens.append(token_dict)

        tags = chara_dict['tags']
        if not chara_dict['name_en']:
            tags.append("not_in_global")

        return_dict = {"id": chara_dict['id'], "appellation": chara_dict['appellation'],
                       "name": chara_dict[f'name_{lang}'] if chara_dict[f'name_{lang}'] else chara_dict['name_zh'],
                       "desc": chara_dict[f'desc_{lang}'] if chara_dict[f'desc_{lang}'] else chara_dict['desc_zh'],
                       "release_time": chara_dict['release_time'],
                       "tags": tags, "blackboard": chara_dict['blackboard'],
                       "nationId": chara_dict['nationId'], "groupId": chara_dict['groupId'], "teamId": chara_dict['teamId'], "position": chara_dict['position'],
                       "isSpChar": chara_dict['isSpChar'], "rarity": chara_dict['rarity'],
                       "profession": chara_dict['profession'], "subProfessionId": chara_dict['subProfessionId'], "stats": stats,
                       'potential': potential, "favorData": favor_data, "tokens": tokens,
                       "skills": skills, "talents": talents, 'uniequip': uniequip_list, }
        data.append(return_dict)
    with open(f'characters_{lang}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
