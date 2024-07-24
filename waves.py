import os
import json
import pprint
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)

KEYS_TO_EXCLUDE = ['trap_079_allydonq']


def get_wave_data(stage_data, stage_id, log=False):
    def is_trap_group(group):
        for action in group:
            key = action['key']
            if 'trap' in key or 'tutorial' in key:
                return True
        return False

    def has_bonus_wave(groups):
        has_sp_flag = False
        has_empty_flag = False
        sp_enemy_list = ["enemy_2034_sythef",
                         "enemy_2001_duckmi", "enemy_2002_bearmi","'enemy_2085_skzjxd'"]
        for group_name in groups[-1]:
            for packKey in groups[-1][group_name]:
                for action in groups[-1][group_name][packKey]:
                    key = action['key']
                    if key == '':
                        has_empty_flag = True
                    elif key in sp_enemy_list:
                        has_sp_flag = True

        return (has_empty_flag and has_sp_flag)

    def all_sums(arrays):
        if not arrays:
            return [[]]
        else:
            results = []
            for value in arrays[0]:
                for subset in all_sums(arrays[1:]):
                    results.append([value] + subset)
            return results

    def get_all_group_enemy_counts(groups_list):
        all_group_enemy_counts = []
        for fragment_group in groups_list:
            for group in fragment_group:
                pack_groups = {}
                for pack in fragment_group[group]:
                    if pack == "none":
                        enemies = {}
                        for action in fragment_group[group][pack]:
                            key = action['key']
                            count = action['count']
                            if not key in enemies:
                                enemies[key] = [count]
                            else:
                                if not count in enemies[key]:
                                    enemies[key].append(count)
                        all_group_enemy_counts.append(enemies)
                    else:
                        pack_enemies = {}
                        for action in fragment_group[group][pack]:
                            key = action['key']
                            count = action['count']
                            if not key in pack_enemies:
                                pack_enemies[key] = count
                            else:
                                pack_enemies[key] += count
                        log and print("pack_enemies: ", pack_enemies)
                        for key in pack_enemies:
                            count = pack_enemies[key]
                            if not key in pack_groups:
                                pack_groups[key] = [count]
                            else:
                                if not count in pack_groups[key]:
                                    pack_groups[key].append(count)
                #additional step for enemies that don't appear in other packs
                for pack_enemy_key in pack_groups:
                    for pack in fragment_group[group]:
                        if pack != 'none':
                            pack_enemies = {}
                            for action in fragment_group[group][pack]:
                                key = action['key']
                                count = action['count']
                                if not key in pack_enemies:
                                    pack_enemies[key] = count
                                else:
                                    pack_enemies[key] += count
                            if not pack_enemy_key in pack_enemies and not 0 in pack_groups[pack_enemy_key]:
                                pack_groups[pack_enemy_key].append(0)

                if len(pack_groups) > 0:
                    log and print("pack_groups: ", pack_groups)
                    for key in pack_groups:
                        all_group_enemy_counts.append({key: pack_groups[key]})
        return all_group_enemy_counts

    def get_all_count_permutations(groups_list):
        all_count_permutations = []
        for fragment_group in groups_list[:-1] if has_bonus_wave else groups_list:
            for group in fragment_group:
                permutations = []
                for pack in fragment_group[group]:
                    if pack == 'none':
                        for action in fragment_group[group][pack]:
                            count = action['count']
                            if action['isUnharmfulAndAlwaysCountAsKilled']:
                                count = 0
                            if action['key'] == '':
                                count = 0
                            if not count in permutations:
                                permutations.append(count)
                    else:
                        count = 0
                        for action in fragment_group[group][pack]:
                            count += action['count']
                        if not count in permutations:
                            permutations.append(count)
                all_count_permutations.append(permutations)
        return all_count_permutations

    def get_all_possible_enemy_counts(base_enemy_count, sums):
        sums_added_up = []
        for sum_array in sums:
            sums_added_up.append(base_enemy_count + (sum(sum_array)))
        all_possible_enemy_count = list(set(sums_added_up))
        all_possible_enemy_count.sort()
        log and print(f"all possible enemy counts: {all_possible_enemy_count}")
        return all_possible_enemy_count

    def get_bonus_count(all_possible_enemy_count):
        all_bonus_enemy_count = [
            count+1 for count in all_possible_enemy_count]
        all_absolute_bonus_enemy_count = list(set(
            all_bonus_enemy_count).difference(set(all_possible_enemy_count)))
        all_absolute_bonus_enemy_count.sort()
        log and print(
            f"absolute bonus count: {all_absolute_bonus_enemy_count}")
        return all_absolute_bonus_enemy_count

    def check_pack_key(stage_data):
        for wave in stage_data["waves"]:
            for fragment in wave['fragments']:
                for action in fragment['actions']:
                    if action['randomSpawnGroupPackKey'] is not None:
                        return True
        return False

    def get_fragment_grouplist(fragment, difficulty, frag_index, stage_id):
        groups = {}
        for action in fragment['actions']:
            key = action['key']
            group = action['randomSpawnGroupKey']
            packKey = action['randomSpawnGroupPackKey']
            hidden_group = action['hiddenGroup']
            actionType = action['actionType']

            if stage_id == 'level_rogue3_3-2' and frag_index == 7:
                if key == 'enemy_1075_dmgswd' or key == 'enemy_1084_sotidm':
                    continue

            if actionType != 'SPAWN':
                continue
            if hidden_group in ['allydonq', "totem1", 'totem2', 'bossrelic', 'calamity', 'cargo', 'hidden_door']:
                continue
            if difficulty == 2:
                for enemy in enemies_to_replace:
                    if key in enemy:
                        key = enemy[key]

            if difficulty == 2 and hidden_group == elite_group_name:
                if not group is None:
                    if not group in groups:
                        groups[group] = {}
                    pack = packKey if packKey else "none"
                    if not pack in groups[group]:
                        groups[group][pack] = []
                    groups[group][pack].append(
                        {"key": key, "count": action['count'], "weight": action['weight'], "packKey": packKey, "isUnharmfulAndAlwaysCountAsKilled": action['isUnharmfulAndAlwaysCountAsKilled']})
            elif difficulty == 1 and hidden_group != elite_group_name:
                if not group is None:
                    if not group in groups:
                        groups[group] = {}
                    pack = packKey if packKey else "none"
                    if not pack in groups[group]:
                        groups[group][pack] = []
                    groups[group][pack].append(
                        {"key": key, "count": action['count'], "weight": action['weight'], "packKey": packKey, "isUnharmfulAndAlwaysCountAsKilled": action['isUnharmfulAndAlwaysCountAsKilled']})
            elif hidden_group is None:
                if not group is None:
                    if not group in groups:
                        groups[group] = {}
                    pack = packKey if packKey else "none"
                    if not pack in groups[group]:
                        groups[group][pack] = []
                    groups[group][pack].append(
                        {"key": key, "count": action['count'], "weight": action['weight'], "packKey": packKey, "isUnharmfulAndAlwaysCountAsKilled": action['isUnharmfulAndAlwaysCountAsKilled']})
        return groups

    def distill_wave_data(stage_data, difficulty=1):
        waves = stage_data["waves"]
        base_enemy_count = 0
        enemy_list = {}
        groups_list = []

        for wave_idx, wave in enumerate(waves):
            for frag_index, fragment in enumerate(wave['fragments']):
                groups = get_fragment_grouplist(
                    fragment, difficulty, frag_index, stage_id)
                for action in fragment['actions']:
                    key = action['key']
                    group = action['randomSpawnGroupKey']
                    packKey = action['randomSpawnGroupPackKey']
                    hidden_group = action['hiddenGroup']
                    actionType = action['actionType']

                    if actionType != 'SPAWN':
                        continue
                    if stage_id == 'level_rogue3_3-2' and frag_index == 7:
                        if key == 'enemy_1075_dmgswd' or key == 'enemy_1084_sotidm':
                            continue

                    if difficulty == 2:
                        for enemy in enemies_to_replace:
                            if key in enemy:
                                key = enemy[key]

                    if group is not None:
                        continue

                    # get data for normal
                    if hidden_group in ['allydonq', "totem1", 'totem2', 'bossrelic', 'calamity', 'cargo', 'hidden_door']:
                        continue

                    if difficulty == 2 and hidden_group is not None and hidden_group != elite_group_name:
                        continue

                    if hidden_group is not None and hidden_group == elite_group_name:
                        if difficulty == 2:
                            if packKey is not None:
                                pack_group = None
                                for group in groups:
                                    if packKey in groups[group]:
                                        pack_group = group
                                        break
                                groups[pack_group][packKey].append(
                                    {"key": key, "count": action['count'], "weight": action['weight'], "packKey": packKey, "isUnharmfulAndAlwaysCountAsKilled": action['isUnharmfulAndAlwaysCountAsKilled']})
                            else:
                                base_enemy_count += action['count']
                                if not key in enemy_list:
                                    enemy_list[key] = {
                                        "min_count": action['count'], "max_count": action['count']}
                                elif key in enemy_list:
                                    enemy_list[key]['min_count'] += action['count']
                                    enemy_list[key]['max_count'] += action['count']
                        else:
                            continue

                    elif packKey is not None:
                        pack_group = None
                        for group in groups:
                            if packKey in groups[group]:
                                pack_group = group
                                break
                        if pack_group is None:
                            pack_group = packKey
                        if not pack_group in groups:
                            groups[pack_group] = {}
                        if not packKey in groups[pack_group]:
                            groups[pack_group][packKey] = []
                        groups[pack_group][packKey].append(
                            {"key": key, "count": action['count'], "weight": action['weight'], "packKey": packKey, "isUnharmfulAndAlwaysCountAsKilled": action['isUnharmfulAndAlwaysCountAsKilled']})
                    else:
                        base_enemy_count += action['count']

                        if not key in enemy_list:
                            enemy_list[key] = {
                                "min_count": action['count'], "max_count": action['count']}
                        elif key in enemy_list:
                            enemy_list[key]['min_count'] += action['count']
                            enemy_list[key]['max_count'] += action['count']

                if len(groups) > 0:
                    groups_list.append(groups)

        return {"base_enemy_count": base_enemy_count, "enemy_list": json.dumps(enemy_list), "groups_list": json.dumps(groups_list)}
    log and print(stage_id)
    enemies_to_replace = []
    elite_group_name = None
    absolute_sp_counts = None
    absolute_elite_sp_counts = None
    elite_enemy_list = None
    all_possible_elite_enemy_count = None

    if stage_data['runes'] is not None:
        for rune in stage_data['runes']:
            if rune['difficultyMask'] == "FOUR_STAR":
                if rune['key'] == 'level_hidden_group_enable':
                    elite_group_name = rune['blackboard'][0]['valueStr']
                elif rune['key'] == 'level_enemy_replace':
                    enemies_to_replace.append(
                        {rune['blackboard'][0]['valueStr']: rune['blackboard'][1]['valueStr']})
    # has_pack_key = check_pack_key(stage_data)
    # if has_pack_key:
    #     print(stage_data['randomSeed'])
    data = distill_wave_data(stage_data)
    base_enemy_count, enemy_list, groups_list = itemgetter(
        'base_enemy_count', 'enemy_list', 'groups_list')(data)
    enemy_list = json.loads(enemy_list)
    groups_list = json.loads(groups_list)

    has_bonus_wave = has_bonus_wave(
        groups_list) if len(groups_list) > 0 else False

    log and pp.pprint(enemy_list)
    log and print(f"elite: {elite_enemy_list}")
    log and print(f"base count: {base_enemy_count}")

    if len(groups_list) > 0:
        log and print("randomSpawnGroup list:")
        log and pp.pprint(groups_list)
    else:
        log and print("No randomSpawnGroups")

    # group enemy count for indiv enemy counting

    all_group_enemy_counts = get_all_group_enemy_counts(groups_list)

    log and pp.pprint(all_group_enemy_counts)

    for group in all_group_enemy_counts:
        for key in group:
            if key == '':
                continue
            if not key in enemy_list:
                enemy_list[key] = {"min_count": 0, "max_count": 0}
            if len(group) == 1:
                enemy_list[key]['min_count'] += min(group[key])
                enemy_list[key]['max_count'] += max(group[key])
            else:
                enemy_list[key]['max_count'] += max(group[key])
    log and print("enemy list: ")
    log and pp.pprint(enemy_list)

    all_count_permutations = get_all_count_permutations(groups_list)
    sums = all_sums(all_count_permutations)

    # log and pp.pprint(all_count_permutations)
    # log and pp.pprint(sums)
    if stage_id == "level_rogue4_t-4": #lazy hack
        base_enemy_count -= 39
    if stage_id == "level_rogue4_t-2": #lazy hack
        base_enemy_count -= 2
    all_possible_enemy_count = get_all_possible_enemy_counts(
        base_enemy_count, sums)

    if has_bonus_wave:
        absolute_sp_counts = get_bonus_count(all_possible_enemy_count)

    if elite_group_name is not None or len(enemies_to_replace) > 0:
        data = distill_wave_data(stage_data, 2)
        elite_base_enemy_count, elite_enemy_list, elite_groups_list = itemgetter(
            'base_enemy_count', 'enemy_list', 'groups_list')(data)
        elite_enemy_list = json.loads(elite_enemy_list)
        elite_groups_list = json.loads(elite_groups_list)
        log and print(f"elite base count: {elite_base_enemy_count}")
        log and pp.pprint(elite_groups_list)

        all_elite_group_enemy_counts = get_all_group_enemy_counts(
            elite_groups_list)
        log and pp.pprint(all_elite_group_enemy_counts)
        for group in all_elite_group_enemy_counts:
            for key in group:
                if key == '':
                    continue
                if not key in elite_enemy_list:
                    elite_enemy_list[key] = {"min_count": 0, "max_count": 0}
                if len(group) == 1:
                    elite_enemy_list[key]['min_count'] += min(group[key])
                    elite_enemy_list[key]['max_count'] += max(group[key])
                else:
                    elite_enemy_list[key]['max_count'] += max(group[key])
        log and print("elite enemy list: ")
        log and pp.pprint(elite_enemy_list)
        if stage_id == "level_rogue4_t-4": #lazy hack
            elite_base_enemy_count -= 39
        if stage_id == "level_rogue4_t-2":
            elite_base_enemy_count -= 10
        all_count_permutations = get_all_count_permutations(
            elite_groups_list)
        sums = all_sums(all_count_permutations)
        all_possible_elite_enemy_count = get_all_possible_enemy_counts(
            elite_base_enemy_count, sums)

        if has_bonus_wave:
            absolute_elite_sp_counts = get_bonus_count(
                all_possible_elite_enemy_count)

    enemy_list = [{"key": key, "min_count": enemy_list[key]["min_count"],
                   "max_count": enemy_list[key]["max_count"]} for key in enemy_list]
    if elite_enemy_list is not None:
        elite_enemy_list = [{"key": key, "min_count": elite_enemy_list[key]["min_count"],
                            "max_count": elite_enemy_list[key]["max_count"]} for key in elite_enemy_list]

    return {"enemy_list": enemy_list, "elite_enemy_list": elite_enemy_list, "all_possible_enemy_count": all_possible_enemy_count, "all_possible_elite_enemy_count": all_possible_elite_enemy_count, "sp_count": absolute_sp_counts, "elite_sp_count": absolute_elite_sp_counts}


script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

# stage_data_path = os.path.join(
#     script_dir,
#     f"zh_CN/gamedata/levels/obt/roguelike/ro3/level_rogue3_1-3.json",
# )
# with open(stage_data_path, encoding="utf-8") as f:
#     stage_data = json.load(f)
#     wave_data = get_wave_data(stage_data, log=True)
