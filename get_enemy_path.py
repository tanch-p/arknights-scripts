import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

map_path = os.path.join(
    script_dir, "cn_data/zh_CN/gamedata/levels/obt/roguelike/ro3/level_rogue3_b-5.json"
)

with open(map_path, encoding="utf-8") as f:
    map_data = json.load(f)

fragment_index = 0
action_index = 13

# route_index = map_data['waves'][0]['fragments'][fragment_index]['actions'][action_index]['routeIndex']
route_index = 12
route_info = map_data['routes'][route_index]

# 0 path, 1 wall

layout = [] 
for row in map_data['mapData']['map']:
    row_layout = []
    for colIndex in row:
        tile = map_data['mapData']['tiles'][colIndex]
        if tile['passableMask'] == "FLY_ONLY":
            row_layout.append(1)
        else:
            row_layout.append(0)
    layout.append(row_layout)

data = {
    "layout":layout,
    "mapData":map_data['mapData'],
    "route": route_info}

with open('temp.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
