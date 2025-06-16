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

bonus_enemies = ['enemy_2001_duckmi', 'enemy_2002_bearmi',
                 'enemy_2034_sythef', 'enemy_2085_skzjxd']


def analyze_enemy_spawns(waves_data, levelId, bonus_data, group_name):
    """
    Analyzes enemy spawn data to calculate absolute counts for all possible spawn combinations.

    Args:
        wave_data: Dictionary containing waves data with the structure from your JSON

    Returns:
        Dictionary with analysis results including guaranteed spawns and all possible combinations
    """
    results = {
        'guaranteed_enemies': {},
        'random_group_combinations': {},
        'all_scenarios': []
    }
    # Track guaranteed spawns (non-grouped)
    guaranteed_spawns = {}

    # Track random groups per fragment
    fragment_groups = []
    print('group name:', group_name)
    # Process each wave
    for wave_index, wave in enumerate(waves_data):
        if bonus_data['type'] == 'wave' and wave_index == bonus_data['wave_index']:
            continue
        for fragment_index, fragment in enumerate(wave['fragments']):
            if bonus_data['type'] == 'fragment' and wave_index == bonus_data['wave_index'] and fragment_index == bonus_data['frag_index']:
                continue
            # Get all SPAWN actions only
            spawn_actions = [action for action in fragment['actions']
                             if action['actionType'] == 'SPAWN']

            # Track groups within this fragment
            fragment_random_groups = {}

            # get groups within the fragment to facilitate pack processing later
            for action in spawn_actions:
                if action['hiddenGroup'] is not None and (action['hiddenGroup'] != group_name or group_name is None):
                    continue
                if action['randomSpawnGroupKey']:
                    group_key = action['randomSpawnGroupKey']
                    if group_key not in fragment_random_groups:
                        fragment_random_groups[group_key] = {
                            'options': [],
                            'total_weight': 0,
                            'location': f"Wave {wave_index + 1}, Fragment {fragment_index + 1}"
                        }
                    fragment_random_groups[group_key]['options'].append({
                        'actions': [action],
                        'packKey': action['randomSpawnGroupPackKey'],
                        'weight': action['weight'],
                        'probability': 0  # Will calculate after collecting all
                    })
                    fragment_random_groups[group_key]['total_weight'] += action['weight']

            # Separate packed and non-packed actions within this fragment
            for action in spawn_actions:
                if action['hiddenGroup'] is not None and (action['hiddenGroup'] != group_name or group_name is None):
                    continue
                enemy_key = action['key']
                if action['randomSpawnGroupPackKey']:
                    pack_key = action['randomSpawnGroupPackKey']
                    for group_key in fragment_random_groups:
                        for option in fragment_random_groups[group_key]['options']:
                            if option['packKey'] == pack_key:
                                option['actions'].append(action)

                elif action['randomSpawnGroupKey']:
                    continue
                else:
                    # Guaranteed spawn
                    if enemy_key not in guaranteed_spawns:
                        guaranteed_spawns[enemy_key] = 0
                    guaranteed_spawns[enemy_key] += action['count']

            # Add this fragment's groups to the collection if it has any
            if fragment_random_groups:
                fragment_groups.append({
                    'location': f"Wave {wave_index + 1}, Fragment {fragment_index + 1}",
                    'groups': fragment_random_groups
                })
    pp.pprint(guaranteed_spawns)
    pp.pprint(fragment_groups)
    # Calculate probabilities for random groups within each fragment
    all_groups = {}
    for fragment_data in fragment_groups:
        for group_key, group_data in fragment_data['groups'].items():
            for option in group_data['options']:
                option['probability'] = option['weight'] / \
                    group_data['total_weight'] if group_data['total_weight'] > 0 else 0

            # Create unique key for this group instance
            unique_key = f"{group_key}_{fragment_data['location']}"
            all_groups[unique_key] = group_data

    results['guaranteed_enemies'] = guaranteed_spawns
    results['random_group_combinations'] = all_groups
    results['fragment_groups'] = fragment_groups

    # Generate all possible scenarios
    def generate_scenarios():
        if not fragment_groups:
            # No random groups, only guaranteed spawns
            return [{
                'enemies': guaranteed_spawns.copy(),
                'total_enemies': sum(guaranteed_spawns.values()),
                'probability': 1.0,
                'selections': {}
            }]
        base_count = sum(guaranteed_spawns.values())
        scenarios = []

        analyze_spawns(fragment_groups)

        return scenarios

    all_scenarios = generate_scenarios()
    # Sort by probability (highest first)
    all_scenarios.sort(key=lambda x: x['probability'], reverse=True)
    results['all_scenarios'] = all_scenarios

    return results

