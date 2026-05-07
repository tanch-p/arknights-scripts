import json
import os
from contextlib import contextmanager

from json_gz import json_to_gz
from sec_filter import gen_sec_filter_options

SCRIPT_DIR = os.path.dirname(__file__)
LANGUAGES = ["zh", "ja", "en"]


def _load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, separators=(",", ":"))


@contextmanager
def _working_directory(path):
    previous_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous_cwd)


def _build_skill_levels(skill, lang):
    levels = []
    for level in skill["levels"]:
        level_options = {
            "rangeId": level["rangeId"],
            "desc": (
                level[f"description_{lang}"]
                if level[f"description_{lang}"]
                else level["description_zh"]
            ),
            "spData": level["spData"],
            "duration": level["duration"],
        }
        if "rangeExtend" in level:
            level_options["rangeExtend"] = level["rangeExtend"]
        levels.append(level_options)
    return levels


def _build_skills(chara_dict, lang):
    skills = []
    for skill in chara_dict["skills"]:
        skills.append(
            {
                "skillId": skill["skillId"],
                "name": skill[f"name_{lang}"]
                if skill[f"name_{lang}"]
                else skill["name_zh"],
                "skillType": skill["skillType"],
                "durationType": skill["durationType"],
                "spType": skill["spType"],
                "levels": _build_skill_levels(skill, lang),
                "tags": skill["tags"],
                "blackboard": skill["blackboard"],
            }
        )
    return skills


def _build_talents(chara_dict, lang):
    talents = []
    for talent in chara_dict["talents"]:
        talent_holder = {
            "prefabKey": talent["prefabKey"],
            "name": talent[f"name_{lang}"]
            if talent[f"name_{lang}"]
            else talent["name_zh"],
            "desc": talent[f"desc_{lang}"]
            if talent[f"desc_{lang}"]
            else talent["desc_zh"],
            "rangeId": talent["rangeId"] if "rangeId" in talent else None,
            "tags": talent["tags"],
            "blackboard": talent["blackboard"],
        }
        talents.append(talent_holder)
    return talents


def _build_combat_parts(parts, lang):
    concise_parts = []
    for part in parts:
        if "TRAIT" in part["target"] or part["target"] == "DISPLAY":
            concise_parts.append(
                {
                    "resKey": part["resKey"],
                    "target": part["target"],
                    "isToken": part["isToken"],
                    "addDesc": part[f"addDesc_{lang}"]
                    if part[f"addDesc_{lang}"]
                    else part["addDesc_zh"],
                    "overrideDesc": part[f"overrideDesc_{lang}"]
                    if part[f"overrideDesc_{lang}"]
                    else part["overrideDesc_zh"],
                }
            )

        if "TALENT" in part["target"]:
            concise_parts.append(
                {
                    "resKey": part["resKey"],
                    "target": part["target"],
                    "isToken": part["isToken"],
                    "name": part[f"name_{lang}"]
                    if part[f"name_{lang}"]
                    else part["name_zh"],
                    "displayRangeId": part["displayRangeId"],
                    "rangeId": part["rangeId"],
                    "talentIndex": part["talentIndex"],
                    "upgradeDesc": part[f"upgradeDesc_{lang}"]
                    if part[f"upgradeDesc_{lang}"]
                    else part["upgradeDesc_zh"],
                }
            )
    return concise_parts


def _build_uniequip(chara_dict, lang):
    uniequip_list = []
    for equip in chara_dict["uniequip"]:
        new_equip = {
            "uniEquipId": equip["uniEquipId"],
            "name": equip[f"name_{lang}"]
            if equip[f"name_{lang}"]
            else equip["name_zh"],
            "typeIcon": equip["typeIcon"],
            "combatData": equip["combatData"],
        }

        combat_data = equip["combatData"]
        if combat_data:
            phases = []
            for phase in combat_data["phases"]:
                phases.append(
                    {
                        "parts": _build_combat_parts(phase["parts"], lang),
                        "attributeBlackboard": phase["attributeBlackboard"],
                        "tokenAttributeBlackboard": phase["tokenAttributeBlackboard"],
                    }
                )
            new_equip["combatData"] = {
                "phases": phases,
                "tags": combat_data["tags"],
                "blackboard": combat_data["blackboard"],
            }

        uniequip_list.append(new_equip)

    uniequip_list.sort(key=lambda equip: equip["uniEquipId"])
    return uniequip_list


