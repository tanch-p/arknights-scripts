KEYS_TO_TRANSLATE = {'max_hp': "hp", 'magic_resistance': "res",
                     'mass_level': "weight", 'move_speed': "ms", 'attack_speed': "aspd"}

STATS = ['hp', 'atk', 'aspd', 'range', 'def',
         'res', 'weight', 'ms', 'lifepoint']


def translateKey(key):
    if key in KEYS_TO_TRANSLATE:
        key = KEYS_TO_TRANSLATE[key]
    return key


def get_runes(runes):
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
    normal_mods = []
    elite_mods = []
    all_mods = []
    for rune in runes:
        effect = parse_rune(rune)
        if effect:
            if rune['difficultyMask'] in ['ALL', 'NONE']:
                all_mods.append(effect)
            elif rune['difficultyMask'] == 'NORMAL':
                normal_mods.append(effect)
            elif rune['difficultyMask'] == 'FOUR_STAR':
                elite_mods.append(effect)

    return {"all_mods": all_mods if len(all_mods) > 0 else None,
            "normal_mods": normal_mods if len(normal_mods) > 0 else None,
            "elite_mods": elite_mods if len(elite_mods) > 0 else None}


def parse_rune(rune):
    targets = []
    mods = []
    special = None
    other = None
    key = rune['key']

    if key == "global_buff_normal":  # in roguelike_topic_table relics
        for item in rune['blackboard']:
            if item['key'] == 'key':
                continue
            elif item['key'] == "selector.enemy_level_type":
                targets.append(item['valueStr'])
            else:
                translated_key = translateKey(item['key'])
                if translated_key in STATS:
                    mods.append(
                        {"key": translateKey(item['key']),
                            "value": item['value'] if item['value'] > 0 else 1 + item['value'],
                            "mode": "mul"})
                else:
                    mods.append(
                        {"key": translateKey(item['key']),
                            "value": item['value'] if item['value'] > 0 else 1 + item['value'],
                            "valueStr": item['valueStr']})
    elif key == 'enemy_attribute_mul' or key == 'ebuff_attribute':
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
        has_target = False
        for item in rune['blackboard']:
            if item['key'] == "char":
                has_target = True
                targets = item['valueStr'].split("|")
        if not has_target:
            targets = ["CHAR"]
        for item in rune['blackboard']:
            if item['key'] != "char":
                mods.append(
                    {"key": translateKey(item['key']),
                        "value": item['value'],
                        "mode": "mul"})
    elif key == 'char_attribute_add':
        for item in rune['blackboard']:
            if item['key'] == "char":
                targets = item['valueStr'].split("|")
        for item in rune['blackboard']:
            if item['key'] != "char":
                mods.append(
                    {"key": translateKey(item['key']),
                        "value": item['value'],
                        "mode": "add"})
    elif key in ['enemy_skill_blackb_add', 'enemy_skill_blackb_mul', 'enemy_talent_blackb_mul', 'enemy_talent_blackb_add']:
        special = {}
        mods = {"key": key}
        skill_name = "skill"
        for item in rune['blackboard']:
            if item['key'] == "enemy":
                targets = item['valueStr'].split("|")
            elif item['key'] == "skill" or not any(stat_key in item['key'] for stat_key in ['atk', 'def', 'res', 'move_speed', "duration", "attack_speed"]):
                skill_name = item['valueStr'] if item['valueStr'] else item['key']
        for item in rune['blackboard']:
            if item['key'] not in ["enemy", "skill"]:
                mods[item['key']] = item['value']
        special = {
            skill_name: mods
        }
    elif key == 'enemy_dynamic_ability_new':
        special = {}
        for item in rune['blackboard']:
            if item['key'] == "enemy":
                targets = item['valueStr'].split("|")
            if item['key'] == "key":
                if item['valueStr'] == 'invisible':
                    special = {
                        "stealth": {
                            "tooltip": {
                                "en": ["$Stealth$"],
                                "ja": ["$ステルス$"],
                                "zh": ["$隐匿$"]
                            }
                        }
                    }
                else:
                    special = {
                        item['valueStr']: {
                            "value": item['value']
                        }
                    }
    if len(targets) == 0:
        targets = ['ALL']
    if special:
        return {"targets": targets, "special": special}
    if other:
        return other
    if len(mods) > 0:
        return {"targets": targets, "mods": mods}
    return None
