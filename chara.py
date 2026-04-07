from __future__ import annotations
import json
import os
import re
from game_types.character_table import (
    CharacterTable,
    CharacterTableEntry,
    PotentialRank,
    SkillRef,
    Talent,
)
from game_types.char_patch_table import CharPatchTable
from chara_skills import replace_substrings
from subprofession_tags import get_sub_profession_tags
import pprint
from tokens import IDS_TO_IGNORE

script_dir = os.path.dirname(__file__)

pp = pprint.PrettyPrinter(indent=4)

buffs_list = [
    "berserk",
    "dying",
    "buffres",
    "shield",
    "strong",
    "invisible",
    "camou",
    "protect",
    "weightless",
    "charged",
    "barrier",
    "overdrive",
    "inspire",
]
subprofessions = [
    "physician",
    "fearless",
    "executor",
    "fastshot",
    "bombarder",
    "bard",
    "protector",
    "ritualist",
    "pioneer",
    "corecaster",
    "splashcaster",
    "charger",
    "centurion",
    "guardian",
    "slower",
    "funnel",
    "mystic",
    "chain",
    "aoesniper",
    "reaperrange",
    "longrange",
    "closerange",
    "siegesniper",
    "loopshooter",
    "bearer",
    "tactician",
    "instructor",
    "lord",
    "artsfghter",
    "sword",
    "musha",
    "crusher",
    "reaper",
    "merchant",
    "hookmaster",
    "ringhealer",
    "healer",
    "wandermedic",
    "unyield",
    "artsprotector",
    "summoner",
    "craftsman",
    "stalker",
    "pusher",
    "dollkeeper",
    "skywalker",
    "agent",
    "fighter",
    "librator",
    "hammer",
    "phalanx",
    "blastcaster",
    "primcaster",
    "incantationmedic",
    "chainhealer",
    "shotprotector",
    "fortress",
    "duelist",
    "primprotector",
    "hunter",
    "geek",
    "underminer",
    "blessing",
    "traper",
    "alchemist",
    "soulcaster",
    "primguard",
    "counsellor",
    "mercenary",
    "skybreaker",
    "watchman",
]

stat_convert = {
    "maxHp": "hp",
    "magicResistance": "res",
    "attackSpeed": "aspd",
    "moveSpeed": "ms",
    "respawnTime": "respawnTime",
    "atk": "atk",
    "def": "def",
    "cost": "cost",
}

ATTRIBUTE_TRANSLATE = {
    "COST": "cost",
    "RESPAWN_TIME": "respawnTime",
    "ATK": "atk",
    "MAX_HP": "hp",
    "ATTACK_SPEED": "aspd",
    "DEF": "def",
    "MAGIC_RESISTANCE": "res",
}

KEYS_TO_IGNORE = [
    "char_512_aprot",
    "char_600_cpione",
    "char_601_cguard",
    "char_602_cdfend",
    "char_603_csnipe",
    "char_604_ccast",
    "char_605_cmedic",
    "char_606_csuppo",
    "char_607_cspec",
    "char_608_acpion",
    "char_609_acguad",
    "char_610_acfend",
    "char_611_acnipe",
    "char_612_accast",
    "char_613_acmedc",
    "char_614_acsupo",
    "char_615_acspec",
    "char_616_pithst",
    "char_617_sharp2",
]

cn_char_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json"
)
cn_skill_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json"
)
en_char_table_path = os.path.join(
    script_dir, "global_data/en/gamedata/excel/character_table.json"
)
jp_char_table_path = os.path.join(
    script_dir, "global_data/jp/gamedata/excel/character_table.json"
)
cn_patch_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/char_patch_table.json"
)
en_patch_table_path = os.path.join(
    script_dir, "global_data/en/gamedata/excel/char_patch_table.json"
)
jp_patch_table_path = os.path.join(
    script_dir, "global_data/jp/gamedata/excel/char_patch_table.json"
)

with open(cn_char_table_path, encoding="utf-8") as f:
    cn_char_table: CharacterTable = json.load(f)
with open(cn_skill_table_path, encoding="utf-8") as f:
    cn_skill_table: dict = json.load(f)
with open(en_char_table_path, encoding="utf-8") as f:
    en_char_table: CharacterTable = json.load(f)
with open(jp_char_table_path, encoding="utf-8") as f:
    jp_char_table: CharacterTable = json.load(f)
with open(cn_patch_table_path, encoding="utf-8") as f:
    cn_patch_table: CharPatchTable = json.load(f)
with open(en_patch_table_path, encoding="utf-8") as f:
    en_patch_table: CharPatchTable = json.load(f)
