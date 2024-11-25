KEYS_TO_TRANSLATE = {'max_hp': "hp", 'magic_resistance': "res",
                     'mass_level': "fixed_weight", 'move_speed': "ms", 'attack_speed': "aspd"}


def translateKey(key, value):
    if key in KEYS_TO_TRANSLATE:
        key = KEYS_TO_TRANSLATE[key]
    if key != 'fixed_weight' and value >= 10:
        key = f"fixed_{key}"
    return key


def parse_runes(runes):
    runes_list = []
    other_runes = []
    for rune in runes:
        targets = ['ALL']
        mods = {}
        key = rune['key']
        if key == 'enemy_attribute_mul' or key == 'ebuff_attribute' or key == 'enemy_attribute_add':
            for item in rune['blackboard']:
                if item['key'] == "enemy":
                    targets = item['valueStr'].split("|")
            for item in rune['blackboard']:
                if item['key'] != "enemy":
                    mods[translateKey(item['key'], item['value'])
                         ] = item['value']
        if key == 'char_attribute_mul':
            for item in rune['blackboard']:
                if item['key'] == "char":
                    targets = item['valueStr'].split("|")
            for item in rune['blackboard']:
                if item['key'] != "char":
                    mods[translateKey(item['key'], item['value'])
                         ] = item['value']
        # elif key == 'enemy_skill_blackb_add':
        #     print(key)
        # elif key == 'enemy_dynamic_ability_new':
        #     print(key)
        else:
            other_runes.append(rune)
        if len(mods) > 0:
            runes_list.append({"targets": targets, "mods": mods})

    return {"runes": runes_list, "other_runes": other_runes}
