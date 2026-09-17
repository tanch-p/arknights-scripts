import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

cn_roguelike_topic_path = os.path.join(
    BASE_DIR, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
en_roguelike_topic_path = os.path.join(
    BASE_DIR, "global_data/en/gamedata/excel/roguelike_topic_table.json"
)
jp_roguelike_topic_path = os.path.join(
    BASE_DIR, "global_data/jp/gamedata/excel/roguelike_topic_table.json"
)

with open(cn_roguelike_topic_path, encoding="utf-8") as f:
    cn_roguelike_topic_table = json.load(f)
with open(en_roguelike_topic_path, encoding="utf-8") as f:
    en_roguelike_topic_table = json.load(f)
with open(jp_roguelike_topic_path, encoding="utf-8") as f:
    jp_roguelike_topic_table = json.load(f)


topics = ["rogue_1", "rogue_2", "rogue_3", "rogue_4", "rogue_5", "rogue_6"]


def get_relic_info(id, topic):
    relic_info = None
    if id in cn_roguelike_topic_table["details"][topic]["items"]:
        in_global = (
            topic in jp_roguelike_topic_table["details"]
            and id in jp_roguelike_topic_table["details"][topic]["items"]
        )
        relic_info = {
            "id": id,
            "name_zh": cn_roguelike_topic_table["details"][topic]["items"][id]["name"],
            "name_ja": jp_roguelike_topic_table["details"][topic]["items"][id]["name"]
            if in_global
            else "",
            "name_en": en_roguelike_topic_table["details"][topic]["items"][id]["name"]
            if in_global
            else "",
            "desc_zh": cn_roguelike_topic_table["details"][topic]["items"][id]["usage"],
            "desc_ja": jp_roguelike_topic_table["details"][topic]["items"][id]["usage"]
            if in_global
            else "",
            "desc_en": en_roguelike_topic_table["details"][topic]["items"][id]["usage"]
            if in_global
            else "",
        }
        if (
            id in cn_roguelike_topic_table["details"][topic]["relicParams"]
            and len(
                cn_roguelike_topic_table["details"][topic]["relicParams"][id][
                    "checkCharBoxParams"
                ]
            )
            > 0
        ):
            relic_info["subProfessionId"] = cn_roguelike_topic_table["details"][topic][
                "relicParams"
            ][id]["checkCharBoxParams"][0]["valueStrs"]
        elif id in cn_roguelike_topic_table["details"][topic]["relics"]:
            sub_profession_ids = []
            for buff in cn_roguelike_topic_table["details"][topic]["relics"][id][
                "buffs"
            ]:
                for blackboard in buff["blackboard"]:
                    if blackboard["key"] == "selector.sub_profession":
                        sub_profession_ids.extend(
                            sub_profession
                            for sub_profession in blackboard["valueStr"].split("|")
                            if sub_profession not in sub_profession_ids
                        )
                        break
            if sub_profession_ids:
                relic_info["subProfessionId"] = sub_profession_ids
            else:
                relic_info["tags"] = None
        else:
            relic_info["tags"] = None

    return relic_info


relics_list = [
    "rogue_1_relic_q29",
    "rogue_1_relic_p46",
    "rogue_1_relic_p43",
    "rogue_1_relic_p42",
    "rogue_1_relic_p44",
    "rogue_1_relic_p45",
    "rogue_1_relic_p47",
    "rogue_1_relic_p41",
    "rogue_2_relic_fight_115",
    "rogue_2_relic_fight_86",
    "rogue_2_relic_fight_85",
    "rogue_2_relic_fight_84",
    "rogue_2_relic_fight_83",
    "rogue_2_relic_fight_82",
    "rogue_2_relic_fight_81",
    "rogue_2_relic_fight_130",
    "rogue_2_relic_fight_134",
    "rogue_2_relic_fight_131",
    "rogue_2_relic_fight_135",
    "rogue_3_relic_legacy_159",
    "rogue_3_relic_fight_18",
    "rogue_3_relic_fight_34",
    "rogue_3_relic_legacy_134",
    "rogue_3_relic_legacy_133",
    "rogue_3_relic_legacy_132",
    "rogue_3_relic_legacy_135",
    "rogue_3_relic_legacy_136",
    "rogue_3_relic_legacy_137",
    "rogue_3_relic_hand_1",
    "rogue_3_relic_hand_2",
    "rogue_3_relic_hand_3",
    "rogue_3_relic_hand_4",
    "rogue_3_relic_hand_5",
    "rogue_4_relic_legacy_147",
    "rogue_4_relic_legacy_160",
    "rogue_4_relic_legacy_163",
    "rogue_4_relic_legacy_165",
    "rogue_4_relic_hand_1",
    "rogue_4_relic_hand_2",
    "rogue_4_relic_hand_3",
    "rogue_4_relic_hand_4",
    "rogue_4_relic_hand_5",
    "rogue_4_relic_hand_6",
    "rogue_5_relic_return_30",
    "rogue_5_relic_return_31",
    "rogue_5_relic_return_32",
    "rogue_5_relic_return_33",
    "rogue_5_relic_return_34",
    "rogue_5_relic_return_35",
    "rogue_5_relic_legacy_46",
    "rogue_5_relic_bullet_3",
    "rogue_6_relic_hand_1",
    "rogue_6_relic_hand_2",
    "rogue_6_relic_hand_3",
    "rogue_6_relic_hand_4",
    "rogue_6_relic_hand_5",
    "rogue_6_relic_hand_6",
    "rogue_6_relic_hand_7",
    "rogue_6_relic_assign_10",
    "rogue_6_relic_assign_12",
    "rogue_6_relic_fight_18",
    "rogue_6_relic_fight_22",
    "rogue_6_relic_legacy_61",
    "rogue_6_relic_legacy_134",
    "rogue_6_relic_legacy_139",
]
data = {}
for topic in topics:
    data[topic] = []
    for id in relics_list:
        relic_info = get_relic_info(id, topic)
        if relic_info:
            data[topic].append(relic_info)


with open("relics_chara.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
