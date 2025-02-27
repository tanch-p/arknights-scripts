import os
import json
import pprint
import itertools
from itertools import combinations
from operator import itemgetter
import copy
import random
from itertools import product
from collections import Counter
from compress_waves import compress_waves
from waves import ALWAYS_KILLED_KEYS

pp = pprint.PrettyPrinter(indent=4)

"""
data: {
    27: [
        {tags:['bossrelic'],
         waves: []}
    ]
}

combinations: [normal|elite] x [bossrelic,totem1]
"""

bonus_enemies = ['enemy_2001_duckmi', 'enemy_2002_bearmi',
                 'enemy_2034_sythef', 'enemy_2085_skzjxd']
neutral_enemies = ['enemy_3003_alymot']


def get_topic(stage_id):
    if 'rogue4' in stage_id:
        return 'rogue_skz'
    if 'rogue3' in stage_id:
        return 'rogue_sami'
    if 'rogue2' in stage_id:
        return 'rogue_mzk'
    if 'rogue1' in stage_id:
        return 'rogue_phantom'


def generate_all_permutations(input_list):
    result = [[]]  # Start with an empty list
    for r in range(1, len(input_list) + 1):
        result.extend([list(combo) for combo in combinations(input_list, r)])
    return result


def flatten(l):
    flat_list = []
    for item in l:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)

    return flat_list


def get_runes_data(runes, levelId, mapData):
    normal_group_name = None
    elite_group_name = None
    enemies_to_replace = {}
    predefine_changes = []
    forbid_locations = []
    max_cost = 99
    if runes is not None:
        for rune in runes:
            key = rune['key']
            if rune['difficultyMask'] == "FOUR_STAR":
                if key == 'level_hidden_group_enable':
                    elite_group_name = rune['blackboard'][0]['valueStr']
                elif key == 'level_enemy_replace':
                    if levelId in ["level_rogue2_5-2"]:
                        enemies_to_replace[rune['blackboard'][1]
                                           ['valueStr']] = rune['blackboard'][0]['valueStr']
                    else:
                        enemies_to_replace[rune['blackboard'][0]
                                           ['valueStr']] = rune['blackboard'][1]['valueStr']
                elif key == 'level_predefines_enable':
                    for item in rune['blackboard']:
                        predefine_changes.append([item['key'], item['value']])
                elif key == 'global_forbid_location':
                    value = rune['blackboard'][0]['valueStr']
                    locations = value.replace(
                        "(", "").replace(")", "").split("|")
                    holder = []
                    for location in locations:
                        v = location.split(",")
                        forbid_locations.append(
                            f"{v[1]},{len(mapData['map']) - 1 - int(v[0])}")
            elif rune['difficultyMask'] == 'NORMAL' and key == 'level_hidden_group_enable':
                normal_group_name = rune['blackboard'][0]['valueStr']
            elif rune['difficultyMask'] == 'ALL' and key == 'cbuff_max_cost':
                max_cost = rune['blackboard'][0]['value']
    return {'normal_group_name': normal_group_name, 'elite_group_name': elite_group_name, 'enemies_to_replace': enemies_to_replace, 'predefine_changes': predefine_changes, 'forbid_locations': forbid_locations,'max_cost':max_cost}


def get_max_permutations(permutation_dict):
    total = 1
    for frag_index, holder in permutation_dict.items():
        for group, value in holder.items():
            total *= value
    return total


def get_hidden_groups(waves, normal_group_name, elite_group_name, levelId):
    hidden_groups = []
    for wave_idx, wave in enumerate(waves):
        for frag_index, fragment in enumerate(wave['fragments']):
            for action in fragment['actions']:
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']
                if not actionType in ['SPAWN']:
                    continue
                if hidden_group is not None and not hidden_group in [normal_group_name, elite_group_name] and not hidden_group in hidden_groups:
                    hidden_groups.append(hidden_group)

    return hidden_groups


def group_resolver(actions):
    groups = {}
    leftovers = []
    not_random_groups = []

    for action in actions:
        group = action['randomSpawnGroupKey']
        if group is not None:
            if not group in groups:
                groups[group] = []
            groups[group].append(action)
        else:
            leftovers.append(action)

    for action in leftovers:
        packKey = action['randomSpawnGroupPackKey']
        if packKey is not None:
            add_pack_to_group(action, groups)
        else:
            not_random_groups.append(action)

    extra_groups = {}
    for action in not_random_groups:
        hidden_group = action['hiddenGroup']

        if not hidden_group in extra_groups:
            extra_groups[hidden_group] = []
        extra_groups[hidden_group].append(action)
    if len(extra_groups) > 0:
        # pp.pprint('extra groups', extra_groups)
        pass
    return groups


