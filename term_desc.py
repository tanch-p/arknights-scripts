import os
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

with open(
    os.path.join(BASE_DIR, "cn_data/zh_CN/gamedata/excel/gamedata_const.json"),
    encoding="utf-8",
) as f:
    cn_gameconst = json.load(f)
with open(
    os.path.join(BASE_DIR, "global_data/en/gamedata/excel/gamedata_const.json"),
    encoding="utf-8",
) as f:
    en_gameconst = json.load(f)
with open(
    os.path.join(BASE_DIR, "global_data/jp/gamedata/excel/gamedata_const.json"),
    encoding="utf-8",
) as f:
    jp_gameconst = json.load(f)

data = {}
data["richTextStyles"] = cn_gameconst["richTextStyles"]
for key in cn_gameconst["termDescriptionDict"]:
    global_has_key = key in en_gameconst["termDescriptionDict"]
    data[key] = {
        "termId": cn_gameconst["termDescriptionDict"][key]["termId"],
        "name_zh": cn_gameconst["termDescriptionDict"][key]["termName"],
        "name_en": en_gameconst["termDescriptionDict"][key]["termName"]
        if global_has_key
        else None,
        "name_ja": jp_gameconst["termDescriptionDict"][key]["termName"]
        if global_has_key
        else None,
        "desc_zh": cn_gameconst["termDescriptionDict"][key]["description"],
        "desc_en": en_gameconst["termDescriptionDict"][key]["description"]
        if global_has_key
        else None,
        "desc_ja": jp_gameconst["termDescriptionDict"][key]["description"]
        if global_has_key
        else None,
    }

with open("gameconst.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