def analyze_spawns(spawn_data):
    """
    Analyze enemy spawn data to calculate counts and probabilities.
    
    Args:
        spawn_data (list): List of spawn fragments with groups and options
        
    Returns:
        dict: Analysis results organized by group, pack, enemy type, and summary
    """
    analysis = {
        'by_group': {},
        'by_pack': {},
        'by_enemy': {},
        'summary': {
            'total_fragments': len(spawn_data),
            'total_groups': 0,
            'total_packs': 0,
            'total_enemy_types': 0
        }
    }
    
    for fragment in spawn_data:
        location = fragment['location']
        
        for group_key, group_data in fragment['groups'].items():
            # Initialize group if not exists
            if group_key not in analysis['by_group']:
                analysis['by_group'][group_key] = {
                    'total_weight': 0,
                    'options': [],
                    'locations': [],
                    'total_enemy_count': 0
                }
            
            analysis['by_group'][group_key]['locations'].append(location)
            analysis['by_group'][group_key]['total_weight'] += group_data['total_weight']
            
            for option in group_data['options']:
                probability = option['weight'] / group_data['total_weight']
                
                # Analyze each action in the option
                for action in option['actions']:
                    if action['actionType'] == 'SPAWN' and action['key']:
                        enemy_key = action['key']
                        count = action.get('count', 1)
                        pack_key = action.get('randomSpawnGroupPackKey')
                        
                        # Group analysis
                        analysis['by_group'][group_key]['options'].append({
                            'location': location,
                            'pack_key': pack_key,
                            'enemy_key': enemy_key,
                            'count': count,
                            'weight': option['weight'],
                            'probability': probability,
                            'route_index': action.get('routeIndex')
                        })
                        analysis['by_group'][group_key]['total_enemy_count'] += count
                        
                        # Pack analysis
                        if pack_key:
                            full_pack_key = f"{group_key}_{pack_key}"
                            if full_pack_key not in analysis['by_pack']:
                                analysis['by_pack'][full_pack_key] = {
                                    'group': group_key,
                                    'pack_key': pack_key,
                                    'enemies': {},
                                    'total_count': 0,
                                    'locations': [],
                                    'probability': 0
                                }
                            
                            if enemy_key not in analysis['by_pack'][full_pack_key]['enemies']:
                                analysis['by_pack'][full_pack_key]['enemies'][enemy_key] = 0
                            
                            analysis['by_pack'][full_pack_key]['enemies'][enemy_key] += count
                            analysis['by_pack'][full_pack_key]['total_count'] += count
                            analysis['by_pack'][full_pack_key]['probability'] = probability
                            
                            if location not in analysis['by_pack'][full_pack_key]['locations']:
                                analysis['by_pack'][full_pack_key]['locations'].append(location)
                        
                        # Enemy type analysis
                        if enemy_key not in analysis['by_enemy']:
                            analysis['by_enemy'][enemy_key] = {
                                'total_count': 0,
                                'groups': {},
                                'packs': {},
                                'locations': []
                            }
                        
                        analysis['by_enemy'][enemy_key]['total_count'] += count
                        
                        if group_key not in analysis['by_enemy'][enemy_key]['groups']:
                            analysis['by_enemy'][enemy_key]['groups'][group_key] = 0
                        analysis['by_enemy'][enemy_key]['groups'][group_key] += count
                        
                        if pack_key:
                            full_pack_key = f"{group_key}_{pack_key}"
                            if full_pack_key not in analysis['by_enemy'][enemy_key]['packs']:
                                analysis['by_enemy'][enemy_key]['packs'][full_pack_key] = 0
                            analysis['by_enemy'][enemy_key]['packs'][full_pack_key] += count
                        
                        if location not in analysis['by_enemy'][enemy_key]['locations']:
                            analysis['by_enemy'][enemy_key]['locations'].append(location)
    
    # Calculate summary statistics
    analysis['summary']['total_groups'] = len(analysis['by_group'])
    analysis['summary']['total_packs'] = len(analysis['by_pack'])
    analysis['summary']['total_enemy_types'] = len(analysis['by_enemy'])
    
    return analysis


