import os
import json
import pprint
import itertools
from itertools import combinations, product
from operator import itemgetter
import copy
import random
from collections import Counter, defaultdict
from compress_waves import compress_waves
from waves import ALWAYS_KILLED_KEYS
import re

pp = pprint.PrettyPrinter(indent=4)

pattern = re.compile(r"^level_rogue\d+_\d+-\d+$")

bonus_enemies = ['enemy_2001_duckmi', 'enemy_2002_bearmi',
                 'enemy_2034_sythef', 'enemy_2085_skzjxd']
sp_stages_with_bonus = [
    "level_rogue5_ev-1",
    "level_rogue5_t-9-a", "level_rogue5_t-9-b", "level_rogue5_t-9-c"]

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

ACTION_TYPES_TO_PARSE = ['SPAWN', 'ACTIVATE_PREDEFINED', 'EMPTY']


with open("enemy_database.json", encoding="utf-8") as f:
    my_enemy_db = json.load(f)


def is_countable_enemy(key, stage_data):
    enemy_refs = stage_data["enemyDbRefs"]
    enemy = next((item for item in enemy_refs if item['id'] == key), None)
    if enemy is None:
        print(f"{key} not found")
        return True
    enemy_id = key
    if enemy['overwrittenData'] is not None:
        if enemy["overwrittenData"]['prefabKey']['m_defined'] or enemy['useDb'] is False:
            enemy_id = enemy["overwrittenData"]['prefabKey']['m_value']
        not_countable = my_enemy_db[enemy_id]['notCountInTotal']
        if enemy["overwrittenData"]["notCountInTotal"]["m_defined"]:
            not_countable = enemy["overwrittenData"]["notCountInTotal"]["m_value"]
        return not (not_countable)
    else:
        return not (my_enemy_db[key]['notCountInTotal'])


def analyze_enemy_spawns(waves_data, levelId, bonus_data, difficulty, group_name, enemies_to_replace, stage_data):
    """
    Returns:
        Dictionary with analysis results including guaranteed spawns and all possible combinations
    """
    results = {
        'enemy_list': {},
        'enemy_counts': [],
        'absolute_bonus_count': "",
    }
    # Track guaranteed spawns (non-grouped)
    guaranteed_spawns = {}

    # Track random groups per fragment
    fragment_groups = []

    # Process each wave
    for wave_index, wave in enumerate(waves_data):
        if bonus_data and bonus_data['type'] == 'wave' and wave_index == bonus_data['wave_index']:
            continue
        for fragment_index, fragment in enumerate(wave['fragments']):
            if bonus_data and bonus_data['type'] == 'fragment' and wave_index == bonus_data['wave_index'] and fragment_index == bonus_data['frag_index']:
                continue
            packed_groups = get_random_groups(fragment, [group_name])

            # Get all SPAWN or ACTIVATE_PREDEFINED actions only
            spawn_actions = [action for action in fragment['actions']
                             if action['actionType'] in ACTION_TYPES_TO_PARSE
                             ]
            # Separate packed and non-packed actions within this fragment
            for action in spawn_actions:
                if difficulty != 0 and action['key'] in enemies_to_replace:
                    action['key'] = enemies_to_replace[action['key']]
            for action in spawn_actions:
                if action['hiddenGroup'] is not None and (action['hiddenGroup'] != group_name or group_name is None):
                    continue
                enemy_key = action['key']
                group_key = action['randomSpawnGroupKey'] if 'randomSpawnGroupKey' in action else None
                pack_key = action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None
                if group_key:
                    continue
                if pack_has_group_in_fragment(fragment['actions'], pack_key):
                    continue
                # Guaranteed spawn
                if enemy_key not in guaranteed_spawns:
                    guaranteed_spawns[enemy_key] = 0
                guaranteed_spawns[enemy_key] += action['count']

            fragment_random_groups = {}
            for group_key in packed_groups:
                fragment_random_groups[group_key] = {
                    'options': [],
                    'total_weight': 0,
                    'location': f"Wave {wave_index + 1}, Fragment {fragment_index + 1}"
                }
                for pack_action in packed_groups[group_key]:
                    if type(pack_action) is dict:
                        fragment_random_groups[group_key]['options'].append({
                            'actions': [pack_action],
                            'packKey': pack_action['randomSpawnGroupPackKey'],
                        })
                    else:
                        fragment_random_groups[group_key]['options'].append({
                            'actions': [*pack_action],
                            'packKey': pack_action[0]['randomSpawnGroupPackKey'],
                        })

            # Add this fragment's groups to the collection if it has any
            if fragment_random_groups:
                fragment_groups.append({
                    'location': f"Wave {wave_index + 1}, Fragment {fragment_index + 1}",
                    'groups': fragment_random_groups
                })
    # pp.pprint(guaranteed_spawns)
    # pp.pprint(fragment_groups)

    # Generate all possible scenarios
    def generate_scenarios():
        base_count = 0
        for key in guaranteed_spawns:
            if is_countable_action(key, stage_data):
                base_count += guaranteed_spawns[key]
        if not fragment_groups:
            # No random groups, only guaranteed spawns
            return [base_count]

        data = get_enemy_spawn_counts(fragment_groups, stage_data)
        final_list = data['list']
        base_count += data['extra_count']
        combinations = get_count_combinations(final_list)
        return [count + base_count for count in combinations]

    base_counts = generate_scenarios()
    bonus_counts = [count + 1 for count in base_counts]
    absolute_bonus_counts = [
        item for item in bonus_counts if item not in base_counts] if bonus_data else None

    min_max_counts = get_min_max_counts(fragment_groups, guaranteed_spawns)

    filtered_enemy_list = [{"key": key, "min_count": counts['min'], "max_count": counts['max']}
                           for key, counts in min_max_counts.items() if not 'trap' in key]

    results['absolute_bonus_count'] = absolute_bonus_counts
    results['enemy_counts'] = base_counts
    results['enemy_list'] = filtered_enemy_list
    # pp.pprint(filtered_enemy_list)
    return results


