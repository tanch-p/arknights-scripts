import json
import os
from pathlib import Path

from chara_skills import replace_substrings

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, "uniequip.json")


def _load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _get_data_paths(base_dir=BASE_DIR):
    return {
        "cn_uniequip": os.path.join(
            base_dir, "cn_data/zh_CN/gamedata/excel/uniequip_table.json"
        ),
        "cn_battle_equip": os.path.join(
            base_dir, "cn_data/zh_CN/gamedata/excel/battle_equip_table.json"
        ),
        "jp_uniequip": os.path.join(
            base_dir, "global_data/jp/gamedata/excel/uniequip_table.json"
        ),
        "jp_battle_equip": os.path.join(
            base_dir, "global_data/jp/gamedata/excel/battle_equip_table.json"
        ),
        "en_uniequip": os.path.join(
            base_dir, "global_data/en/gamedata/excel/uniequip_table.json"
        ),
        "en_battle_equip": os.path.join(
            base_dir, "global_data/en/gamedata/excel/battle_equip_table.json"
        ),
        "current_uniequip": os.path.join(base_dir, "uniequip.json"),
    }


def _log(verbose, *args):
    if verbose:
        print(*args)


def _build_trait_or_display_part(
    equip_id,
    phase_idx,
    index,
    part,
    in_global,
    en_battle_equip_table,
    jp_battle_equip_table,
    verbose,
):
    if part["addOrOverrideTalentDataBundle"]["candidates"] is not None:
        _log(verbose, "TRAIT or DISPLAY TalentDataBundle not NONE", equip_id)

    max_candidate = part["overrideTraitDataBundle"]["candidates"][-1]
    max_candidate_en = (
        en_battle_equip_table[equip_id]["phases"][phase_idx]["parts"][index][
            "overrideTraitDataBundle"
        ]["candidates"][-1]
        if in_global
        else None
    )
    max_candidate_jp = (
        jp_battle_equip_table[equip_id]["phases"][phase_idx]["parts"][index][
            "overrideTraitDataBundle"
        ]["candidates"][-1]
        if in_global
        else None
    )

    if max_candidate["rangeId"] is not None:
        _log(verbose, "TRAIT rangeId not NONE", equip_id)

    add_desc_ja = ""
    add_desc_en = ""
    override_desc_ja = ""
    override_desc_en = ""
    if in_global:
        assert max_candidate_jp is not None
        assert max_candidate_en is not None
        add_desc_ja = replace_substrings(
            max_candidate_jp["additionalDescription"], max_candidate["blackboard"]
        )
        add_desc_en = replace_substrings(
            max_candidate_en["additionalDescription"], max_candidate["blackboard"]
        )
        override_desc_ja = replace_substrings(
            max_candidate_jp["overrideDescripton"], max_candidate["blackboard"]
        )
        override_desc_en = replace_substrings(
            max_candidate_en["overrideDescripton"], max_candidate["blackboard"]
        )

    concise_part = {
        "resKey": part["resKey"],
        "target": part["target"],
        "isToken": part["isToken"],
        "addDesc_zh": replace_substrings(
            max_candidate["additionalDescription"], max_candidate["blackboard"]
        ),
        "addDesc_ja": add_desc_ja,
        "addDesc_en": add_desc_en,
        "overrideDesc_zh": replace_substrings(
            max_candidate["overrideDescripton"], max_candidate["blackboard"]
        ),
        "overrideDesc_ja": override_desc_ja,
        "overrideDesc_en": override_desc_en,
    }
    blackboard = max_candidate["blackboard"] if phase_idx == 2 else []
    return concise_part, blackboard


def _build_talent_part(
    equip_id,
    phase_idx,
    index,
    part,
    in_global,
    en_battle_equip_table,
    jp_battle_equip_table,
    verbose,
):
    if part["overrideTraitDataBundle"]["candidates"] is not None:
        _log(verbose, "TALENT TraitDataBundle not NONE", equip_id)

    max_candidate = part["addOrOverrideTalentDataBundle"]["candidates"][-1]
    max_candidate_en = (
        en_battle_equip_table[equip_id]["phases"][phase_idx]["parts"][index][
            "addOrOverrideTalentDataBundle"
        ]["candidates"][-1]
        if in_global
        else None
    )
    max_candidate_jp = (
        jp_battle_equip_table[equip_id]["phases"][phase_idx]["parts"][index][
            "addOrOverrideTalentDataBundle"
        ]["candidates"][-1]
        if in_global
        else None
    )

    if max_candidate["description"] is not None:
        _log(verbose, "TALENT description not NONE", equip_id)

    name_ja = ""
    name_en = ""
    upgrade_desc_ja = ""
    upgrade_desc_en = ""
    if in_global:
        assert max_candidate_jp is not None
        assert max_candidate_en is not None
        name_ja = max_candidate_jp["name"]
        name_en = max_candidate_en["name"]
        upgrade_desc_ja = replace_substrings(
            max_candidate_jp["upgradeDescription"], max_candidate["blackboard"]
        )
        upgrade_desc_en = replace_substrings(
            max_candidate_en["upgradeDescription"], max_candidate["blackboard"]
        )

    concise_part = {
        "resKey": part["resKey"],
        "target": part["target"],
        "isToken": part["isToken"],
        "name_zh": max_candidate["name"],
        "name_ja": name_ja,
        "name_en": name_en,
        "displayRangeId": max_candidate["displayRangeId"],
        "rangeId": max_candidate["rangeId"],
        "talentIndex": max_candidate["talentIndex"],
        "upgradeDesc_zh": replace_substrings(
            max_candidate["upgradeDescription"], max_candidate["blackboard"]
        ),
        "upgradeDesc_ja": upgrade_desc_ja,
        "upgradeDesc_en": upgrade_desc_en,
    }
    blackboard = max_candidate["blackboard"] if phase_idx == 2 else []
    return concise_part, blackboard


