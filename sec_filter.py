import json

SEARCH_IN_BLACKBOARD = [
    "max_target",
    "stealth",
    "camouflage",
    "ally_camouflage",
    "ally_undying",
    "undying",
    "taunt",
    "ally_taunt",
    "reflect_dmg",
    "ally_reflect_dmg",
    "cancel_stealth",
    "stun",
    "sluggish",
    "sleep",
    "silence",
    "cold",
    "levitate",
    "root",
    "tremble",
    "fear",
    "max_hp",
    "def",
    "res",
    "attack_speed",
    "respawn_time",
    "atk_down",
    "def_down",
    "res_down",
    "ms_down",
    "aspd_down",
    "ally_max_hp",
    "ally_atk",
    "ally_def",
    "ally_res",
    "ally_aspd",
    "ally_block_up",
    "ally_block_down",
    "ally_cost_down",
    "evasion",
    "ally_evasion",
    "ally_dmg_res",
    "dmg_res",
    "shield",
    "ally_shield",
    "block_dmg",
    "ally_block_dmg",
    "sp_gain",
    "ally_sp_regen",
    "ally_sp_gain",
    "ally_sp_stock",
    "sp_stock",
    "def_penetrate",
    "res_penetrate",
    "damage_scale",
    "ally_damage_scale",
    "sp_regen",
    "ally_heal_scale",
    "heal_scale",
    "receive_heal_scale",
    "cost_return",
    "block",
    "hitrate_down",
    "block_no_attack",
    "force",
    "trigger_time",
    "ct",
    "heal_scale_down",
    "ally_def_penetrate",
    "ally_res_penetrate",
    "add_bullet",
    "max_ammo",
    "ally_max_ammo",
    "liftoff",
    "attract",
    "palsy",
    "bonus_lifepoint",
    "enemy_damage_share",
    "sp_module",
]

TARGET_AIR_KEYS = [
    "stun",
    "sluggish",
    "sleep",
    "silence",
    "cold",
    "root",
    "ms_down",
    "aspd_down",
    "res_down",
    "def_down",
]

VALUE_KEY_LIST = ["sp_module"]


def gen_sec_filter_options():
    with open("characters.json", encoding="utf-8") as f:
        chara_list = json.load(f)
    obj = {}

    def find_and_add_key_entries(item):
        if item.get("key") in SEARCH_IN_BLACKBOARD:
            for key, value in item.items():
                if key == "key":
                    continue
                if item["key"] not in obj:
                    obj[item["key"]] = {}

                if key not in obj[item["key"]]:
                    obj[item["key"]][key] = []
                if key == "value" and item.get("key") in VALUE_KEY_LIST:
                    if value not in obj[item["key"]][key]:
                        obj[item["key"]][key].append(value)
                if isinstance(value, list):
                    for val in value or []:
                        if val not in obj[item["key"]][key]:
                            obj[item["key"]][key].append(val)
                elif key in ["targets", "dep_stat", "damage_type", "order"]:
                    if value not in obj[item["key"]][key]:
                        obj[item["key"]][key].append(value)

                if key == "category" and "others" not in obj[item["key"]][key]:
                    obj[item["key"]][key].append("others")

    for char in chara_list:
        # Process character blackboard
        for item in char.get("blackboard", []):
            find_and_add_key_entries(item)

        # Process skills
        for skill in char.get("skills", []):
            for item in skill.get("blackboard", []):
                find_and_add_key_entries(item)

        # Process talents
        for talent in char.get("talents", []):
            for item in talent.get("blackboard", []):
                find_and_add_key_entries(item)

        # Process uniequip
        for equip in char.get("uniequip", []):
            if equip.get("combatData"):
                for item in equip["combatData"].get("blackboard", []):
                    find_and_add_key_entries(item)

        # Process tokens
        for token in char.get("tokens", []):
            for item in token.get("blackboard", []):
                find_and_add_key_entries(item)

    # Add target_air for TARGET_AIR_KEYS
    for key in TARGET_AIR_KEYS:
        if key in obj:
            obj[key]["target_air"] = ["target_air", "not_target_air"]

    # Add blockCnt
    obj["blockCnt"] = {"category": ["normal_state", "skill_active"]}

    # Add PASSIVE
    obj["PASSIVE"] = {"duration": ["infinite", "finite"]}

    with open("sec_filters.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"), indent=4)