def _build_potential(chara_dict, lang):
    potential = []
    for pot in chara_dict["potential"]:
        potential.append(
            {
                "desc": pot[f"desc_{lang}"] if pot[f"desc_{lang}"] else pot["desc_zh"],
                "attribute": pot["attribute"],
            }
        )
    return potential


def _build_token_skills(token, lang):
    token_skills = []
    for skill in token["skills"]:
        sp_data = {
            "maxChargeTime": skill["spData"]["maxChargeTime"],
            "spCost": skill["spData"]["spCost"],
            "initSp": skill["spData"]["initSp"],
            "increment": skill["spData"]["increment"],
        }
        token_skills.append(
            {
                "skillId": skill["skillId"],
                "name": skill[f"name_{lang}"]
                if skill[f"name_{lang}"]
                else skill["name_zh"],
                "iconId": skill["iconId"],
                "rangeId": skill["rangeId"],
                "desc": skill[f"desc_{lang}"]
                if skill[f"desc_{lang}"]
                else skill["desc_zh"],
                "skillType": skill["skillType"],
                "durationType": skill["durationType"],
                "spType": skill["spType"],
                "spData": sp_data,
            }
        )
    return token_skills


def _build_token_talents(token, lang):
    token_talents = []
    for talent in token["talents"]:
        token_talents.append(
            {
                "prefabKey": talent["prefabKey"],
                "name": talent[f"name_{lang}"]
                if talent[f"name_{lang}"]
                else talent["name_zh"],
                "desc": talent[f"desc_{lang}"]
                if talent[f"desc_{lang}"]
                else talent["desc_zh"],
            }
        )
    return token_talents


def _build_tokens(chara_dict, lang):
    tokens = []
    for token in chara_dict["tokens"]:
        tokens.append(
            {
                "id": token["id"],
                "name": token[f"name_{lang}"]
                if token[f"name_{lang}"]
                else token["name_zh"],
                "desc": token[f"desc_{lang}"]
                if token[f"desc_{lang}"]
                else token["desc_zh"],
                "position": token["position"],
                "stats": token["stats"],
                "tags": token["tags"],
                "blackboard": token["blackboard"],
                "skills": _build_token_skills(token, lang),
                "talents": _build_token_talents(token, lang),
            }
        )
    return tokens


def _build_character_entry(chara_dict, lang):
    tags = list(chara_dict["tags"])
    if not chara_dict["name_en"]:
        tags.append("not_in_global")

    return {
        "id": chara_dict["id"],
        "appellation": chara_dict["appellation"],
        "name": chara_dict[f"name_{lang}"]
        if chara_dict[f"name_{lang}"]
        else chara_dict["name_zh"],
        "desc": chara_dict[f"desc_{lang}"]
        if chara_dict[f"desc_{lang}"]
        else chara_dict["desc_zh"],
        "release_time": chara_dict["release_time"],
        "tags": tags,
        "blackboard": chara_dict["blackboard"],
        "powers": chara_dict["powers"],
        "position": chara_dict["position"],
        "isSpChar": chara_dict["isSpChar"],
        "rarity": chara_dict["rarity"],
        "profession": chara_dict["profession"],
        "subProfessionId": chara_dict["subProfessionId"],
        "stats": chara_dict["stats"],
        "potential": _build_potential(chara_dict, lang),
        "favorData": chara_dict["favorData"],
        "tokens": _build_tokens(chara_dict, lang),
        "skills": _build_skills(chara_dict, lang),
        "talents": _build_talents(chara_dict, lang),
        "uniequip": _build_uniequip(chara_dict, lang),
    }


def split_characters_json(
    output_dir=None,
    base_dir=SCRIPT_DIR,
    languages=None,
    compress=True,
    generate_sec_filters=True,
):
    if languages is None:
        languages = LANGUAGES

    chara_list = _load_json(os.path.join(base_dir, "characters.json"))
    output = {}

    for lang in languages:
        output[lang] = [
            _build_character_entry(chara_dict, lang) for chara_dict in chara_list
        ]

    if output_dir is not None:
        for lang, data in output.items():
            output_path = os.path.join(output_dir, f"characters_{lang}.json")
            _write_json(output_path, data)
            if compress:
                json_to_gz(
                    output_path, os.path.join(output_dir, f"characters_{lang}.gz")
                )

        if generate_sec_filters:
            with _working_directory(base_dir):
                gen_sec_filter_options()

    return output


def main():
    split_characters_json(
        output_dir=SCRIPT_DIR,
        base_dir=SCRIPT_DIR,
        compress=True,
        generate_sec_filters=True,
    )


if __name__ == "__main__":
    main()