def _build_combat_data(
    equip_id,
    battle_equip,
    in_global,
    en_battle_equip_table,
    jp_battle_equip_table,
    verbose,
):
    if battle_equip is None:
        return None

    phases = []
    blackboard = []
    for phase_idx, phase in enumerate(battle_equip["phases"]):
        concise_parts = []
        for index, part in enumerate(phase["parts"]):
            if part["target"] not in [
                "TALENT",
                "TALENT_DATA_ONLY",
                "TRAIT",
                "TRAIT_DATA_ONLY",
                "DISPLAY",
            ]:
                _log(verbose, part["target"])

            if "TRAIT" in part["target"] or part["target"] == "DISPLAY":
                concise_part, part_blackboard = _build_trait_or_display_part(
                    equip_id,
                    phase_idx,
                    index,
                    part,
                    in_global,
                    en_battle_equip_table,
                    jp_battle_equip_table,
                    verbose,
                )
                concise_parts.append(concise_part)
                blackboard.extend(part_blackboard)

            if "TALENT" in part["target"]:
                concise_part, part_blackboard = _build_talent_part(
                    equip_id,
                    phase_idx,
                    index,
                    part,
                    in_global,
                    en_battle_equip_table,
                    jp_battle_equip_table,
                    verbose,
                )
                concise_parts.append(concise_part)
                blackboard.extend(part_blackboard)

        phases.append(
            {
                "parts": concise_parts,
                "attributeBlackboard": phase["attributeBlackboard"],
                "tokenAttributeBlackboard": phase["tokenAttributeBlackboard"],
            }
        )

    return {"phases": phases, "tags": [], "blackboard": blackboard}


def _build_uniequip_entry(
    equip_id,
    equip,
    cn_battle_equip_table,
    en_uniequip_table,
    en_battle_equip_table,
    jp_uniequip_table,
    jp_battle_equip_table,
    verbose,
):
    in_global = equip_id in en_battle_equip_table
    battle_equip = (
        cn_battle_equip_table[equip_id] if equip_id in cn_battle_equip_table else None
    )

    entry = {
        "uniEquipId": equip["uniEquipId"],
        "name_zh": equip["uniEquipName"],
        "name_ja": "",
        "name_en": "",
        "typeIcon": equip["typeIcon"],
        "charId": equip["charId"],
        "combatData": _build_combat_data(
            equip_id,
            battle_equip,
            in_global,
            en_battle_equip_table,
            jp_battle_equip_table,
            verbose,
        ),
    }

    if in_global:
        entry["name_ja"] = jp_uniequip_table["equipDict"][equip_id]["uniEquipName"]
        entry["name_en"] = en_uniequip_table["equipDict"][equip_id]["uniEquipName"]

    return entry


def generate_uniequip(
    output_path=DEFAULT_OUTPUT_PATH, base_dir=BASE_DIR, verbose=False
):
    paths = _get_data_paths(base_dir)
    cn_uniequip_table = _load_json(paths["cn_uniequip"])
    cn_battle_equip_table = _load_json(paths["cn_battle_equip"])
    jp_uniequip_table = _load_json(paths["jp_uniequip"])
    jp_battle_equip_table = _load_json(paths["jp_battle_equip"])
    en_uniequip_table = _load_json(paths["en_uniequip"])
    en_battle_equip_table = _load_json(paths["en_battle_equip"])
    curr_uniequip = _load_json(paths["current_uniequip"])

    new_equips = [
        equip_id
        for equip_id in cn_uniequip_table["equipDict"].keys()
        if equip_id not in set(curr_uniequip.keys())
    ]

    new_entries = {}
    for equip_id in new_equips:
        equip = cn_uniequip_table["equipDict"][equip_id]
        new_entries[equip_id] = _build_uniequip_entry(
            equip_id,
            equip,
            cn_battle_equip_table,
            en_uniequip_table,
            en_battle_equip_table,
            jp_uniequip_table,
            jp_battle_equip_table,
            verbose,
        )

    result = curr_uniequip | new_entries

    if output_path is not None:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

    return result


def main():
    generate_uniequip(output_path=DEFAULT_OUTPUT_PATH, verbose=True)


if __name__ == "__main__":
    main()
