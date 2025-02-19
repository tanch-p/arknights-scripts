import os
import pprint
import copy
import json
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

stage_data_path = os.path.join(
    script_dir,
    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/ro3/level_rogue3_1-3.json",
)
with open("tel_extrainfo.json", encoding="utf-8") as f:
    tel_data = json.load(f)

def compress_waves(stage_data, stage_id):
    routes = []
    waves = copy.deepcopy(stage_data['waves'])
    extra_routes = []
    branches = copy.deepcopy(stage_data['branches'])
    tiles = []
    for tile_index, tile in enumerate(stage_data['mapData']['tiles']):
        mask = 0
        height = 0
        buildableType = 1
        bb = {}
        if tile['blackboard'] is not None:
            for item in tile['blackboard']:
                bb[item['key']] = item['value']

        if tile['passableMask'] == 'FLY_ONLY':
            mask = 1
        if tile['heightType'] == 'HIGHLAND':
            height = 1
        if tile['buildableType'] == 'NONE':
            buildableType = 0
        if stage_id in tel_data and str(tile_index) in tel_data[stage_id]:
            bb = tel_data[stage_id][str(tile_index)]
            bb.pop('tileKey', None)
            bb.pop('position', None)            

        tiles.append([tile['tileKey'], height, mask,
                     bb if len(bb) > 0 else None,buildableType])
    map_data = {"map": stage_data['mapData']['map'], "tiles": tiles}
    for i, route in enumerate(stage_data['routes']):
        route_idx = -1
        for idx, route_data in enumerate(routes):
            if route == route_data[1]:
                route_idx = idx
                break
        if route_idx == -1:
            routes.append([i, route])
        # replace original routeIndex
        for wave in waves:
            for fragment in wave['fragments']:
                for action in fragment['actions']:
                    if action['routeIndex'] == i:
                        if route_idx == -1:  # newly added route
                            action['routeIndex'] = len(routes)-1
                        else:
                            action['routeIndex'] = route_idx
    routes = [route_data[1] for route_data in routes]

    # extra routes
    for i, route in enumerate(stage_data['extraRoutes']):
        route_idx = -1
        for idx, route_data in enumerate(extra_routes):
            if route == route_data[1]:
                route_idx = idx
                break
        if route_idx == -1:
            extra_routes.append([i, route])
        # replace original routeIndex
        for branch_name in branches:
            for phase in branches[branch_name]['phases']:
                for action in phase['actions']:
                    if action['routeIndex'] == i:
                        if route_idx == -1:  # newly added route
                            action['routeIndex'] = len(extra_routes)-1
                        else:
                            action['routeIndex'] = route_idx
    # prune branches
    if branches is not None:
        for branch_name in branches:
                for phase in branches[branch_name]['phases']:
                    for action in phase['actions']:
                        action.pop('managedByScheduler', None)
                        action.pop('blockFragment', None)
                        action.pop('autoDisplayEnemyInfo', None)
                        action.pop('isUnharmfulAndAlwaysCountAsKilled', None)
                        action.pop('hiddenGroup', None)
                        action.pop('randomSpawnGroupKey', None)
                        action.pop('randomSpawnGroupPackKey', None)
                        action.pop('randomType', None)
                        action.pop('refreshType', None)
                        action.pop('weight', None)
                        action.pop('dontBlockWave', None)
                        action.pop('forceBlockWaveInBranch', None)
                    
    extra_routes = [route_data[1] for route_data in extra_routes]

    # pp.pprint(waves)

    return {"routes": routes, "waves": waves, "extra_routes":extra_routes, "branches":branches, "map_data": map_data}
