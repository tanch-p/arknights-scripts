import json
import os

from chara_skills import replace_substrings

SCRIPT_DIR = os.path.dirname(__file__)
DEFAULT_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "tokens.json")

IDS_TO_IGNORE = ["token_10057_svash2_eagle"]


def _load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _get_data_paths(base_dir=SCRIPT_DIR):
    return {
        "cn_char_table": os.path.join(
            base_dir, "cn_data/zh_CN/gamedata/excel/character_table.json"
        ),
        "en_char_table": os.path.join(
            base_dir, "global_data/en/gamedata/excel/character_table.json"
        ),
        "jp_char_table": os.path.join(
            base_dir, "global_data/jp/gamedata/excel/character_table.json"
        ),
        "cn_skill_table": os.path.join(
            base_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json"
        ),
        "en_skill_table": os.path.join(
            base_dir, "global_data/en/gamedata/excel/skill_table.json"
        ),
        "jp_skill_table": os.path.join(
            base_dir, "global_data/jp/gamedata/excel/skill_table.json"
        ),
        "token_tags": os.path.join(base_dir, "chara_token_tags.json"),
    }


def _get_final_phase(token_dict):
    return token_dict["phases"][-1]


def _get_final_attributes(token_dict):
    return _get_final_phase(token_dict)["attributesKeyFrames"][-1]


def _build_stats(token_dict):
    final_phase = _get_final_phase(token_dict)
    final_attributes = _get_final_attributes(token_dict)
    final_data = final_attributes["data"]

    return {
        "rangeId": final_phase["rangeId"],
        "level": final_attributes["level"],
        "hp": final_data["maxHp"],
        "atk": final_data["atk"],
        "def": final_data["def"],
        "res": final_data["magicResistance"],
        "cost": final_data["cost"],
        "blockCnt": final_data["blockCnt"],
        "aspd": final_data["baseAttackTime"],
        "respawnTime": final_data["respawnTime"],
    }


def _build_skills(
    token_id,
    token_dict,
    in_global,
    cn_skill_table,
    en_skill_table,
    jp_skill_table,
):
    skills = []
    token_skills = {
        skill["skillId"]
        for skill in token_dict["skills"]
        if skill["skillId"] is not None
    }

    for skill_id in sorted(token_skills):
        skill = cn_skill_table[skill_id]
        level = skill["levels"][-1]
        desc = level["description"]
        if not desc:
            continue

        blackboard = level["blackboard"]
        icon_id = skill["iconId"]
        if token_id == "token_10012_rosmon_shield":
            icon_id = "sktok_rosmon"

        skills.append(
            {
                "skillId": skill_id,
                "name_zh": level["name"],
                "name_ja": jp_skill_table[skill_id]["levels"][-1]["name"]
                if in_global
                else "",
                "name_en": en_skill_table[skill_id]["levels"][-1]["name"]
                if in_global
                else "",
                "iconId": icon_id,
                "rangeId": level["rangeId"],
                "desc_zh": replace_substrings(desc, blackboard),
                "desc_ja": (
                    replace_substrings(
                        jp_skill_table[skill_id]["levels"][-1]["description"],
                        blackboard,
                    )
                    if in_global
                    else ""
                ),
                "desc_en": (
                    replace_substrings(
                        en_skill_table[skill_id]["levels"][-1]["description"],
                        blackboard,
                    )
                    if in_global
                    else ""
                ),
                "skillType": level["skillType"],
                "durationType": level["durationType"],
                "spType": level["spData"]["spType"],
                "spData": level["spData"],
            }
        )

    return skills