with open(jp_patch_table_path, encoding="utf-8") as f:
    jp_patch_table: CharPatchTable = json.load(f)

with open("chara_skills.json", encoding="utf-8") as f:
    chara_skills = json.load(f)
with open("chara_talents.json", encoding="utf-8") as f:
    chara_talents = json.load(f)
with open("uniequip.json", encoding="utf-8") as f:
    uniequip_dict = json.load(f)
with open("tokens.json", encoding="utf-8") as f:
    tokens_dict = json.load(f)
with open("chara_imple_dates.json", encoding="utf-8") as f:
    imple_dates = json.load(f)


def build_stats(character_dict: CharacterTableEntry) -> dict:
    last_phase = character_dict["phases"][-1]
    last_frame = last_phase["attributesKeyFrames"][-1]
    data = last_frame["data"]
    return {
        "rangeId": last_phase["rangeId"],
        "level": last_frame["level"],
        "hp": data["maxHp"],
        "atk": data["atk"],
        "def": data["def"],
        "res": data["magicResistance"],
        "cost": data["cost"],
        "blockCnt": data["blockCnt"],
        "aspd": data["baseAttackTime"],
        "respawnTime": data["respawnTime"],
    }


def build_potential(
    cn_ranks: list[PotentialRank],
    en_ranks: list[PotentialRank] | None = None,
    jp_ranks: list[PotentialRank] | None = None,
) -> list[dict]:
    potential = []
    for idx, pot in enumerate(cn_ranks):
        pot_dict = {
            "desc_zh": pot["description"],
            "desc_ja": jp_ranks[idx]["description"]
            if jp_ranks and idx < len(jp_ranks)
            else "",
            "desc_en": en_ranks[idx]["description"]
            if en_ranks and idx < len(en_ranks)
            else "",
        }
        attribute = (
            {
                ATTRIBUTE_TRANSLATE[
                    pot["buff"]["attributes"]["attributeModifiers"][0]["attributeType"]
                ]: pot["buff"]["attributes"]["attributeModifiers"][0]["value"]
            }
            if pot["buff"]
            else None
        )
        pot_dict["attribute"] = attribute
        potential.append(pot_dict)
    return potential


def build_favor(character_dict: CharacterTableEntry) -> dict:
    favor_data = {}
    if character_dict["favorKeyFrames"] is None:
        return favor_data
    for key in character_dict["favorKeyFrames"][-1]["data"]:
        if bool(character_dict["favorKeyFrames"][-1]["data"][key]):
            favor_data[stat_convert[key]] = character_dict["favorKeyFrames"][-1][
                "data"
            ][key]
    return favor_data


def build_tokens(character_dict: CharacterTableEntry, tokens_dict: dict) -> list:
    if character_dict["displayTokenDict"] is None:
        return []
    return [
        tokens_dict[key]
        for key in character_dict["displayTokenDict"]
        if key not in IDS_TO_IGNORE
    ]


def build_powers(character_dict: CharacterTableEntry) -> list[str]:
    powers = []
    powers_list = character_dict["subPower"] or []
    powers_list.append(character_dict["mainPower"])
    for power in powers_list:
        if power["nationId"] is not None:
            powers.append(power["nationId"])
        if power["groupId"] is not None:
            powers.append(power["groupId"])
        if power["teamId"] is not None:
            powers.append(power["teamId"])
    return powers


def build_uniequip(char_id: str, uniequip_dict: dict) -> list:
    uniequip_list = [
        equip for equip in uniequip_dict.values() if equip["charId"] == char_id
    ]
    uniequip_list.sort(key=lambda equip: equip["uniEquipId"])
    return uniequip_list


def build_skills(
    character_skills: list[SkillRef],
    chara_skills: dict,
    strip_level_blackboard: bool = False,
) -> list:
    skills = []
    for skill in character_skills:
        skill_id = skill["skillId"]
        blackboard = (
            chara_skills[skill_id]["blackboard"] if skill_id in chara_skills else []
        )
        levels = chara_skills[skill_id]["levels"]
        if strip_level_blackboard:
            for level in levels:
                del level["blackboard"]
        skills.append(
            {
                "skillId": skill_id,
                "name_zh": chara_skills[skill_id]["name_zh"],
                "name_ja": chara_skills[skill_id]["name_ja"],
                "name_en": chara_skills[skill_id]["name_en"],
                "skillType": chara_skills[skill_id]["skillType"],
                "durationType": chara_skills[skill_id]["durationType"],
                "spType": chara_skills[skill_id]["spType"],
                "levels": levels,
                "tags": chara_skills[skill_id]["tags"]
                if skill_id in chara_skills
                else [],
                "blackboard": blackboard,
            }
        )
    return skills


