import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_roguelike_topic_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)
en_roguelike_topic_path = os.path.join(
    script_dir, "global_data/en_US/gamedata/excel/roguelike_topic_table.json"
)
jp_roguelike_topic_path = os.path.join(
    script_dir, "global_data/ja_JP/gamedata/excel/roguelike_topic_table.json"
)

with open(cn_roguelike_topic_path, encoding="utf-8") as f:
    cn_roguelike_topic_table = json.load(f)
with open(en_roguelike_topic_path, encoding="utf-8") as f:
    en_roguelike_topic_table = json.load(f)
with open(jp_roguelike_topic_path, encoding="utf-8") as f:
    jp_roguelike_topic_table = json.load(f)


topics = ['rogue_1', 'rogue_2', 'rogue_3']


def get_relic_info(id, topic):
    relic_info = None
    if id in cn_roguelike_topic_table['details'][topic]['items']:
        in_global = topic in jp_roguelike_topic_table[
            'details'] and id in jp_roguelike_topic_table['details'][topic]['items']
        relic_info = {
            "id": id,
            "name_zh": cn_roguelike_topic_table['details'][topic]['items'][id]['name'],
            'name_ja': jp_roguelike_topic_table['details'][topic]['items'][id]['name'] if in_global else "",
            'name_en': en_roguelike_topic_table['details'][topic]['items'][id]['name'] if in_global else "",
            "desc_zh": cn_roguelike_topic_table['details'][topic]['items'][id]['usage'],
            "desc_ja": jp_roguelike_topic_table['details'][topic]['items'][id]['usage'] if in_global else "",
            "desc_en": en_roguelike_topic_table['details'][topic]['items'][id]['usage'] if in_global else ""
        }
        if id in cn_roguelike_topic_table['details'][topic]['relicParams'] and len(cn_roguelike_topic_table['details'][topic]['relicParams'][id]['checkCharBoxParams']) > 0:
            relic_info['checkCharBoxParams'] = cn_roguelike_topic_table['details'][
                topic]['relicParams'][id]['checkCharBoxParams'][0]['valueStrs']
        else:
            relic_info['tags'] = None

    return relic_info


relics_list = ["rogue_1_relic_q29",
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
               ]
data = {}
for topic in topics:
    data[topic] = []
    for id in relics_list:
        relic_info = get_relic_info(id, topic)
        if (relic_info):
            data[topic].append(relic_info)


with open("relics_chara.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