def get_min_max_counts(fragment_groups, guaranteed_spawns):
    """
    Takes in fragment groups and consolidates min and max count of each enemy and adds count from guaranteed spawns

    Args:
        fragment_groups, guaranteed_spawns

    Returns:
        Dictionary with min/max count of each enemy
    """

    holder = {}
    for fragment in fragment_groups:
        for group_key, group_data in fragment['groups'].items():
            local_group_spawns = []
            for option in group_data['options']:
                option_spawns = {}
                for action in option['actions']:
                    actionKey = action['key']
                    if not actionKey in option_spawns:
                        option_spawns[actionKey] = 0
                    option_spawns[actionKey] += action['count']
                local_group_spawns.append(option_spawns)
            group_spawns = {}
            has_none_option = any("" in key for key in local_group_spawns)

            # pp.pprint(local_group_spawns)

            for pack in local_group_spawns:
                for key, count in pack.items():
                    if key == '':
                        continue
                    if not key in group_spawns:
                        group_spawns[key] = []
                    group_spawns[key].append(count)
            min_max_list = [{"key": key,
                             "min": 0 if has_none_option or len(group_spawns[key]) != len(local_group_spawns) else min(group_spawns[key]),
                             "max": max(group_spawns[key])} for key in group_spawns]
            for item in min_max_list:
                if not item['key'] in holder:
                    holder[item['key']] = {"min": 0, "max": 0}
                holder[item['key']]["min"] += item['min']
                holder[item['key']]["max"] += item['max']
    for key, count in guaranteed_spawns.items():
        if not key in holder:
            holder[key] = {"min": count, "max": count}
        else:
            holder[key]["min"] += count
            holder[key]["max"] += count
    return holder


def get_count_combinations(lst):
    merged_results = defaultdict(float)

    for combination in product(*lst):
        total_value = sum(item['count'] for item in combination)

        merged_results[total_value] = 1

    # Convert to list of dicts
    return [value for value, prob in sorted(merged_results.items())]