def _build_talents(token_id, token_dict, in_global, en_char_table, jp_char_table):
    talents = []
    if not token_dict["talents"]:
        return talents

    for talent_index, talent in enumerate(token_dict["talents"]):
        if not talent["candidates"]:
            continue

        max_candidate_index = len(talent["candidates"]) - 1
        maxed_talent = talent["candidates"][max_candidate_index]
        if maxed_talent["description"] is None:
            continue

        talent_holder = {
            "prefabKey": maxed_talent["prefabKey"],
            "name_zh": maxed_talent["name"],
            "name_en": "",
            "name_ja": "",
            "desc_zh": replace_substrings(
                maxed_talent["description"], maxed_talent["blackboard"]
            ),
            "desc_ja": "",
            "desc_en": "",
        }

        if in_global:
            jp_talent = jp_char_table[token_id]["talents"][talent_index]["candidates"][
                max_candidate_index
            ]
            en_talent = en_char_table[token_id]["talents"][talent_index]["candidates"][
                max_candidate_index
            ]
            talent_holder["name_ja"] = jp_talent["name"]
            talent_holder["desc_ja"] = replace_substrings(
                jp_talent["description"], maxed_talent["blackboard"]
            )
            talent_holder["name_en"] = en_talent["name"]
            talent_holder["desc_en"] = replace_substrings(
                en_talent["description"], maxed_talent["blackboard"]
            )

        if maxed_talent["name"]:
            talents.append(talent_holder)

    return talents


def _build_token_entry(
    token_id,
    token_dict,
    token_tags,
    en_char_table,
    jp_char_table,
    cn_skill_table,
    en_skill_table,
    jp_skill_table,
):
    in_global = token_id in en_char_table
    tags = []
    blackboard = []
    if token_id in token_tags:
        tags = token_tags[token_id]["tags"]
        blackboard = token_tags[token_id]["blackboard"]

    entry = {
        "id": token_id,
        "name_zh": token_dict["name"],
        "name_ja": "",
        "name_en": "",
        "desc_zh": token_dict["description"].replace("<$ba", "<ba")
        if token_dict["description"]
        else "",
        "desc_ja": "",
        "desc_en": "",
        "position": token_dict["position"],
        "stats": _build_stats(token_dict),
        "tags": tags,
        "blackboard": blackboard,
        "skills": _build_skills(
            token_id,
            token_dict,
            in_global,
            cn_skill_table,
            en_skill_table,
            jp_skill_table,
        ),
        "talents": _build_talents(
            token_id, token_dict, in_global, en_char_table, jp_char_table
        ),
    }

    if in_global:
        entry["name_ja"] = jp_char_table[token_id]["name"]
        entry["name_en"] = en_char_table[token_id]["name"]
        entry["desc_ja"] = jp_char_table[token_id]["description"].replace("<$ba", "<ba")
        entry["desc_en"] = en_char_table[token_id]["description"].replace("<$ba", "<ba")

    return entry


def generate_tokens(
    output_path=DEFAULT_OUTPUT_PATH, base_dir=SCRIPT_DIR, verbose=False
):
    paths = _get_data_paths(base_dir)
    cn_char_table = _load_json(paths["cn_char_table"])
    cn_skill_table = _load_json(paths["cn_skill_table"])
    en_char_table = _load_json(paths["en_char_table"])
    jp_char_table = _load_json(paths["jp_char_table"])
    en_skill_table = _load_json(paths["en_skill_table"])
    jp_skill_table = _load_json(paths["jp_skill_table"])
    token_tags = _load_json(paths["token_tags"])

    filtered_cn_char_table = {
        key: value
        for key, value in cn_char_table.items()
        if "token" not in key and "trap" not in key
    }

    tokens_list = []
    for chara_dict in filtered_cn_char_table.values():
        display_token_dict = chara_dict["displayTokenDict"]
        if display_token_dict is not None:
            tokens_list.extend(display_token_dict.keys())

    if verbose:
        print(tokens_list)

    data = {}
    for token_id in tokens_list:
        if token_id in IDS_TO_IGNORE:
            continue

        token_dict = cn_char_table[token_id]
        data[token_id] = _build_token_entry(
            token_id,
            token_dict,
            token_tags,
            en_char_table,
            jp_char_table,
            cn_skill_table,
            en_skill_table,
            jp_skill_table,
        )

    if output_path is not None:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return data


def main():
    generate_tokens(output_path=DEFAULT_OUTPUT_PATH, verbose=True)


if __name__ == "__main__":
    main()