def display_analysis(analysis):
    """Display analysis results in a readable format."""
    print("=== ENEMY SPAWN ANALYSIS ===\n")
    
    print("SUMMARY:")
    print(f"- Total Fragments: {analysis['summary']['total_fragments']}")
    print(f"- Total Groups: {analysis['summary']['total_groups']}")
    print(f"- Total Packs: {analysis['summary']['total_packs']}")
    print(f"- Total Enemy Types: {analysis['summary']['total_enemy_types']}\n")
    
    print("BY GROUP:")
    for group_key, group_data in analysis['by_group'].items():
        print(f"\n{group_key.upper()}:")
        print(f"  Total Weight: {group_data['total_weight']}")
        print(f"  Total Enemy Count: {group_data['total_enemy_count']}")
        print(f"  Locations: {', '.join(group_data['locations'])}")
        print(f"  Options:")
        
        for i, option in enumerate(group_data['options'], 1):
            print(f"    {i}. {option['enemy_key']} (Count: {option['count']}, "
                  f"Weight: {option['weight']}, Probability: {option['probability']*100:.1f}%)")
    
    print("\nBY PACK:")
    for pack_key, pack_data in analysis['by_pack'].items():
        print(f"\n{pack_key.upper()}:")
        print(f"  Group: {pack_data['group']}")
        print(f"  Total Count: {pack_data['total_count']}")
        print(f"  Probability: {pack_data['probability']*100:.1f}%")
        print(f"  Locations: {', '.join(pack_data['locations'])}")
        print(f"  Enemies:")
        
        for enemy_key, count in pack_data['enemies'].items():
            print(f"    - {enemy_key}: {count}")
    
    print("\nBY ENEMY TYPE:")
    for enemy_key, enemy_data in analysis['by_enemy'].items():
        print(f"\n{enemy_key.upper()}:")
        print(f"  Total Count: {enemy_data['total_count']}")
        
        groups_str = ', '.join([f"{g}({c})" for g, c in enemy_data['groups'].items()])
        print(f"  Groups: {groups_str}")
        
        if enemy_data['packs']:
            packs_str = ', '.join([f"{p}({c})" for p, c in enemy_data['packs'].items()])
            print(f"  Packs: {packs_str}")
        
        print(f"  Locations: {', '.join(enemy_data['locations'])}")


def get_enemy_probabilities(analysis, group_key=None):
    """
    Get probability distribution for enemies in a specific group or overall.
    
    Args:
        analysis (dict): Analysis results from analyze_enemy_spawns()
        group_key (str, optional): Specific group to analyze. If None, analyzes all.
        
    Returns:
        dict: Enemy probabilities
    """
    if group_key and group_key in analysis['by_group']:
        group_data = analysis['by_group'][group_key]
        enemy_probs = {}
        
        for option in group_data['options']:
            enemy_key = option['enemy_key']
            if enemy_key not in enemy_probs:
                enemy_probs[enemy_key] = 0
            enemy_probs[enemy_key] += option['probability']
        
        return enemy_probs
    else:
        # Overall probabilities across all groups
        total_spawns = sum(data['total_enemy_count'] for data in analysis['by_group'].values())
        enemy_probs = {}
        
        for enemy_key, enemy_data in analysis['by_enemy'].items():
            enemy_probs[enemy_key] = enemy_data['total_count'] / total_spawns if total_spawns > 0 else 0
        
        return enemy_probs


def get_pack_summary(analysis):
    """Get a summary of all packs and their contents."""
    pack_summary = {}
    
    for pack_key, pack_data in analysis['by_pack'].items():
        pack_summary[pack_key] = {
            'group': pack_data['group'],
            'total_enemies': pack_data['total_count'],
            'probability': pack_data['probability'],
            'enemy_types': len(pack_data['enemies']),
            'enemies': dict(pack_data['enemies'])
        }
    
    return pack_summary

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


def is_countable_action(key, level_id):
    if 'trap' in key:
        return False
    if key == '':
        return False
    if key in ALWAYS_KILLED_KEYS:
        return False
    if level_id == 'level_rogue4_t-4':
        return key != 'enemy_1263_durbus'
    return True


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


def get_bonus_counts(stage_data, levelId, log=False):
    waves_data = itemgetter(
        'waves')(compress_waves(stage_data, levelId))
    normal_group_name, elite_group_name, enemies_to_replace = itemgetter(
        'normal_group_name', 'elite_group_name', 'enemies_to_replace')(get_runes_data(stage_data['runes'], levelId, stage_data['mapData']))
    if levelId == 'level_rogue4_b-8':
        normal_group_name = "normal_amiya"
        elite_group_name = "hard_amiya"
    log and print('normal:', normal_group_name, 'elite:',
                  elite_group_name, 'replace:', enemies_to_replace)
    has_bonus_wave = not (
        '_ev-' in levelId or '_t-' in levelId or "_b-" in levelId or "_d-" in levelId)
    if not has_bonus_wave:
        return None
    holder = ['NORMAL', 'ELITE']
    bonus_data = None
    if has_bonus_wave:
        bonus_data = get_bonus(stage_data)
    for diff_group in holder:
        group_name = normal_group_name if diff_group == "NORMAL" else elite_group_name
        analysis = analyze_enemy_spawns(
            waves_data, levelId, bonus_data, group_name)

    return


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
    pp.pprint(temp)
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
