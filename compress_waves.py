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

empty_action = {
              "actionType": "EMPTY",
              "key": "",
              "count": 1,
              "preDelay": 0.0,
              "interval": 1.0,
              "routeIndex": 0,
              "hiddenGroup": None,
              "randomSpawnGroupKey": None,
              "randomSpawnGroupPackKey": None,
              "randomType": "ALWAYS",
              "refreshType": "ALWAYS",
              "weight": 10,
              "dontBlockWave": False,
              "forceBlockWaveInBranch": False
            }

def remove_by_indexes(lst, indexes):
    return [item for i, item in enumerate(lst) if i not in indexes]


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
                     bb if len(bb) > 0 else None, buildableType])
    map_data = {"map": stage_data['mapData']['map'], "tiles": tiles}
    for i, route in enumerate(stage_data['routes']):
        if not route:
            # null routes found in act24side_tr01
            continue
        route_idx = -1
        if (route['checkpoints']):
            for checkpoint in route['checkpoints']:
                if checkpoint['type'] == 'WAIT_FOR_SECONDS' and checkpoint['time'] > 998:
                    checkpoint['time'] = 600
                    if 'rogue5' in stage_id and not stage_id in ['level_rogue5_b-5']:
                        checkpoint['time'] = 45
                checkpoint.pop("randomizeReachOffset", None)
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
                    action.pop('managedByScheduler', None)
                    action.pop('blockFragment', None)
                    action.pop('autoDisplayEnemyInfo', None)
                    action.pop('isUnharmfulAndAlwaysCountAsKilled', None)
                    action.pop('randomType', None)
                    action.pop('refreshType', None)
                    action.pop('forceBlockWaveInBranch', None)
                    if action['routeIndex'] == i:
                        if route_idx == -1:  # newly added route
                            action['routeIndex'] = len(routes)-1
                        else:
                            action['routeIndex'] = route_idx
    routes = [route_data[1] for route_data in routes]

    # extra routes
    if 'extraRoutes' in stage_data:
        for i, route in enumerate(stage_data['extraRoutes']):
            if not route:
                # null routes found in act2bossrush_01
                continue
            route_idx = -1
            if (route['checkpoints']):
                for checkpoint in route['checkpoints']:
                    checkpoint.pop("randomizeReachOffset", None)
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

    # handling of special cases

    if stage_id == 'level_rogue4_b-8':
        # apparently the first 3 checkpoints are missing from actual game movement
        extra_routes[1]['checkpoints'] = extra_routes[1]['checkpoints'][3:]
    if stage_id == 'level_rogue4_b-7':
        extra_routes[1]['startPosition'] = {
            "row": 5,
            "col": 20
        }
    if stage_id == 'level_rogue1_b-9':
        branches = None
    if stage_id == 'level_rogue3_3-2':
        for wave in waves:
            for frag_index, fragment in enumerate(wave['fragments']):
                if frag_index == 7:
                    indexes = []
                    for idx, action in enumerate(fragment['actions']):
                        key = action['key']
                        if key == 'enemy_1075_dmgswd' or key == 'enemy_1084_sotidm':
                            indexes.append(idx)
                    fragment['actions'] = remove_by_indexes(
                        fragment['actions'], indexes)
    if stage_id == 'level_rogue5_5-6':
        for wave in waves:
            for frag_index, fragment in enumerate(wave['fragments']):
                if frag_index == 0:
                    indexes = []
                    for idx, action in enumerate(fragment['actions']):
                        key = action['key']
                        if key == 'enemy_10060_cjbfod' and action['randomSpawnGroupKey'] == "t1":
                            indexes.append(idx)
                    fragment['actions'] = remove_by_indexes(
                        fragment['actions'], indexes)
    if stage_id == 'level_rogue5_b-4':
        # 39 - dycast x 2
        # 40 - dyrnge x 3
        # 49 - 10 mob + dycast
        # 50 - 10 mob + dyrnge
        # 53
        for wave_index, wave in enumerate(waves):
            if wave_index == 1:
                for frag_index, fragment in enumerate(wave['fragments']):
                    for idx, action in enumerate(fragment['actions']):
                        if idx in [0, 1]:
                            action['randomSpawnGroupPackKey'] = 'sp1'
                        elif idx in [2,3]:
                            action['randomSpawnGroupPackKey'] = 'sp2'
                        elif idx in [4,5]:
                            action['randomSpawnGroupPackKey'] = 'sp3'
                    empty_t2 = copy.deepcopy(empty_action)
                    empty_t2['randomSpawnGroupKey'] = 't2'
                    empty_t2['weight'] = 10
                    empty_t3 = copy.deepcopy(empty_action)
                    empty_t3['randomSpawnGroupKey'] = 't3'
                    empty_t3['weight'] = 40
                    fragment['actions'].insert(0,empty_t2)
                    fragment['actions'].insert(1,empty_t3)

    if stage_id == 'level_rogue4_d-1':
        branches['Walk']['phases'][0]['actions'][0]['key'] = "enemy_1516_jakill"
    if stage_id == 'level_rogue4_d-2':
        branches['Walk_1']['phases'][0]['actions'][0]['key'] = "enemy_2001_duckmi"
        branches['Walk_2']['phases'][0]['actions'][0]['key'] = "enemy_2002_bearmi"
    if stage_id == 'level_rogue4_d-3':
        branches['Walk_1']['phases'][0]['actions'][0]['key'] = "enemy_2001_duckmi"
        branches['Walk_2']['phases'][0]['actions'][0]['key'] = "enemy_2002_bearmi"
    if stage_id == 'level_rogue4_d-b':
        branches['Walk_1']['phases'][0]['actions'][0]['key'] = "enemy_2090_skzjbc"
        branches['Walk_2']['phases'][0]['actions'][0]['key'] = "enemy_2090_skzjbc"
    if stage_id in ['level_rogue4_d-1']:
        waves = waves[:1]
    if stage_id in ['level_rogue4_d-2', 'level_rogue4_d-3', 'level_rogue4_d-b']:
        # fix to pack enemies together
        waves = waves[:1]
        for wave in waves:
            wave['fragments'] = wave['fragments'][1:]
            for frag_idx, fragment in enumerate(wave['fragments']):
                if frag_idx % 2 == 1:
                    for action in fragment['actions']:
                        action['randomSpawnGroupKey'] = None
                        wave['fragments'][frag_idx-1]['actions'].append(action)
        for wave in waves:
            wave['fragments'] = wave['fragments'][0::2]

    return {"routes": routes, "waves": waves, "extra_routes": extra_routes, "branches": branches, "map_data": map_data}
