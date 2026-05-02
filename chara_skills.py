import json
import os
import re


def replace_key(string):
    string = string.replace(
        "ABILITY_RANGE_FORWARD_EXTEND", "ability_range_forward_extend"
    )
    string = string.replace(
        "HP_RECOVERY_PER_SEC_BY_MAX_HP_RATIO", "hp_recovery_per_sec_by_max_hp_ratio"
    )
    string = string.replace("HP_RECOVERY_PER_SEC", "hp_recovery_per_sec")
    return string


def replace_substrings(text, blackboard):
    if text is None:
        return text
    # Define the regular expression pattern
    pattern = r"\{(.*?)\}"

    # Define a function to replace the matched substrings
    def replace_match(match):
        # Extract the substring inside the curly braces
        value = match.group(1)
        key = value
        if ":" in key:
            key = key.split(":")[0]
        key = key.replace("-", "")
        board = next((n for n in blackboard if n["key"] == key), None)
        if board:
            if "%" in value:
                value = abs(round(board["value"] * 100))
                if board["key"] == "damage_scale" and board["value"] > 1:
                    value -= 100
                value = f"{value}%"
            else:
                if isinstance(board["value"], float) and f"{board['value']}"[-1] != "0":
                    value = f"{abs(board['value'])}"
                else:
                    value = f"{abs(round(board['value']))}"
            return value
        else:
            print("unchanged key", value)
            return "{" + value + "}"
        # Replace the matched substring with the value

    # Replace the substrings using the regular expression and the replace_match function
    text = replace_key(text)
    result = re.sub(pattern, replace_match, text)
    result = re.sub(r"<([A-Z][^>]*)>", r"&lt;\1&gt;", result)

    return result


# Empirical tiers for degree keywords in skill descriptions, derived from
# 93 observed base_attack_time modifier skills. Maps keyword → (min_pct, max_pct)
# of percent change on the character's baseAttackTime. Used to decide whether
# an ambiguous blackboard value should be rendered as absolute seconds or as a
# percent — e.g. bat=-0.8 on BAT=3.0 is -26% absolute (wrong tier for 大幅度缩短)
# but -80% as percent (correct tier).
DEGREE_TIERS = {
    "超大幅度缩短": (-90, -65),
    "超大幅度减小": (-90, -65),
    "大幅度缩短": (-90, -35),
    "大幅度减小": (-90, -35),
    "大幅度增大": (35, 230),
    "较大幅度缩短": (-85, -35),
    "较大幅度减小": (-85, -35),
    "较大幅度增大": (35, 140),
    "略微缩短": (-50, -15),
    "略微减小": (-50, -15),
    "略微增大": (15, 55),
    "缩短": (-85, -15),
    "减小": (-85, -15),
    "增大": (15, 230),
}
_DEGREE_KEYWORDS = sorted(DEGREE_TIERS, key=len, reverse=True)


def _find_degree(text):
    for kw in _DEGREE_KEYWORDS:
        if kw in text:
            return kw
    return None


def insert_attack_interval(text, blackboard, base_attack_time=None, bracket_value=None):
    if text is None:
        return text
    bat = next((b["value"] for b in blackboard if "base_attack_time" in b["key"]), None)
    if bat is None:
        return text

    def fmt_num(sign, v):
        v = abs(v)
        if isinstance(v, float) and str(v)[-1] != "0":
            return f"{sign}{v}"
        return f"{sign}{round(v)}"

    def pick_val(tag, context, default_form):
        """Return bracket body, switching to percent form if the tier demands it.

        default_form: "multiplier" → "*{bat}", "absolute" → "{sign}{|bat|}".
        """
        if default_form == "multiplier":
            default_str = fmt_num("*", bat)
            default_pct = (bat - 1) * 100
        else:
            sign = "-" if tag == "vup" else "+"
            default_str = fmt_num(sign, bat)
            signed_bat = -abs(bat) if tag == "vup" else abs(bat)
            default_pct = (
                signed_bat / base_attack_time * 100 if base_attack_time else None
            )

        if base_attack_time in (None, 0):
            return default_str
        degree = _find_degree(context) if context else None
        if degree not in DEGREE_TIERS or default_pct is None:
            return default_str
        lo, hi = DEGREE_TIERS[degree]
        if lo <= default_pct <= hi:
            return default_str
        # Default doesn't fit tier — try percent form (bat interpreted as fraction)
        pct_sign = "-" if tag == "vup" else "+"
        pct_signed = -abs(bat) * 100 if tag == "vup" else abs(bat) * 100
        if lo <= pct_signed <= hi:
            return fmt_num(pct_sign, abs(bat) * 100) + "%"
        return default_str

    # Match interval keyword + short connector (≤20 chars) + vup/vdown block, all on one pass.
    # This prevents inserting into unrelated tag blocks that happen to follow later in text.
    combined = re.compile(
        r"(攻击间隔|攻撃(?:の)?間隔|[Aa]ttack\s+[Ii]nterval)"
        r"([^，、,\n]{0,20}?)"
        r"<@ba\.(vup|vdown)>(.*?)</>",
        re.DOTALL,
    )

    def insert_val(m):
        keyword, connector, tag, content = (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
        )
        if re.search(r"\([+\-*][^)]+\)", content):
            return m.group(0)
        if bracket_value is not None:
            val = bracket_value
        else:
            # bat_value > 0 with vup (interval shortens) → multiplier (*); otherwise additive (+/-)
            form = "multiplier" if (tag == "vup" and bat > 0) else "absolute"
            val = pick_val(tag, connector + content, form)
        return f"{keyword}{connector}<@ba.{tag}>{content}({val})</>"

    result = combined.sub(insert_val, text, count=1)

    # Fallback for plain-text pattern: {keyword}{desc}{boundary}  (no tag wrapping the interval change)
    if result == text:
        plain = re.compile(
            r"(攻击间隔|攻撃(?:の)?間隔|[Aa]ttack\s+[Ii]nterval)"
            r"([^，、,<\n]+)"
            r"(?=[，、,])"
        )

        def insert_plain(m):
            keyword, desc = m.group(1), m.group(2)
            if re.search(r"\([+\-*][^)]+\)", desc):
                return m.group(0)
            space = " " if keyword.isascii() else ""
            val = bracket_value if bracket_value is not None else pick_val(
                "vup", desc, "absolute"
            )
            return f"{keyword}{desc}{space}({val})"

        result = plain.sub(insert_plain, result, count=1)

    return result


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


