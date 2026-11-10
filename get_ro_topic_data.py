import pprint
import os
import re
from pathlib import Path
import json
from runes import parse_rune

pp = pprint.PrettyPrinter(indent=4)
relic_id_pattern = re.compile(r"^rogue_\d+_relic_[A-Za-z0-9_]+$")

BASE_DIR = Path(__file__).resolve().parent
roguelike_table_path = os.path.join(
    BASE_DIR, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
with open(roguelike_table_path, encoding="utf-8") as f:
    ro_topic_table = json.load(f)

localized_ro_topic_tables = {}
for language, locale in (("en", "en"), ("ja", "jp")):
    with open(
        BASE_DIR / "global_data" / locale / "gamedata/excel/roguelike_topic_table.json",
        encoding="utf-8",
    ) as f:
        localized_ro_topic_tables[language] = json.load(f)


def get_relic_translations(rogue_topic, item, description_key):
    translations = {
        "name": {"zh": item["name"], "ja": "", "en": ""},
        description_key: {"zh": item["usage"], "ja": "", "en": ""},
    }
    for language, table in localized_ro_topic_tables.items():
        localized_item = (
            table["details"].get(rogue_topic, {}).get("items", {}).get(item["id"], {})
        )
        translations["name"][language] = localized_item.get("name", "")
        translations[description_key][language] = localized_item.get("usage", "")
    return translations


def get_difficulties(rogue_topic):
    data = []
    for item in ro_topic_table["details"][rogue_topic]["difficulties"]:
        holder = {
            "difficulty": item["grade"],
            "ruleDesc": item["ruleDesc"],
            "addDesc": item["addDesc"],
            "effects": [],
            "floorBuff": {"atk": 1.0, "hp": 1.0},
        }
        data.append(holder)
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_other_data(rogue_topic, key, folder="details"):
    if key in ro_topic_table[folder][rogue_topic]:
        with open("temp.json", "w", encoding="utf-8") as f:
            json.dump(
                ro_topic_table[folder][rogue_topic][key],
                f,
                ensure_ascii=False,
                indent=4,
            )
    else:
        print("Invalid Key", key)


def get_all_relics(rogue_topic):
    if rogue_topic == "ALL":
        topics = ro_topic_table["details"].values()
    else:
        topics = [ro_topic_table["details"][rogue_topic]]

    relic_ids = [
        relic["id"]
        for topic in topics
        for relic in topic.get("relics", {}).values()
        if relic_id_pattern.fullmatch(relic["id"])
    ]
    relics_with_level = [
        relic_id for relic_id in relic_ids if relic_id.endswith(("_a", "_b", "_c"))
    ]
    data = [relic_id for relic_id in relic_ids if relic_id not in relics_with_level]

    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open("relics_with_level.json", "w", encoding="utf-8") as f:
        json.dump(relics_with_level, f, ensure_ascii=False, indent=4)


def get_enemy_relics(rogue_topic):
    data = []
    for item in ro_topic_table["details"][rogue_topic]["items"].values():
        if item["usage"] is None:
            continue
        if "敌" in item["usage"]:
            effects = []
            id = item["id"]
            if id in ro_topic_table["details"][rogue_topic]["relics"]:
                for buff in ro_topic_table["details"][rogue_topic]["relics"][id][
                    "buffs"
                ]:
                    effects.append(parse_rune(buff))
            holder = {
                "id": item["id"],
                **get_relic_translations(rogue_topic, item, "tooltip"),
                "effects": effects,
            }
            data.append(holder)
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_chara_relics(rogue_topic):
    data = []
    for item in ro_topic_table["details"][rogue_topic]["items"].values():
        if "手" in item["name"]:
            id = item["id"]
            subProfessionId = None
            if id in ro_topic_table["details"][rogue_topic]["relics"]:
                for buff in ro_topic_table["details"][rogue_topic]["relics"][id][
                    "buffs"
                ]:
                    for bb_item in buff["blackboard"]:
                        if bb_item["key"] == "selector.sub_profession":
                            subProfessionId = bb_item["valueStr"]
            if subProfessionId is None:
                continue
            holder = {
                "id": item["id"],
                **get_relic_translations(rogue_topic, item, "desc"),
                "subProfessionId": subProfessionId.split("|"),
            }
            data.append(holder)
    with open("temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(topic_number=1):
    rogue_topic = f"rogue_{topic_number}"

    # get_difficulties(rogue_topic)
    # get_other_data(rogue_topic, "weather")
    # get_chara_relics(rogue_topic)
    get_enemy_relics(rogue_topic)
    # get_all_relics("ALL")


if __name__ == "__main__":
    main()