def add_pack_to_group(action, groups):
    for group_key in groups:
        for item in groups[group_key]:
            if action['randomSpawnGroupPackKey'] == item['randomSpawnGroupPackKey']:
                groups[group_key].append(action)
                return


# resolve into all permutations
def random_group_resolver(random_groups):
    group_collector = {}
    for group_key in random_groups:
        pack_dict = {}
        for action in random_groups[group_key]:
            pack_key = action['randomSpawnGroupPackKey']
            if not pack_key in pack_dict:
                pack_dict[pack_key] = []
            pack_dict[pack_key].append(action)
        # pp.pprint(pack_dict)
        # case with no packkey
        if len(pack_dict) == 1:
            for pack in pack_dict:
                group_collector[group_key] = pack_dict[pack]
        else:
            pack_groups = []
            for pack in pack_dict:
                pack_groups.append(pack_dict[pack])
            group_collector[group_key] = (pack_groups)

    return group_collector


def get_wave_permutations(waves_data, permutation, group_name, has_bonus_wave, bonus_frag_index, bonus_wave_index, stage_id, log=False):
    waves = copy.deepcopy(waves_data)
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == bonus_wave_index:
            continue
        for frag_index, fragment in enumerate(wave['fragments']):
            if frag_index == bonus_frag_index:
                continue
            groups = []
            actions = []
            for action in fragment['actions']:
                group = action['randomSpawnGroupKey']
                packKey = action['randomSpawnGroupPackKey']
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']

                if not actionType in ['SPAWN']:
                    if not (stage_id == 'level_rogue4_4-10' and action['key'] == "trap_760_skztzs#0"):
                        continue

                if hidden_group is not None and (hidden_group != group_name or group_name is None):
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
                else:
                    actions.append(action)

            random_groups = group_resolver(groups)
            groups = random_group_resolver(random_groups)
            key = f"w{wave_idx}f{frag_index}"
            for groupKey in groups:
                choice = permutation[key][groupKey]
                actions.append(groups[groupKey][choice])

            fragment['actions'] = flatten(actions)
    return waves


def get_bonus(stage_data):
    waves = copy.deepcopy(stage_data['waves'])
    max_frag_index = 0
    bonus_frag_index = -1
    bonus_wave_index = -1
    type = "wave"
    for wave_idx, wave in enumerate(waves):
        for frag_index, fragment in enumerate(wave['fragments']):
            if frag_index > max_frag_index:
                max_frag_index = frag_index
            for action in fragment['actions']:
                if action['key'] == 'enemy_2002_bearmi':
                    bonus_fragment = fragment
                    bonus_frag_index = frag_index
                    bonus_wave_index = wave_idx
                    if frag_index != 0:
                        type = "fragment"
                    break
    if type == "wave":
        return {"type": "wave", "wave_index": bonus_wave_index,  "frag_index": -1}
    else:
        # print('max_frag_index', max_frag_index)
        return {"type": type, "wave_index": bonus_wave_index, "frag_index": bonus_frag_index}


def get_bonus_counts(stage_data, hidden_groups, has_bonus_wave, bonus_frag_index, log=False):
    if not has_bonus_wave:
        return None
    waves = copy.deepcopy(stage_data['waves'])
    base_count = 0
    group_counts = []
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
            continue
        for frag_index, fragment in enumerate(wave['fragments']):
            if frag_index == bonus_frag_index:
                continue
            groups = []
            for action in fragment['actions']:
                group = action['randomSpawnGroupKey']
                packKey = action['randomSpawnGroupPackKey']
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']

                if not actionType in ['SPAWN', 'ACTIVATE_PREDEFINED']:
                    continue
                if hidden_group is not None and hidden_group not in hidden_groups:
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
                else:
                    if action['key'] not in neutral_enemies:
                        base_count += action['count']
                    else:
                        base_count += action['count']
            random_groups = group_resolver(groups)
            groups = random_group_resolver(random_groups)
            # calculate bonus count and probability
            for group in groups:
                counter = []
                for choice in groups[group]:
                    count = 0
                    if type(choice) is dict:
                        count += choice['count']
                    else:
                        for action in choice:
                            count += action['count']
                    counter.append(count)
                group_counts.append(counter)
    log and print(group_counts)
    log and print(base_count)
    # Generate all possible combinations
    combinations = product(*group_counts)
    # Calculate the sum for each combination
    sums = [sum(combo) for combo in combinations]
    # Count the occurrences of each sum
    sum_counts = Counter(sums)
    # Create the result dictionary
    result = [
        {
            "val": base_count+sum_value,
            "prob_count": count
        }
        for sum_value, count in sum_counts.items()
    ]
    new_result = []
    for i in range(len(result) - 1):
        bonus_count = result[i]['val'] + 1
        prob_count = result[i]['prob_count']
        other_prob_count = 0
        for item in result:
            if item['val'] == bonus_count:
                other_prob_count = item['prob_count']
        new_result.append({
            "val": bonus_count,
            "prob": prob_count/(prob_count+other_prob_count),
            "prob_str": str(prob_count) + "/" + str(prob_count+other_prob_count)
        })
    log and print(new_result)
    return new_result


