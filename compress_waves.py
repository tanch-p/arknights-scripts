import os
import pprint
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

stage_data_path = os.path.join(
    script_dir,
    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/ro3/level_rogue3_1-3.json",
)
# with open(stage_data_path, encoding="utf-8") as f:
# stage_data = json.load(f)


def compress_waves(stage_data):
    routes = []
    waves = stage_data['waves']
    for i, route in enumerate(stage_data['routes']):
        route_idx = -1
        for route_data in routes:
            if route == route_data[1]:
                route_idx = route_data[0]
                break
        if route_idx == -1:
            routes.append([i, route])
        else:
            # replace original routeIndex
            for wave in waves:
                for fragment in wave['fragments']:
                    for action in fragment['actions']:
                        if action['routeIndex'] == i:
                            action['routeIndex'] = route_idx
    routes = [route_data[1] for route_data in routes]

    return {routes, waves}
