import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_roguelike_topic_path = os.path.join(
    script_dir, "zh_CN\\gamedata\\excel\\roguelike_topic_table.json"
)
en_roguelike_topic_path = os.path.join(
    script_dir, "en_US\\gamedata\\excel\\roguelike_topic_table.json"
)
jp_roguelike_topic_path = os.path.join(
    script_dir, "ja_JP\\gamedata\\excel\\roguelike_topic_table.json"
)

with open(cn_roguelike_topic_path, encoding="utf-8") as f:
    cn_roguelike_topic_table = json.load(f)
with open(en_roguelike_topic_path, encoding="utf-8") as f:
    en_roguelike_topic_table = json.load(f)
with open(jp_roguelike_topic_path, encoding="utf-8") as f:
    jp_roguelike_topic_table = json.load(f)

rogue_1_relics = ['rogue_1_relic_a02', 'rogue_1_relic_a03', 'rogue_1_relic_a04',
                  'rogue_1_relic_a05', 'rogue_1_relic_a06', 'rogue_1_relic_a07',
                  'rogue_1_relic_a08', 'rogue_1_relic_a09', 'rogue_1_relic_a10',
                  'rogue_1_relic_c01', 'rogue_1_relic_c02', 'rogue_1_relic_c03',
                  'rogue_1_relic_c04', 'rogue_1_relic_c05', 'rogue_1_relic_c06',
                  'rogue_1_relic_m06', 'rogue_1_relic_q32', 'rogue_1_relic_sp03',
                  'rogue_1_relic_n13']

rogue_2_relics = ['rogue_2_relic_fight_1', 'rogue_2_relic_fight_2', 'rogue_2_relic_fight_3',
                  'rogue_2_relic_fight_4', 'rogue_2_relic_fight_5', 'rogue_2_relic_fight_6',
                  'rogue_2_relic_fight_7', 'rogue_2_relic_fight_8', 'rogue_2_relic_fight_9',
                  'rogue_2_relic_fight_42', 'rogue_2_relic_fight_105', 'rogue_2_relic_fight_117',
                  'rogue_2_relic_fight_123', 'rogue_2_relic_curse_2','rogue_2_relic_curse_10']

data = []
for id in rogue_1_relics:
    name_zh = cn_roguelike_topic_table['details']['rogue_1']['items'][id]['name']
    relic_info = {
        "id": id,
        "name_zh": cn_roguelike_topic_table['details']['rogue_1']['items'][id]['name'],
        "name_ja": jp_roguelike_topic_table['details']['rogue_1']['items'][id]['name'],
        "name_en": en_roguelike_topic_table['details']['rogue_1']['items'][id]['name'],
        "img": cn_roguelike_topic_table['details']['rogue_1']['items'][id]['name'],
        "effects": [],
        "tooltip_zh": cn_roguelike_topic_table['details']['rogue_1']['items'][id]['usage'],
        "tooltip_ja": jp_roguelike_topic_table['details']['rogue_1']['items'][id]['usage'],
        "tooltip_en": en_roguelike_topic_table['details']['rogue_1']['items'][id]['usage']

    }
    data.append(relic_info)


with open("relics_phantom.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

data = []
for id in rogue_2_relics:
    name_zh = cn_roguelike_topic_table['details']['rogue_2']['items'][id]['name']
    relic_info = {
        "id": id,
        "name_zh": cn_roguelike_topic_table['details']['rogue_2']['items'][id]['name'],
        "name_ja": jp_roguelike_topic_table['details']['rogue_2']['items'][id]['name'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "name_en": en_roguelike_topic_table['details']['rogue_2']['items'][id]['name'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "img": cn_roguelike_topic_table['details']['rogue_2']['items'][id]['name'],
        "effects": [],
        "tooltip_zh": cn_roguelike_topic_table['details']['rogue_2']['items'][id]['usage'],
        "tooltip_ja": jp_roguelike_topic_table['details']['rogue_2']['items'][id]['usage'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "tooltip_en": en_roguelike_topic_table['details']['rogue_2']['items'][id]['usage'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None

    }
    data.append(relic_info)

with open("relics_mizuki.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