def get_group_permutations(stage_data, group_name, bonus_data, bonus_frag_index, bonus_wave_index, stage_id, log=False):
    waves = copy.deepcopy(stage_data['waves'])
    permutations = {}
    for wave_idx, wave in enumerate(waves):
        if bonus_data and bonus_data['type'] == 'wave' and wave_idx == bonus_wave_index:
            continue
        for frag_index, fragment in enumerate(wave['fragments']):
            groups = []
            if bonus_data and bonus_data['type'] == 'fragment' and wave_idx == bonus_wave_index and frag_index == bonus_frag_index:
                continue
            for action in fragment['actions']:
                group = action['randomSpawnGroupKey']
                packKey = action['randomSpawnGroupPackKey']
                actionType = action['actionType']
                if not actionType in ['SPAWN']:
                    if not (stage_id == 'level_rogue4_4-10' and action['key'] == "trap_760_skztzs#0"):
                        continue
                if action['hiddenGroup'] and not action['hiddenGroup'] in [group_name]:
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
            # STEP 1.2 - Generate permutations based on groups

            random_groups = group_resolver(groups)

            groups = random_group_resolver(random_groups)
            log and print('groups', groups)
            if (len(groups) > 0):
                key = f"w{wave_idx}f{frag_index}"
                for group_key in groups:
                    if not key in permutations:
                        permutations[key] = {}
                    permutations[key][group_key] = len(
                        groups[group_key])
    log and pp.pprint(permutations)
    return permutate(permutations)


"""
{
    1: {  g1 : [0,1],
          g2 : [0,1]},
    2: {  g1 : [0,1]}
}
"""


def permutate(permutations, log=False):
    log and pp.pprint('permutations', permutations)
    max_samples = 32
    permutations_list = []
    p_holder = []
    max_permutations = get_max_permutations(permutations)
    # Step 1 - convert permutations into list
    for frag_index in permutations:
        holder = {"frag_index": frag_index, "groups": []}
        groups = []
        for group in permutations[frag_index]:
            holder['groups'].append(group)
            groups.append(list(
                range(permutations[frag_index][group])))
        permutations_list.append(list(map(list, itertools.product(*groups))))
        p_holder.append(holder)
    # Step 2 - get cartesian product of permutations
    if max_permutations <= max_samples:
        result = (list(map(list, itertools.product(*permutations_list))))
    else:
        result = []
    # Step 3 - convert result back to permutations format
    temp = []
    for permutation in result:
        holder = {}
        for frag_idx, frag in enumerate(permutation):
            frag_index = p_holder[frag_idx]["frag_index"]
            holder[frag_index] = {}
            for group_idx, choice in enumerate(frag):
                group = p_holder[frag_idx]['groups'][group_idx]
                holder[frag_index][group] = choice
        temp.append(holder)
    # pp.pprint(temp)
    return {"max_permutations": max_permutations, "data": temp}


