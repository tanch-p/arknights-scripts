import json
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
mzk_path = os.path.join(
    script_dir, "cn_data\\zh_CN\\gamedata\\levels\\obt\\roguelike\\ro2\\level_rogue2_b-7.json"
)
with open(mzk_path, encoding="utf-8") as f:
    mzk_stage_info = json.load(f)

lower_left_routes = []
upper_left_routes = []
top_routes = [] 
upper_right_routes = []
extra_routes = []
extra_routes_indexes = []

key_replace = {
    "enemy_2041_syjely_e": "精干打手",
    "enemy_2041_syjely": "骨海漂流体",
    "enemy_2041_syjely_f": "法术近卫组长",
    "enemy_2041_syjely_boom1": "游击队萨卡兹术师组长",
    "enemy_2041_syjely_o": "掠海漂移体",
    "enemy_2041_syjely_j": "领潮员",
    "enemy_2041_syjely_h": "深池重甲卫士队长",
    "enemy_2041_syjely_m": "帝国前锋精锐",
    "enemy_2041_syjely_boom2": "游击队迫击炮兵",
    "enemy_2041_syjely_n": "萨卡兹术师",
    "enemy_2041_syjely_i": "冰爆源石虫",
    "enemy_2041_syjely_c": "萨卡兹大剑手",
    "enemy_2041_syjely_g": "呼啸骑士团学徒",
    "enemy_2041_syjely_d": "爆破攻坚手",
    "enemy_2041_syjely_l": "碎岩者组长"
}


def get_start_pos(routeIndex):
    if routeIndex in lower_left_routes:
        return "↙"
    if routeIndex in upper_left_routes:
        return "↖"
    if routeIndex in top_routes:
        return "↑"
    if routeIndex in upper_right_routes:
        return "➚"
    start_pos = mzk_stage_info['extraRoutes'][routeIndex]['startPosition']
    x = start_pos['col']
    y = start_pos['row']
    return f"x:{x} y:{y}"


for index, route in enumerate(mzk_stage_info['extraRoutes']):
    startPosition = route['startPosition']
    row = startPosition['row']
    col = startPosition['col']

    if index == 83:
        pp.pprint(route)

    if row == 3 and col == 0:
        lower_left_routes.append(index)
    elif row == 8 and col == 1:
        upper_left_routes.append(index)
    elif row == 7 and col == 12:
        upper_right_routes.append(index)
    elif row == 7 and col == 3:
        top_routes.append(index)
    else:
        pass
    
    if index > 103:
        found = False
        for item in extra_routes:
            if route == item:
                found = True
                break
        if not found:
            extra_routes.append(route)
            extra_routes_indexes.append(index)

print(extra_routes_indexes)
print(len(extra_routes_indexes))

with open("test.json", "w", encoding="utf-8") as f:
    json.dump(extra_routes, f, ensure_ascii=False, indent=4)

prev_phase_time = 0
data = {}
for branch in mzk_stage_info['branches']:
    # if branch == "syboss_extra":
    #     continue
    for index, phase in enumerate(mzk_stage_info['branches'][branch]['phases']):
        spawns = {}
        for action in phase['actions']:
            if action['count'] > 1:
                for count in range(action['count']):
                    spawn_time = prev_phase_time + \
                        action['preDelay']+count*action['interval']
                    if not spawn_time in spawns:
                        spawns[spawn_time] = []
                    spawns[spawn_time].append(
                        {"key": action['key'],
                            "enemy": key_replace[action['key']],
                         "count": f"{count+1}/{action['count']}",
                         "interval":action['interval'],
                         "route": get_start_pos(action['routeIndex']),
                         "routeIndex": action['routeIndex']
                         }
                    )
            else:
                spawn_time = prev_phase_time + action['preDelay']
                if not spawn_time in spawns:
                    spawns[spawn_time] = []
                spawns[spawn_time].append(
                    {"key": action['key'],
                        "enemy": key_replace[action['key']],
                     "count": "1/1",
                     "route": get_start_pos(action['routeIndex']),
                     "routeIndex": action['routeIndex']
                     })
        myKeys = list(spawns.keys())
        myKeys.sort()
        sorted_dict = {i: spawns[i] for i in myKeys}
        data[f"{branch}-fragment{index}"] = sorted_dict

with open("mzk.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# with open("mzk.txt", "w", encoding="utf-8") as f:
#     for time in range(361):
#         f.write(f"{str(time)}\n")

#         for branch in mzk_stage_info['branches']:
#             if branch == "syboss_extra":
#                 continue
#             for phase in mzk_stage_info['branches'][branch]['phases']:
#                 for action in phase['actions']:
#                     if action['hiddenGroup'] is not None:
#                         print("hiddenGroup")
#                     if action['randomSpawnGroupKey'] is not None:
#                         print('randomSpawnGroupKey')
