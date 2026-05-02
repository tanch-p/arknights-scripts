import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("chara_skills.json", encoding="utf-8") as f:
    data = json.load(f)

results = {}
for skill_id, skill in data.items():
    if skill_id in ["skchr_radian_2"]:
        continue
    last = skill["levels"][-1]
    bat = next(
        (b for b in last.get("blackboard", []) if "base_attack_time" in b["key"]),
        None,
    )
    if bat:
        results[skill_id] = {
            "name_zh": skill.get("name_zh", ""),
            "name_en": skill.get("name_en", ""),
            "chara_list": skill.get("chara_list", []),
            "bat_key": bat["key"],
            "bat_value": bat["value"],
            "description_zh": last.get("description_zh", ""),
            "description_ja": last.get("description_ja", ""),
            "description_en": last.get("description_en", ""),
        }

print(f"Found {len(results)} skills with base_attack_time in blackboard:\n")
for skill_id, info in results.items():
    print(f"{skill_id}  ({', '.join(info['chara_list'])})")
    print(f"  key={info['bat_key']}  value={info['bat_value']}")
    print(f"  {info['name_en'] or info['name_zh']}")
    print(f"  zh: {info['description_zh']}")
    print(f"  ja: {info['description_ja']}")
    print(f"  en: {info['description_en']}")

with open("temp.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)


def extract_bat_from_descriptions():
    with open("temp.json", encoding="utf-8") as f:
        data = json.load(f)

    with open(
        "cn_data/zh_CN/gamedata/excel/character_table.json", encoding="utf-8"
    ) as f:
        char_table = json.load(f)
    name_to_id = {v["name"]: k for k, v in char_table.items()}

    def get_base_attack_time(char_id):
        char = char_table.get(char_id)
        if not char:
            return None
        last_phase = char["phases"][-1]
        last_frame = last_phase["attributesKeyFrames"][-1]
        return last_frame["data"]["baseAttackTime"]

    interval_pat = re.compile(r"攻击间隔|攻撃間隔|[Aa]ttack\s+[Ii]nterval")
    bracket_pat = re.compile(r"\(([+\-*][^)]+)\)")

    extracted = []
    for skill_id, info in data.items():
        bracket_value = None
        for lang in ["description_zh", "description_ja", "description_en"]:
            text = info.get(lang, "")
            if not text or not interval_pat.search(text):
                continue
            # Find the first bracketed value that appears after an interval keyword
            interval_match = interval_pat.search(text)
            after = text[interval_match.start() :]
            bm = bracket_pat.search(after)
            if bm:
                bracket_value = bm.group(1)
                break

        if bracket_value is None:
            continue

        operator = bracket_value[0]
        raw = bracket_value[1:]
        numeric = float(raw.rstrip("%s")) if raw.rstrip("%s") else None

        if operator == "+":
            direction = "increase"
        elif operator == "-":
            direction = "decrease"
        else:  # *
            direction = (
                "decrease" if numeric is not None and numeric < 1 else "increase"
            )

        chara_list = info.get("chara_list", [])
        chara_ids = [name_to_id[name] for name in chara_list if name in name_to_id]
        base_attack_times = {cid: get_base_attack_time(cid) for cid in chara_ids}

        extracted.append(
            {
                "skill_id": skill_id,
                "name": info.get("name_en") or info.get("name_zh", ""),
                "chara_list": chara_list,
                "chara_ids": chara_ids,
                "baseAttackTime": base_attack_times,
                "bat_key": info.get("bat_key"),
                "bat_value": info.get("bat_value"),
                "bracket_value": bracket_value,
                "operator": operator,
                "direction": direction,
                "description": info.get("description_zh", ""),
            }
        )

    return extracted


DEGREE_KEYWORDS = [
    "超大幅度缩短", "超大幅度减小", "超大幅度增大",
    "大幅度缩短", "大幅度减小", "大幅度增大",
    "较大幅度缩短", "较大幅度减小", "较大幅度增大",
    "略微缩短", "略微减小", "略微增大",
    "缩短", "减小", "增大",
]


def compute_final_bat(data):
    interval_pat = re.compile(r"攻击间隔|攻撃間隔|[Aa]ttack\s+[Ii]nterval")
    bracket_pat = re.compile(r"\(([+\-*][^)]+)\)")

    enriched = []
    for entry in data:
        desc = entry.get("description", "")

        interval_match = interval_pat.search(desc)
        if not interval_match:
            continue
        after = desc[interval_match.end():]
        bracket_match = bracket_pat.search(after)
        if not bracket_match:
            continue

        bracket_value = bracket_match.group(1)
        before_bracket = after[:bracket_match.start()]
        degree = next((kw for kw in DEGREE_KEYWORDS if kw in before_bracket), None)

        op = bracket_value[0]
        raw = bracket_value[1:]
        is_percent = raw.endswith("%")
        try:
            numeric = float(raw.rstrip("%"))
        except ValueError:
            numeric = None

        final_bats = {}
        pct_changes = {}
        for cid, initial in entry.get("baseAttackTime", {}).items():
            if initial is None or numeric is None:
                final_bats[cid] = None
                pct_changes[cid] = None
                continue

            if op == "*":
                final = initial * (numeric / 100) if is_percent else initial * numeric
            elif is_percent:
                factor = 1 + numeric / 100 if op == "+" else 1 - numeric / 100
                final = initial * factor
            else:
                final = initial + numeric if op == "+" else initial - numeric

            final = round(final, 4)
            final_bats[cid] = final
            pct_changes[cid] = round((final - initial) / initial * 100, 2) if initial else None

        enriched.append({
            **entry,
            "bracket_value": bracket_value,
            "degree": degree,
            "is_percent": is_percent,
            "final_baseAttackTime": final_bats,
            "pct_change": pct_changes,
        })

    return enriched


if __name__ == "__main__":
    data_extracted = extract_bat_from_descriptions()
    print(f"\nExtracted bracket values from {len(data_extracted)} skills:\n")
    data = [{
        "skill_id": entry['skill_id'],
        "chara_list": entry['chara_list'],
        "chara_ids": entry['chara_ids'],
        "baseAttackTime": entry['baseAttackTime'],
        "bat_key": entry['bat_key'],
        "bat_value": entry['bat_value'],
        "operator": entry['operator'],
        "direction": entry['direction'],
        "description": entry['description']
    }
        for entry in data_extracted
    ]

    with open("skill_bat.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    enriched = compute_final_bat(data)
    print(f"Computed final BAT for {len(enriched)} skills")
    with open("skill_bat_final.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=4)