def update_chara_skills():
    cn_char_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json"
    )
    cn_skill_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json"
    )
    en_skill_table_path = os.path.join(
        script_dir, "global_data/en/gamedata/excel/skill_table.json"
    )
    jp_skill_table_path = os.path.join(
        script_dir, "global_data/jp/gamedata/excel/skill_table.json"
    )

    with open(cn_char_table_path, encoding="utf-8") as f:
        cn_char_table = json.load(f)
    with open(cn_skill_table_path, encoding="utf-8") as f:
        cn_skill_table = json.load(f)
    with open(en_skill_table_path, encoding="utf-8") as f:
        en_skill_table = json.load(f)
    with open(jp_skill_table_path, encoding="utf-8") as f:
        jp_skill_table = json.load(f)

    with open("chara_skills.json", encoding="utf-8") as f:
        chara_skills = json.load(f)

    # append new skills to skill tags json
    new_skill_list = [
        skill
        for skill in dict.keys(cn_skill_table)
        if skill not in set(dict.keys(chara_skills))
    ]
    return_dict = {}
    for skill in new_skill_list:
        in_global = skill in en_skill_table
        if "sktok" in skill or "skcom_withdraw" in skill:
            continue
        chara_list = []
        for id in cn_char_table:
            for skill_dict in cn_char_table[id]["skills"]:
                if skill_dict["skillId"] == skill:
                    chara_list.append(cn_char_table[id]["name"])
        levels = cn_skill_table[skill]["levels"]

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
        return_levels = []
        index = 5
        for level in levels:
            index += 1
            description_zh = replace_substrings(
                cn_skill_table[skill]["levels"][index]["description"],
                cn_skill_table[skill]["levels"][index]["blackboard"],
            )
            description_ja = (
                replace_substrings(
                    jp_skill_table[skill]["levels"][index]["description"],
                    cn_skill_table[skill]["levels"][index]["blackboard"],
                )
                if in_global
                else ""
            )
            description_en = (
                replace_substrings(
                    en_skill_table[skill]["levels"][index]["description"],
                    cn_skill_table[skill]["levels"][index]["blackboard"],
                )
                if in_global
                else ""
            )
            data = {
                "rangeId": level["rangeId"],
                "description_zh": description_zh,
                "description_ja": description_ja,
                "description_en": description_en,
                "spData": level["spData"],
                "duration": level["duration"],
                "blackboard": level["blackboard"],
            }
            return_levels.append(data)

        blackboard = levels[-1]["blackboard"]
        return_dict[skill] = {
            "name_zh": cn_skill_table[skill]["levels"][0]["name"],
            "name_ja": jp_skill_table[skill]["levels"][0]["name"] if in_global else "",
            "name_en": en_skill_table[skill]["levels"][0]["name"] if in_global else "",
            "chara_list": chara_list,
            "skillType": cn_skill_table[skill]["levels"][0]["skillType"],
            "durationType": cn_skill_table[skill]["levels"][0]["durationType"],
            "spType": cn_skill_table[skill]["levels"][0]["spData"]["spType"],
            "levels": return_levels,
            "tags": [],
            "blackboard": blackboard,
        }
    return_dict = chara_skills | return_dict

    with open("chara_skills.json", "w", encoding="utf-8") as f:
        json.dump(return_dict, f, ensure_ascii=False, indent=4)


