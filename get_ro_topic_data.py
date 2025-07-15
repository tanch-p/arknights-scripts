from os import walk
import pprint
import os
import json
from runes import parse_rune

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
roguelike_table_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json")
with open(roguelike_table_path, encoding='utf-8') as f:
    ro_topic_table = json.load(f)


def get_difficulties(rogue_topic):
    data = []
    for item in ro_topic_table['details'][rogue_topic]['difficulties']:
        holder = {
            "difficulty": item['grade'],
            "ruleDesc": item['ruleDesc'],
            "addDesc": item['addDesc'],
            "effects": [],
            "floorBuff": {
                "atk": 1.0,
                "hp": 1.0
            },
        }
        data.append(holder)
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_other_data(rogue_topic, key):
    if key in ro_topic_table['details'][rogue_topic]:
        with open('temp.json', 'w', encoding='utf-8') as f:
            json.dump(ro_topic_table['details'][rogue_topic]
                      [key], f, ensure_ascii=False, indent=4)
    else:
        print("Invalid Key", key)


def get_enemy_relics(rogue_topic):
    data = []
    for item in ro_topic_table['details'][rogue_topic]['items'].values():
        if '敌' in item['usage']:
            effects = []
            id = item['id']
            if id in ro_topic_table['details'][rogue_topic]['relics']:
                for buff in ro_topic_table['details'][rogue_topic]['relics'][id]['buffs']:
                    effects.append(parse_rune(buff))
            holder = {
                "id": item['id'],
                "name_zh": item['name'],
                "name_ja": "",
                "name_en": "",
                "effects": effects,
                "tooltip_zh": item['usage'],
                "tooltip_ja": "",
                "tooltip_en": ""
            }
            data.append(holder)
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_chara_relics(rogue_topic):
    data = []
    for item in ro_topic_table['details'][rogue_topic]['items'].values():
        if '手' in item['name']:
            id = item['id']
            subProfessionId = None
            if id in ro_topic_table['details'][rogue_topic]['relics']:
                for buff in ro_topic_table['details'][rogue_topic]['relics'][id]['buffs']:
                    for bb_item in buff['blackboard']:
                        if bb_item['key'] == "selector.sub_profession":
                            subProfessionId = bb_item['valueStr']
            if subProfessionId is None:
                continue
            holder = {
                "id": item['id'],
                "name_zh": item['name'],
                "name_ja": "",
                "name_en": "",
                "desc_zh": item['usage'],
                "desc_ja": "",
                "desc_en": "",
                "subProfessionId": subProfessionId.split("|")
            }
            data.append(holder)
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(topic_number=5):
    rogue_topic = f'rogue_{topic_number}'
    
    # get_difficulties(rogue_topic)
    # get_other_data(rogue_topic, 'buff')
    # get_chara_relics(rogue_topic)
    # get_enemy_relics(rogue_topic)


if __name__ == "__main__":
    main()