def build_talents(
    char_id: str,
    character_talents: list[Talent] | None,
    chara_talents: dict,
    en_talents: list[Talent] | None = None,
    jp_talents: list[Talent] | None = None,
    skip_none_names: bool = False,
    include_range_id: bool = False,
) -> list:
    talents = []
    if not character_talents:
        return talents
    for talent_index, talent in enumerate(character_talents):
        max_candidate_index = len(talent["candidates"]) - 1
        maxed_talent = talent["candidates"][max_candidate_index]
        if skip_none_names and maxed_talent["name"] is None:
            continue
        talent_holder = {
            "prefabKey": maxed_talent["prefabKey"],
            "name_zh": maxed_talent["name"],
            "name_en": "",
            "name_ja": "",
            "desc_zh": chara_talents[char_id]["talents"][talent_index]["desc_zh"]
            if char_id in chara_talents
            else maxed_talent["description"],
            "desc_en": "",
            "desc_ja": "",
        }
        if en_talents is not None:
            talent_holder["name_en"] = en_talents[talent_index]["candidates"][
                max_candidate_index
            ]["name"]
            talent_holder["desc_en"] = chara_talents[char_id]["talents"][talent_index][
                "desc_en"
            ]
            talent_holder["name_ja"] = jp_talents[talent_index]["candidates"][
                max_candidate_index
            ]["name"]
            talent_holder["desc_ja"] = chara_talents[char_id]["talents"][talent_index][
                "desc_ja"
            ]
        if include_range_id:
            talent_holder["rangeId"] = (
                chara_talents[char_id]["talents"][talent_index].get("rangeId")
                if char_id in chara_talents
                else None
            )
        talent_holder["tags"] = (
            chara_talents[char_id]["talents"][talent_index]["tags"]
            if char_id in chara_talents
            else []
        )
        talent_holder["blackboard"] = (
            chara_talents[char_id]["talents"][talent_index]["blackboard"]
            if char_id in chara_talents
            else []
        )
        talents.append(talent_holder)
    return talents


def build_subprofession_blackboard(sub_prof: str) -> list:
    blackboard = []
    if sub_prof in ["phalanx"]:
        blackboard.append(
            {"key": "def", "value": 2, "conditions": ["not_skill_active"]}
        )
        blackboard.append(
            {"key": "res", "value": 20, "conditions": ["not_skill_active"]}
        )
    if sub_prof == "slower":
        blackboard.append(
            {"key": "sluggish", "targets": 1, "value": 0.8, "target_air": True}
        )
        blackboard.append(
            {
                "key": "ms_down",
                "targets": 1,
                "value": 0.8,
                "duration": 0.8,
                "category": ["sluggish"],
                "target_air": True,
            }
        )
    if sub_prof == "chain":
        blackboard.append(
            {"key": "sluggish", "targets": 4, "value": 0.5, "target_air": True}
        )
        blackboard.append(
            {
                "key": "ms_down",
                "targets": 4,
                "value": 0.8,
                "duration": 0.5,
                "category": ["sluggish"],
                "target_air": True,
            }
        )
    if sub_prof == "stalker":
        blackboard.append({"key": "evasion", "value": 0.5, "types": ["phys", "arts"]})
    if sub_prof == "ringhealer":
        blackboard.append({"key": "max_target", "value": 3})
    if sub_prof == "librator":
        blackboard.append({"key": "block", "value": 0})
    if sub_prof == "skybreaker":
        blackboard.append({"key": "liftoff", "value": 999})
    return blackboard