def update_chara_skills_new():
    cn_char_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json"
    )
    cn_skill_table_path = os.path.join(
        script_dir, "cn_data/zh_CN/gamedata/excel/skill_table.json"
    )
    en_skill_table_path = os.path.join(
        script_dir, "global_data/en/gamedata/excel/skill_table.json"
    )
    jp_skill_table_path = os.path.join(
        script_dir, "global_data/jp/gamedata/excel/skill_table.json"
    )

    with open(cn_char_table_path, encoding="utf-8") as f:
        cn_char_table = json.load(f)
    with open(cn_skill_table_path, encoding="utf-8") as f:
        cn_skill_table = json.load(f)
    with open(en_skill_table_path, encoding="utf-8") as f:
        en_skill_table = json.load(f)
    with open(jp_skill_table_path, encoding="utf-8") as f:
        jp_skill_table = json.load(f)

    with open("chara_skills.json", encoding="utf-8") as f:
        chara_skills = json.load(f)

    def get_base_attack_time(char_id):
        char = cn_char_table.get(char_id)
        if not char:
            return None
        last_phase = char["phases"][-1]
        last_frame = last_phase["attributesKeyFrames"][-1]
        return last_frame["data"]["baseAttackTime"]

    # append new skills to skill tags json
    new_skill_list = [
        skill for skill in dict.keys(cn_skill_table) if skill not in set(dict.keys({}))
    ]
    return_dict = {}
    for skill in new_skill_list:
        in_global = skill in en_skill_table
        if "sktok" in skill or "skcom_withdraw" in skill:
            continue
        chara_list = []
        chara_ids = []
        for id in cn_char_table:
            for skill_dict in cn_char_table[id]["skills"]:
                if skill_dict["skillId"] == skill:
                    chara_list.append(cn_char_table[id]["name"])
                    chara_ids.append(id)
        base_attack_time = get_base_attack_time(chara_ids[0]) if chara_ids else None
        levels = cn_skill_table[skill]["levels"]

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
        return_levels = []
        index = 5
        for i, level in enumerate(levels):
            index += 1
            level_blackboard = cn_skill_table[skill]["levels"][index]["blackboard"]
            description_zh = insert_attack_interval(
                replace_substrings(
                    cn_skill_table[skill]["levels"][index]["description"],
                    level_blackboard,
                ),
                level_blackboard,
                base_attack_time,
            )
            # Tier table is Chinese-only — compute the bracket from ZH, then reuse
            # it verbatim for JA/EN so all three languages stay consistent.
            bv_match = re.search(
                r"(攻击间隔|攻撃(?:の)?間隔|[Aa]ttack\s+[Ii]nterval).{0,30}?\(([+\-*][^)]+)\)",
                description_zh or "",
                re.DOTALL,
            )
            bv = bv_match.group(2) if bv_match else None
            description_ja = (
                insert_attack_interval(
                    replace_substrings(
                        jp_skill_table[skill]["levels"][index]["description"],
                        level_blackboard,
                    ),
                    level_blackboard,
                    base_attack_time,
                    bracket_value=bv,
                )
                if in_global
                else ""
            )
            description_en = (
                insert_attack_interval(
                    replace_substrings(
                        en_skill_table[skill]["levels"][index]["description"],
                        level_blackboard,
                    ),
                    level_blackboard,
                    base_attack_time,
                    bracket_value=bv,
                )
                if in_global
                else ""
            )
            data = {
                "description": {
                    "zh": description_zh,
                    "ja": description_ja,
                    "en": description_en,
                }
            }
            if i == len(levels) - 1:
                data["duration"] = level["duration"]

            return_levels.append(data)

        blackboard = [
            {"key": b["key"], "value": b["value"]} for b in levels[-1]["blackboard"]
        ]
        return_dict[skill] = {
            "name": {
                "zh": cn_skill_table[skill]["levels"][0]["name"],
                "ja": jp_skill_table[skill]["levels"][0]["name"] if in_global else "",
                "en": en_skill_table[skill]["levels"][0]["name"] if in_global else "",
            },
            "chara_list": chara_list,
            "chara_ids": chara_ids,
            "skillType": cn_skill_table[skill]["levels"][0]["skillType"],
            "durationType": cn_skill_table[skill]["levels"][0]["durationType"],
            "spType": cn_skill_table[skill]["levels"][0]["spData"]["spType"],
            "levels": return_levels,
            "tags": [],
            "blackboard": blackboard,
        }
    # return_dict = chara_skills | return_dict

    with open("chara_skills_new.json", "w", encoding="utf-8") as f:
        json.dump(return_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    update_chara_skills_new()
