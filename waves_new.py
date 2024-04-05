import os
import json
import pprint
import itertools
from more_itertools import powerset
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
    enemies_to_replace = []
    if stage_data['runes'] is not None:
        for rune in runes:
            key = rune['key']
            if rune['difficultyMask'] == "FOUR_STAR":
                if key == 'level_hidden_group_enable':
                    elite_group_name = rune['blackboard'][0]['valueStr']
                elif key == 'level_enemy_replace':
                    enemies_to_replace.append(
                        {rune['blackboard'][0]['valueStr']: rune['blackboard'][1]['valueStr']})
            elif rune['difficultyMask'] == 'NORMAL' and key == 'level_hidden_group_enable':
                normal_group_name = rune['blackboard'][0]['valueStr']
    return {'normal_group_name': normal_group_name, 'elite_group_name': elite_group_name, 'enemies_to_replace': enemies_to_replace}


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

    return {"random_groups": groups, "extra_groups": extra_groups}


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


def get_wave_permutations(stage_data, permutation, log=False):
    waves = copy.deepcopy(stage_data['waves'])
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
            continue
        for frag_index, fragment in enumerate(wave['fragments']):
            groups = []
            actions = []
            for action in fragment['actions']:
                group = action['randomSpawnGroupKey']
                packKey = action['randomSpawnGroupPackKey']
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']

                if actionType != 'SPAWN':
                    continue
                if hidden_group is not None and hidden_group != normal_group_name:
                    continue
                if group is not None or packKey is not None or hidden_group is not None:
                    groups.append(action)
                else:
                    actions.append(action)

            extra_groups, random_groups = itemgetter(
                "extra_groups", "random_groups")(group_resolver(groups))

            groups = random_group_resolver(random_groups)

            for groupKey in groups:
                choice = permutation[frag_index][groupKey]
                actions.append(groups[groupKey][choice])

            fragment['actions'] = flatten(actions)
    return waves


def get_group_permutations(stage_data):
    waves = copy.deepcopy(stage_data['waves'])
    permutations = {}
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
            continue
        for frag_index, fragment in enumerate(wave['fragments']):
            groups = []
            for action in fragment['actions']:
                group = action['randomSpawnGroupKey']
                packKey = action['randomSpawnGroupPackKey']
                hidden_group = action['hiddenGroup']
                actionType = action['actionType']

                if actionType != 'SPAWN':
                    continue
                if hidden_group is not None and hidden_group != normal_group_name:
                    continue
                if group is not None or packKey is not None or hidden_group is not None:
                    groups.append(action)
            # STEP 1.2 - Generate permutations based on groups
            extra_groups, random_groups = itemgetter(
                "extra_groups", "random_groups")(group_resolver(groups))

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


def create_timeline(waves):
    timelines = []
    total_count = 0
    for wave_idx, wave in enumerate(waves):
        if has_bonus_wave and wave_idx == 1:
            continue
        prev_phase_time = 0
        spawns = {}
        for index, fragment in enumerate(wave['fragments']):
            prev_phase_time += fragment['preDelay']
            for action in fragment['actions']:
                if action['key'] == "":
                    continue
                else:
                    total_count += action['count']
                if action['count'] > 1:
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
                             }
                        )
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
                         })
            prev_phase_time = max(
                list(spawns.keys())) if len(spawns) > 0 else 0

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

stage_id = 'level_rogue3_1-1'
stage_data_path = os.path.join(
    script_dir,
    f"cn_data/zh_CN/gamedata/levels/obt/roguelike/ro3/{stage_id}.json",
)
with open(stage_data_path, encoding="utf-8") as f:
    stage_data = json.load(f)
    normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes']))
    
    has_bonus_wave = not (
        '_ev-' in stage_id or '_t-' in stage_id or "_b-" in stage_id)
    permutations = get_group_permutations(stage_data)
    data = {}
    for permutation in permutations:
        wave_data = get_wave_permutations(stage_data, permutation, log=True)
        count, waves = itemgetter('count', 'timelines')(
            create_timeline(wave_data))
        if not count in data:
            data[count] = []
        data[count].append({"tags": ["NORMAL"], "waves": waves})
    myKeys = list(data.keys())
    myKeys.sort()
    sorted_dict = {i: data[i] for i in myKeys}

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_dict, f, ensure_ascii=False, indent=4)
