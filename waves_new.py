import os
import json
import pprint
import itertools
from itertools import combinations
from operator import itemgetter
import copy

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

bonus_enemies = ['enemy_2001_duckmi', 'enemy_2002_bearmi', 'enemy_2034_sythef']


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


def get_runes_data(runes):
    normal_group_name = None
    elite_group_name = None
    enemies_to_replace = {}
    if runes is not None:
        for rune in runes:
            key = rune['key']
            if rune['difficultyMask'] == "FOUR_STAR":
                if key == 'level_hidden_group_enable':
                    elite_group_name = rune['blackboard'][0]['valueStr']
                elif key == 'level_enemy_replace':
                    enemies_to_replace[rune['blackboard'][0]
                                       ['valueStr']] = rune['blackboard'][1]['valueStr']
            elif rune['difficultyMask'] == 'NORMAL' and key == 'level_hidden_group_enable':
                normal_group_name = rune['blackboard'][0]['valueStr']
    return {'normal_group_name': normal_group_name, 'elite_group_name': elite_group_name, 'enemies_to_replace': enemies_to_replace}


def get_hidden_groups(waves, normal_group_name, elite_group_name):
    hidden_groups = []
    for wave_idx, wave in enumerate(waves):
        for frag_index, fragment in enumerate(wave['fragments']):
            for action in fragment['actions']:
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']
                if actionType != 'SPAWN':
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
        pp.pprint(extra_groups)
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


def get_wave_permutations(stage_data, permutation, hidden_groups, has_bonus_wave, bonus_frag_index, log=False):
    waves = copy.deepcopy(stage_data['waves'])
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
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

                if actionType != 'SPAWN':
                    continue
                if hidden_group is not None and hidden_group not in hidden_groups:
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
                else:
                    actions.append(action)

            random_groups = group_resolver(groups)
            groups = random_group_resolver(random_groups)
            for groupKey in groups:
                choice = permutation[frag_index][groupKey]
                actions.append(groups[groupKey][choice])

            fragment['actions'] = flatten(actions)
    return waves


def get_bonus(stage_data):
    waves = copy.deepcopy(stage_data['waves'])
    max_frag_index = 0
    bonus_frag_index = -1
    type = "wave"
    for wave_idx, wave in enumerate(waves):
        for frag_index, fragment in enumerate(wave['fragments']):
            if frag_index > max_frag_index:
                max_frag_index = frag_index
            for action in fragment['actions']:
                if action['key'] == 'enemy_2002_bearmi':
                    bonus_fragment = fragment
                    bonus_frag_index = frag_index
                    if wave_idx == 0:
                        type = "fragment"
                    break
    if type == "wave":
        return {"type": "wave", "data": waves[1], "frag_index": -1}
    else:
        print('max_frag_index', max_frag_index)
        return {"type": type, "data": bonus_fragment, "frag_index": bonus_frag_index}


def get_group_permutations(stage_data, hidden_groups, has_bonus_wave, bonus_frag_index):
    waves = copy.deepcopy(stage_data['waves'])
    permutations = {}
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

                if actionType != 'SPAWN':
                    continue
                if hidden_group is not None and hidden_group not in hidden_groups:
                    continue
                if group is not None or packKey is not None:
                    groups.append(action)
            # STEP 1.2 - Generate permutations based on groups
            random_groups = group_resolver(groups)
            groups = random_group_resolver(random_groups)
            if (len(groups) > 0):
                for group_key in groups:
                    if not frag_index in permutations:
                        permutations[frag_index] = {}
                    permutations[frag_index][group_key] = len(
                        groups[group_key])
    pp.pprint(permutations)
    return permutate(permutations)


"""
{
    1: {  g1 : [0,1],
          g2 : [0,1]},
    2: {  g1 : [0,1]}
}
"""


def permutate(permutations):
    permutations_list = []
    p_holder = []
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
    result = (list(map(list, itertools.product(*permutations_list))))
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
    return temp


def create_timeline(waves, tag, enemies_to_replace, has_bonus_wave):
    timelines = []
    total_count = 0
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
            continue
        prev_phase_time = 0
        spawns = {}
        wave_blocking_spawns = {}
        for index, fragment in enumerate(wave['fragments']):
            prev_phase_time += fragment['preDelay']
            for action in fragment['actions']:
                if action['key'] != "" and action['isUnharmfulAndAlwaysCountAsKilled'] is False:
                    total_count += action['count']
                if tag == 'ELITE' and action['key'] in enemies_to_replace:
                    action['key'] = enemies_to_replace[action['key']]
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
        sorted_dict = {i: spawns[i] for i in myKeys}
        timelines.append({
            "preDelay": wave['preDelay'],
            "postDelay": wave['postDelay'],
            "maxTimeWaitingForNextWave": wave['maxTimeWaitingForNextWave'],
            "timeline": sorted_dict})
    return {"timelines": timelines, "count": total_count}


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


def get_timeline(folder, stage_id, log=False):
    stage_data_path = os.path.join(
        script_dir, f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}/{stage_id}")
    with open(stage_data_path, encoding="utf-8") as f:
        stage_data = json.load(f)
        normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
            'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes']))
        log and print('normal:', normal_group_name, 'elite:',
                      elite_group_name, 'replace:', enemies_to_replace)
        has_bonus_wave = not (
            '_ev-' in stage_id or '_t-' in stage_id or "_b-" in stage_id)
        hidden_groups = get_hidden_groups(
            stage_data['waves'], normal_group_name, elite_group_name)
        log and print('hidden groups', hidden_groups)
        result = generate_all_permutations(hidden_groups)
        log and print('result', result)

        temp = copy.deepcopy(result)
        if normal_group_name is not None:
            for perm in temp:
                perm.append(normal_group_name)
        normal_hidden_group_permutations = copy.deepcopy(temp)
        temp = copy.deepcopy(result)
        if elite_group_name is not None:
            for perm in temp:
                perm.append(elite_group_name)
        elite_hidden_group_permutations = copy.deepcopy(temp)

        log and print('normal_hidden_group_perms',
                      normal_hidden_group_permutations)
        log and print('elite_hidden_group_perms',
                      elite_hidden_group_permutations)

        return_data = {}
        holder = [{"tag": "NORMAL", "list": normal_hidden_group_permutations}]
        bonus_frag_index = -1
        if has_bonus_wave:
            bonus_data = get_bonus(stage_data)
            bonus_frag_index = bonus_data['frag_index']
            holder.append(
                {"tag": "ELITE", "list": elite_hidden_group_permutations})
        for data in holder:
            for hidden_group_grouplist in data['list']:
                permutations = get_group_permutations(
                    stage_data, hidden_group_grouplist, has_bonus_wave, bonus_frag_index)
                for permutation in permutations:
                    wave_data = get_wave_permutations(
                        stage_data, permutation, hidden_group_grouplist, has_bonus_wave, bonus_frag_index, log)
                    count, waves = itemgetter('count', 'timelines')(
                        create_timeline(wave_data, data['tag'], enemies_to_replace, has_bonus_wave))
                    
                    tags = copy.deepcopy(hidden_group_grouplist)
                    if normal_group_name in tags:
                        tags.remove(normal_group_name)
                    if elite_group_name in tags:
                        tags.remove(elite_group_name)
                    tags.append(data['tag'])
                    tag_str = '|'.join(tags)
                    if not tag_str in return_data:
                        return_data[tag_str] = []
                    return_data[tag_str].append(
                        {"count": count, "waves": waves})
        if has_bonus_wave:
            return_data['bonus'] = bonus_data
        return return_data
