KEYS_TO_TRANSLATE = {'max_hp': "hp", 'magic_resistance': "res",
                     'mass_level': "weight", 'move_speed': "ms", 'attack_speed': "aspd"}


def translateKey(key):
    if key in KEYS_TO_TRANSLATE:
        key = KEYS_TO_TRANSLATE[key]
    return key


def parse_runes(runes, diff):
    """
    "elite_mods": [
      {
        "targets": ["ALL"],
        "mods": [
          {
            "key": "atk",
            "value": 1.6,
            "mode": "mul"
          },
          {
            "key": "def",
            "value": 1.2,
            "mode": "mul"
          },
          {
            "key": "hp",
            "value": 1.4,
            "mode": "mul"
          }
        ]
      }
    ],
    """
    runes_list = []
    other_runes = []
    for rune in runes:
        targets = ['ALL']
        mods = []
        key = rune['key']
        if rune['difficultyMask'] == 'NORMAL' and diff == 'normal':
            if key == 'enemy_attribute_mul' or key == 'ebuff_attribute':
                for item in rune['blackboard']:
                    if item['key'] == "enemy":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "enemy":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "mul"})
            elif key == 'enemy_attribute_add':
                for item in rune['blackboard']:
                    if item['key'] == "enemy":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "enemy":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "add"})
            elif key == 'char_attribute_mul':
                for item in rune['blackboard']:
                    if item['key'] == "char":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "char":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "mul"})
            else:
                other_runes.append(rune)
            if len(mods) > 0:
                runes_list.append({"targets": targets, "mods": mods})
        else:
            continue
        if rune['difficultyMask'] != 'NORMAL' and diff == 'elite':
            if key == 'enemy_attribute_mul' or key == 'ebuff_attribute':
                for item in rune['blackboard']:
                    if item['key'] == "enemy":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "enemy":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "mul"})
            elif key == 'enemy_attribute_add':
                for item in rune['blackboard']:
                    if item['key'] == "enemy":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "enemy":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "add"})
            elif key == 'char_attribute_mul':
                for item in rune['blackboard']:
                    if item['key'] == "char":
                        targets = item['valueStr'].split("|")
                for item in rune['blackboard']:
                    if item['key'] != "char":
                        mods.append(
                            {"key": translateKey(item['key']),
                                "value": item['value'],
                                "mode": "mul"})
            # elif key == 'enemy_skill_blackb_add':
            #     print(key)
            # elif key == 'enemy_dynamic_ability_new':
            #     print(key)
            else:
                other_runes.append(rune)
            if len(mods) > 0:
                runes_list.append({"targets": targets, "mods": mods})
    if len(runes_list) == 0:
        runes_list = None
    return {"runes": runes_list, "other_runes": other_runes}