def process_main_chars(
    filtered_cn_char_table: CharacterTable,
) -> tuple[list, list[str]]:
    data = []
    subProfessionIds = []

    for id, character_dict in filtered_cn_char_table.items():
        if character_dict["subProfessionId"] not in subProfessionIds:
            subProfessionIds.append(character_dict["subProfessionId"])

        skills = build_skills(character_dict["skills"], chara_skills)

        in_global = id in en_char_table
        en_talents = en_char_table[id]["talents"] if in_global else None
        jp_talents = jp_char_table[id]["talents"] if in_global else None
        talents = build_talents(
            id,
            character_dict["talents"],
            chara_talents,
            en_talents=en_talents,
            jp_talents=jp_talents,
            skip_none_names=True,
            include_range_id=True,
        )

        uniequip_list = build_uniequip(id, uniequip_dict)
        stats = build_stats(character_dict)

        en_ranks = en_char_table[id]["potentialRanks"] if in_global else None
        jp_ranks = jp_char_table[id]["potentialRanks"] if in_global else None
        potential = build_potential(
            character_dict["potentialRanks"], en_ranks, jp_ranks
        )

        favor_data = build_favor(character_dict)
        tokens = build_tokens(character_dict, tokens_dict)

        sub_prof = character_dict["subProfessionId"]
        blackboard = build_subprofession_blackboard(sub_prof)
        tags = get_sub_profession_tags(character_dict, id)

        desc_zh = character_dict["description"].replace("<$ba", "<ba")
        if sub_prof in ["librator", "healer", "musha"]:
            desc_zh = replace_substrings(
                character_dict["trait"]["candidates"][-1]["overrideDescripton"],
                character_dict["trait"]["candidates"][-1]["blackboard"],
            )

        powers = build_powers(character_dict)

        return_dict = {
            "id": id,
            "appellation": character_dict["appellation"],
            "name_zh": character_dict["name"],
            "name_ja": "",
            "name_en": "",
            "desc_zh": desc_zh,
            "desc_ja": "",
            "desc_en": "",
            "release_time": imple_dates[id] if id in imple_dates else 0,
            "tags": tags,
            "blackboard": blackboard,
            "powers": powers,
            "position": character_dict["position"],
            "isSpChar": character_dict["isSpChar"],
            "rarity": character_dict["rarity"],
            "profession": character_dict["profession"],
            "subProfessionId": sub_prof,
            "stats": stats,
            "potential": potential,
            "favorData": favor_data,
            "tokens": tokens,
            "skills": skills,
            "talents": talents,
            "uniequip": uniequip_list,
        }
        if in_global:
            desc_en = en_char_table[id]["description"].replace("<$ba", "<ba")
            desc_ja = jp_char_table[id]["description"].replace("<$ba", "<ba")
            if sub_prof in ["librator", "healer", "musha"]:
                desc_en = replace_substrings(
                    en_char_table[id]["trait"]["candidates"][-1]["overrideDescripton"],
                    en_char_table[id]["trait"]["candidates"][-1]["blackboard"],
                )
                desc_ja = replace_substrings(
                    jp_char_table[id]["trait"]["candidates"][-1]["overrideDescripton"],
                    jp_char_table[id]["trait"]["candidates"][-1]["blackboard"],
                )
            desc_en = re.sub(r"<([A-Z][^>]*)>", r"&lt;\1&gt;", desc_en)
            return_dict["name_ja"] = jp_char_table[id]["name"]
            return_dict["name_en"] = en_char_table[id]["name"]
            return_dict["desc_ja"] = desc_ja
            return_dict["desc_en"] = desc_en
        data.append(return_dict)

    return data, subProfessionIds


def process_patch_chars() -> list:
    data = []
    for id, character_dict in cn_patch_table["patchChars"].items():
        in_global = id in en_patch_table["patchChars"]

        skills = build_skills(
            character_dict["skills"], chara_skills, strip_level_blackboard=True
        )

        en_talents = en_patch_table["patchChars"][id]["talents"] if in_global else None
        jp_talents = jp_patch_table["patchChars"][id]["talents"] if in_global else None
        talents = build_talents(
            id,
            character_dict["talents"],
            chara_talents,
            en_talents=en_talents,
            jp_talents=jp_talents,
        )

        uniequip_list = build_uniequip(id, uniequip_dict)
        stats = build_stats(character_dict)

        en_ranks = (
            en_patch_table["patchChars"][id]["potentialRanks"] if in_global else None
        )
        jp_ranks = (
            jp_patch_table["patchChars"][id]["potentialRanks"] if in_global else None
        )
        potential = build_potential(
            character_dict["potentialRanks"], en_ranks, jp_ranks
        )

        favor_data = build_favor(character_dict)
        tokens = build_tokens(character_dict, tokens_dict)
        tags = get_sub_profession_tags(character_dict, id)
        powers = build_powers(character_dict)

        return_dict = {
            "id": id,
            "appellation": character_dict["appellation"],
            "name_zh": character_dict["name"],
            "name_ja": "",
            "name_en": "",
            "desc_zh": character_dict["description"].replace("<$ba", "<ba"),
            "desc_ja": "",
            "desc_en": "",
            "release_time": imple_dates[id],
            "tags": tags,
            "blackboard": [],
            "powers": powers,
            "position": character_dict["position"],
            "isSpChar": character_dict["isSpChar"],
            "rarity": character_dict["rarity"],
            "profession": character_dict["profession"],
            "subProfessionId": character_dict["subProfessionId"],
            "stats": stats,
            "potential": potential,
            "favorData": favor_data,
            "tokens": tokens,
            "skills": skills,
            "talents": talents,
            "uniequip": uniequip_list,
        }
        if in_global:
            return_dict["name_ja"] = jp_patch_table["patchChars"][id]["name"]
            return_dict["name_en"] = en_patch_table["patchChars"][id]["name"]
            return_dict["desc_ja"] = jp_patch_table["patchChars"][id][
                "description"
            ].replace("<$ba", "<ba")
            return_dict["desc_en"] = en_patch_table["patchChars"][id][
                "description"
            ].replace("<$ba", "<ba")
        data.append(return_dict)
    return data