def get_random_groups(fragment, hidden_groups):
    groups = []
    for action in fragment['actions']:
        action_type = action.get('actionType')
        group_key = action.get('randomSpawnGroupKey')
        pack_key = action.get('randomSpawnGroupPackKey')

        if action_type not in ACTION_TYPES_TO_PARSE:
            continue
        if group_key:
            groups.append(action)
            continue

        if pack_has_group_in_fragment(fragment['actions'], pack_key):
            groups.append(action)

    random_groups = group_resolver(groups)
    packed_groups = random_group_resolver(random_groups)
    for group_key in packed_groups:
        is_pack = False
        for i, grouping in enumerate(packed_groups[group_key]):
            if type(grouping) is list:
                is_pack = True
                packed_groups[group_key][i] = [action for action in grouping if (
                    action['hiddenGroup'] is None or action['hiddenGroup'] in hidden_groups)]
        if not is_pack:
            pass
            packed_groups[group_key] = [action for action in packed_groups[group_key] if (
                action['hiddenGroup'] is None or action['hiddenGroup'] in hidden_groups)]

    keys_to_delete = []
    for group_key in packed_groups:
        if len(packed_groups[group_key]) == 0:
            keys_to_delete.append(group_key)
        elif type(packed_groups[group_key][0]) is list:
            is_empty = True
            for grouping in packed_groups[group_key]:
                if len(grouping) > 0:
                    is_empty = False
            if is_empty:
                keys_to_delete.append(group_key)

    for key in keys_to_delete:
        del packed_groups[key]
    return packed_groups


def get_enemy_spawn_counts(spawn_data, stage_data):
    # pp.pprint(spawn_data)
    final_list = []
    extra_base_count = 0
    for fragment in spawn_data:

        for group_key, group_data in fragment['groups'].items():
            options = []
            count_list = []
            for option in group_data['options']:
                count = get_option_count(option, stage_data)
                count_list.append(count)
                options.append(
                    {"count": count, 'packKey': option['packKey']})
            count_set = set(count_list)

            if len(count_set) > 1:
                final_list.append(options)
            else:
                for count in count_set:
                    extra_base_count += count
    return {"list": final_list, "extra_count": extra_base_count}


def get_option_count(option, stage_data):
    count = 0
    for action in option['actions']:
        key = action["key"]
        if is_countable_action(key, stage_data):
            count += action['count']
    return count


def pack_has_group_in_fragment(actions, pack_key):
    if not pack_key:
        return False
    for action in actions:
        if action.get('randomSpawnGroupPackKey') == pack_key and action.get('randomSpawnGroupKey'):
            return True
    return False


def get_topic(stage_id):
    if 'rogue4' in stage_id:
        return 'rogue_skz'
    if 'rogue3' in stage_id:
        return 'rogue_sami'
    if 'rogue2' in stage_id:
        return 'rogue_mzk'
    if 'rogue1' in stage_id:
        return 'rogue_phantom'


def is_countable_action(key, stage_data):
    if 'trap' in key:
        return False
    if key == '':
        return False
    if key in ALWAYS_KILLED_KEYS:
        return False

    return is_countable_enemy(key, stage_data)


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
    return {'normal_group_name': normal_group_name, 'elite_group_name': elite_group_name, 'enemies_to_replace': enemies_to_replace, 'predefine_changes': predefine_changes, 'forbid_locations': forbid_locations, 'max_cost': max_cost}


def get_max_permutations(permutation_dict):
    total = 1
    for frag_index, holder in permutation_dict.items():
        for group, value in holder.items():
            total *= value
    return total

def group_resolver(actions):
    groups = {}
    leftovers = []
    not_random_groups = []

    for action in actions:
        group = action['randomSpawnGroupKey'] if 'randomSpawnGroupKey' in action else None
        if group is not None:
            if not group in groups:
                groups[group] = []
            groups[group].append(action)
        else:
            leftovers.append(action)
    for action in leftovers:
        packKey = action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None
        if packKey is not None:
            add_pack_to_group(action, groups)
        else:
            not_random_groups.append(action)
    if len(not_random_groups) > 0:
        raise Exception("not random groups is not 0 in group resolver")
    return groups


def add_pack_to_group(action, groups):
    # print(action)
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
            pack_key = action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None
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
                if action['hiddenGroup'] == "copper_r":
                    continue
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