def create_timeline(waves, has_bonus_wave, bonus_wave_idx):
    timelines = []
    total_count = 0
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == bonus_wave_idx:
            continue
        prev_phase_time = 0
        spawns = {}
        wave_blocking_spawns = {}
        for index, fragment in enumerate(wave['fragments']):
            prev_phase_time += fragment['preDelay']
            for action in fragment['actions']:
                if action['key'] in ALWAYS_KILLED_KEYS:
                    continue
                if action['key'] != "" and not 'trap' in action['key'] and (action['isUnharmfulAndAlwaysCountAsKilled'] is False or action['key'] in neutral_enemies):
                    total_count += action['count']
                if action['count'] > 1:
                    # intervals
                    for count in range(action['count']):
                        spawn_time = prev_phase_time + \
                            action['preDelay'] + count*action['interval']
                        if not spawn_time in spawns:
                            spawns[spawn_time] = []
                        spawns[spawn_time].append(
                            {"key": action['key'],
                             "enemy": [action['key']],
                             "count": f"{count+1}/{action['count']}",
                             "interval": action['interval'],
                             "route": (action['routeIndex']),
                             "routeIndex": action['routeIndex'],
                             "hiddenGroup": action['hiddenGroup'],
                             "randomSpawnGroupKey": action['randomSpawnGroupKey'],
                             "randomSpawnGroupPackKey": action['randomSpawnGroupPackKey'],
                             'weight': action['weight']
                             }
                        )
                        if action['dontBlockWave'] is False:
                            if not spawn_time in wave_blocking_spawns:
                                wave_blocking_spawns[spawn_time] = []
                            wave_blocking_spawns[spawn_time].append({"key": action['key'],
                                                                     })
                else:
                    spawn_time = prev_phase_time + action['preDelay']
                    if not spawn_time in spawns:
                        spawns[spawn_time] = []
                    spawns[spawn_time].append(
                        {"key": action['key'],
                         "count": 1,
                         "route": (action['routeIndex']),
                         "routeIndex": action['routeIndex'],
                         "hiddenGroup": action['hiddenGroup'],
                         "randomSpawnGroupKey": action['randomSpawnGroupKey'],
                         "randomSpawnGroupPackKey": action['randomSpawnGroupPackKey'],
                         'weight': action['weight']
                         })
                    if action['dontBlockWave'] is False:
                        if not spawn_time in wave_blocking_spawns:
                            wave_blocking_spawns[spawn_time] = []
                        wave_blocking_spawns[spawn_time].append({"key": action['key'],
                                                                 })
            prev_phase_time = max(
                list(wave_blocking_spawns.keys())) if len(wave_blocking_spawns) > 0 else 0

        myKeys = list(spawns.keys())
        myKeys.sort()
        spawn_list = [{"t": i, "actions": spawns[i]} for i in myKeys]
        timelines.append({
            "preDelay": wave['preDelay'],
            "postDelay": wave['postDelay'],
            "maxTimeWaitingForNextWave": wave['maxTimeWaitingForNextWave'],
            "timeline": spawn_list})
    return {"timelines": timelines, "count": total_count}


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


def get_waves_data(stage_data, levelId, log=False):
    routes, waves_data, extra_routes, branches, map_data = itemgetter(
        'routes', 'waves', 'extra_routes', 'branches', 'map_data')(compress_waves(stage_data, levelId))
    normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes'], levelId, stage_data['mapData']))
    if levelId == 'level_rogue4_b-8':
        normal_group_name = "normal_amiya"
        elite_group_name = "hard_amiya"
    log and print('normal:', normal_group_name, 'elite:',
                  elite_group_name, 'replace:', enemies_to_replace)
    has_bonus_wave = not (
        '_ev-' in levelId or '_t-' in levelId or "_b-" in levelId or "_d-" in levelId)

    return_data = {"routes": routes, "mapData": map_data,
                   "extra_routes": extra_routes, "branches": branches}
    holder = ['NORMAL', 'ELITE']
    bonus_frag_index = -1
    bonus_wave_index = -1
    bonus_data = None
    if has_bonus_wave:
        bonus_data = get_bonus(stage_data)
        bonus_frag_index = bonus_data['frag_index']
        bonus_wave_index = bonus_data['wave_index']
        log and pp.pprint(bonus_data)
    return_data['NORMAL'] = {"groupKey": normal_group_name}
    return_data['ELITE'] = {"groupKey": elite_group_name}
    for diff_group in holder:
        group_name = normal_group_name if diff_group == "NORMAL" else elite_group_name
        max_permutations, permutations = itemgetter("max_permutations", "data")(get_group_permutations(
            stage_data, group_name, bonus_data, bonus_frag_index, bonus_wave_index, levelId, log))
        return_data[diff_group]["max_permutations"] = max_permutations
        return_data[diff_group]['permutations'] = []
        for permutation in permutations:
            return_data[diff_group]['permutations'].append(
                permutation)
    return_data['waves'] = waves_data
    # return_data['timelines'] = timelines
    return_data['bonus'] = bonus_data if has_bonus_wave else None
    # if has_bonus_wave:
    #     return_data['bonus'] = {"data:": bonus_data, "count": bonus_counts}
    return return_data