def update_chara_talents_json(filtered_cn_char_table: CharacterTable) -> None:
    new_chara_list = [id for id in filtered_cn_char_table if id not in chara_talents]
    print(f"new charas: {new_chara_list}")
    return_dict = {}

    for id in new_chara_list:
        talents = []
        if filtered_cn_char_table[id]["talents"]:
            for talent_index, talent in enumerate(
                filtered_cn_char_table[id]["talents"]
            ):
                max_candidate_index = len(talent["candidates"]) - 1
                maxed_talent = talent["candidates"][max_candidate_index]
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
                    "tags": [],
                    "blackboard": maxed_talent["blackboard"],
                }
                if id in en_char_table:
                    talent_holder["name_ja"] = jp_char_table[id]["talents"][
                        talent_index
                    ]["candidates"][max_candidate_index]["name"]
                    talent_holder["desc_ja"] = replace_substrings(
                        jp_char_table[id]["talents"][talent_index]["candidates"][
                            max_candidate_index
                        ]["description"],
                        maxed_talent["blackboard"],
                    )
                    talent_holder["name_en"] = en_char_table[id]["talents"][
                        talent_index
                    ]["candidates"][max_candidate_index]["name"]
                    talent_holder["desc_en"] = replace_substrings(
                        en_char_table[id]["talents"][talent_index]["candidates"][
                            max_candidate_index
                        ]["description"],
                        maxed_talent["blackboard"],
                    )
                talents.append(talent_holder)
        return_dict[id] = {
            "appellation": filtered_cn_char_table[id]["appellation"],
            "talents": talents,
        }

    # patch table
    new_chara_list = [
        id for id in cn_patch_table["patchChars"] if id not in chara_talents
    ]
    for id in new_chara_list:
        talents = []
        if cn_patch_table["patchChars"][id]["talents"]:
            for talent_index, talent in enumerate(
                cn_patch_table["patchChars"][id]["talents"]
            ):
                max_candidate_index = len(talent["candidates"]) - 1
                maxed_talent = talent["candidates"][max_candidate_index]
                talent_holder = {
                    "prefabKey": maxed_talent["prefabKey"],
                    "name_zh": maxed_talent["name"],
                    "name_en": "",
                    "name_ja": "",
                    "desc_zh": maxed_talent["description"],
                    "desc_ja": "",
                    "desc_en": "",
                    "tags": [],
                    "blackboard": maxed_talent["blackboard"],
                }
                if id in en_patch_table["patchChars"]:
                    talent_holder["name_ja"] = jp_patch_table["patchChars"][id][
                        "talents"
                    ][talent_index]["candidates"][max_candidate_index]["name"]
                    talent_holder["desc_ja"] = jp_patch_table["patchChars"][id][
                        "talents"
                    ][talent_index]["candidates"][max_candidate_index]["description"]
                    talent_holder["name_en"] = en_patch_table["patchChars"][id][
                        "talents"
                    ][talent_index]["candidates"][max_candidate_index]["name"]
                    talent_holder["desc_en"] = en_patch_table["patchChars"][id][
                        "talents"
                    ][talent_index]["candidates"][max_candidate_index]["description"]
                talents.append(talent_holder)
        return_dict[id] = {
            "appellation": cn_patch_table["patchChars"][id]["appellation"],
            "talents": talents,
        }

    return_dict = chara_talents | return_dict
    with open("chara_talents.json", "w", encoding="utf-8") as f:
        json.dump(return_dict, f, ensure_ascii=False, indent=4)


# Main execution
filtered_cn_char_table = {
    key: cn_char_table[key]
    for key in cn_char_table
    if "token" not in key and "trap" not in key and key not in KEYS_TO_IGNORE
}

data, subProfessionIds = process_main_chars(filtered_cn_char_table)
data.extend(process_patch_chars())

with open("characters.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"), indent=4)

update_chara_talents_json(filtered_cn_char_table)

for id in subProfessionIds:
    if id not in subprofessions:
        print(id, " (new!)")