def get_wave_spawns_data(stage_data, levelId, log=False):
    waves_data = itemgetter(
        'waves')(compress_waves(stage_data, levelId))
    normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes'], levelId, stage_data['mapData']))
    if levelId == 'level_rogue4_b-8':
        normal_group_name = "normal_amiya"
        elite_group_name = "hard_amiya"
    log and print('levelId:', levelId, 'normal:', normal_group_name, 'elite:',
                  elite_group_name, 'replace:', enemies_to_replace)
    has_bonus_wave = pattern.match(levelId) or levelId in sp_stages_with_bonus
    holder = ['NORMAL']
    if elite_group_name is not None or len(enemies_to_replace) > 0:
        holder.append("ELITE")
    bonus_data = None
    results = {"enemy_list": {}, "elite_enemy_list": None, "sp_count": None,
               "elite_sp_count": None, "enemy_counts": [], "elite_enemy_counts": None}
    if has_bonus_wave:
        bonus_data = get_bonus(stage_data)
    for diff_group in holder:
        group_name = normal_group_name if diff_group == "NORMAL" else elite_group_name
        difficulty = 0 if diff_group == "NORMAL" else 4
        analysis = analyze_enemy_spawns(
            waves_data, levelId, bonus_data, difficulty, group_name, enemies_to_replace, stage_data)
        list, counts, absolute_bonus_count = itemgetter(
            'enemy_list', 'enemy_counts', 'absolute_bonus_count')(analysis)
        if diff_group == "NORMAL":
            results['enemy_list'] = list
            results['sp_count'] = absolute_bonus_count
            results['enemy_counts'] = counts
        else:
            results['elite_enemy_list'] = list
            results['elite_sp_count'] = absolute_bonus_count
            results['elite_enemy_counts'] = counts
    # print(results)
    return results


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
                group = action['randomSpawnGroupKey'] if 'randomSpawnGroupKey' in action else None
                packKey = action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None
                actionType = action['actionType']
                if not actionType in ['SPAWN', "EMPTY"]:
                    if not (stage_id == 'level_rogue4_4-10' and action['key'] == "trap_760_skztzs#0"):
                        continue
                if action['hiddenGroup'] and not action['hiddenGroup'] in [group_name]:
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
            # STEP 1.2 - Generate permutations based on groups

            log and print('groups before', groups)
            random_groups = group_resolver(groups)

            groups = random_group_resolver(random_groups)
            log and print('groups after', groups)
            if (len(groups) > 0):
                key = f"w{wave_idx}f{frag_index}"
                for group_key in groups:
                    if not key in permutations:
                        permutations[key] = {}
                    permutations[key][group_key] = len(
                        groups[group_key])
    return permutate(permutations, log)


"""
{
    1: {  g1 : [0,1],
          g2 : [0,1]},
    2: {  g1 : [0,1]}
}
"""


def permutate(permutations, log=False):
    log and print('permutations')
    log and pp.pprint(permutations)
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
    log and pp.pprint(temp)
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
                if action['key'] != "" and not 'trap' in action['key']:
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
                             "randomSpawnGroupKey": action['randomSpawnGroupKey'] if 'randomSpawnGroupKey' in action else None,
                             "randomSpawnGroupPackKey": action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None,
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
                         "randomSpawnGroupKey": action['randomSpawnGroupKey'] if 'randomSpawnGroupKey' in action else None,
                         "randomSpawnGroupPackKey": action['randomSpawnGroupPackKey'] if 'randomSpawnGroupPackKey' in action else None,
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


def get_waves_data(stage_data, levelId, log=False, test=False):
    routes, waves_data, extra_routes, branches, map_data = itemgetter(
        'routes', 'waves', 'extra_routes', 'branches', 'map_data')(compress_waves(stage_data, levelId))
    normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes'], levelId, stage_data['mapData']))
    if levelId == 'level_rogue4_b-8':
        normal_group_name = "normal_amiya"
        elite_group_name = "hard_amiya"
    log and print('normal:', normal_group_name, 'elite:',
                  elite_group_name, 'replace:', enemies_to_replace)
    has_bonus_wave = pattern.match(levelId) or levelId in sp_stages_with_bonus
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
