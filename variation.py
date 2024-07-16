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

data = []
for key in cn_roguelike_topic_table['details']['rogue_1']['variationData']:
    variation = cn_roguelike_topic_table['details']['rogue_1']['variationData'][key]
    info = {
        "id": variation["id"],
        "outerName_zh": cn_roguelike_topic_table['details']['rogue_1']['variationData'][key]['outerName'],
        "innerName_zh": cn_roguelike_topic_table['details']['rogue_1']['variationData'][key]['innerName'],
        "outerName_ja": jp_roguelike_topic_table['details']['rogue_1']['variationData'][key]['outerName'],
        "innerName_ja": jp_roguelike_topic_table['details']['rogue_1']['variationData'][key]['innerName'],
        "outerName_en": en_roguelike_topic_table['details']['rogue_1']['variationData'][key]['outerName'],
        "innerName_en": en_roguelike_topic_table['details']['rogue_1']['variationData'][key]['innerName'],
        "src": None,
        "effects": [],
        "tooltip_zh": cn_roguelike_topic_table['details']['rogue_1']['variationData'][key]['functionDesc'],
        "tooltip_ja": jp_roguelike_topic_table['details']['rogue_1']['variationData'][key]['functionDesc'],
        "tooltip_en": en_roguelike_topic_table['details']['rogue_1']['variationData'][key]['functionDesc']

    }
    data.append(info)


with open("variations_phantom.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

data = []
for key in cn_roguelike_topic_table['details']['rogue_2']['variationData']:
    variation = cn_roguelike_topic_table['details']['rogue_2']['variationData'][key]
    info = {
        "id": variation["id"],
        "outerName_zh": cn_roguelike_topic_table['details']['rogue_2']['variationData'][key]['outerName'],
        "innerName_zh": cn_roguelike_topic_table['details']['rogue_2']['variationData'][key]['innerName'],
        "outerName_ja": jp_roguelike_topic_table['details']['rogue_2']['variationData'][key]['outerName'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "innerName_ja": jp_roguelike_topic_table['details']['rogue_2']['variationData'][key]['innerName'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "outerName_en": en_roguelike_topic_table['details']['rogue_2']['variationData'][key]['outerName'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "innerName_en": en_roguelike_topic_table['details']['rogue_2']['variationData'][key]['innerName'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "src": None,
        "effects": [],
        "tooltip_zh": cn_roguelike_topic_table['details']['rogue_2']['variationData'][key]['functionDesc'],
        "tooltip_ja": jp_roguelike_topic_table['details']['rogue_2']['variationData'][key]['functionDesc'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None,
        "tooltip_en": en_roguelike_topic_table['details']['rogue_2']['variationData'][key]['functionDesc'] if 'rogue_2' in jp_roguelike_topic_table['details'] else None

    }
    data.append(info)

with open("variations_mizuki.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


data = []
for key in cn_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData']:
    disaster = cn_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]
    in_global = 'rogue_4' in jp_roguelike_topic_table['modules']
    info = {
        "id": disaster["id"],
        "name_zh": cn_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['name'],
        "name_ja": jp_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['name'] if in_global else None,
        "name_en": en_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['name'] if in_global else None,
        "iconId": disaster['iconId'],
        "level": disaster['level'],
        "effects": [],
        "tooltip_zh": cn_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['functionDesc'],
        "tooltip_ja": jp_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['functionDesc'] if in_global else None,
        "tooltip_en": en_roguelike_topic_table['modules']['rogue_4']['disaster']['disasterData'][key]['functionDesc'] if in_global else None

    }
    data.append(info)

with open("disasters.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
