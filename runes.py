import json

KEYS_TO_TRANSLATE = {'max_hp': "hp", 'magic_resistance': "res",
                     'mass_level': "weight", 'move_speed': "ms", 'attack_speed': "aspd"}

STATS = ['hp', 'atk', 'aspd', 'range', 'def',
         'res', 'weight', 'ms', 'lifepoint']

STAT_KEYS_ZH = {"hp": "生命值", 'atk': "攻击力", 'aspd': "攻击速度",
                "def": "防御力", "res": "法术耐性",
                'range': "攻击范围",  "ms": "移动速度", "weight": "重量"}
STAT_KEYS_JA = {"hp": "最大HP", 'atk': "攻撃力", 'aspd': "攻撃速度",
                "def": "防御力", "res": "術耐性",
                'range': "攻撃範囲",  "ms": "移動速度", "weight": "重量"}
STAT_KEYS_EN = {"hp": "Max HP", 'atk': "ATK", 'aspd': "ASPD",
                "def": "DEF", "res": "RES",
                'range': "Attack range",  "ms": "Movespeed", "weight": "Weight"}
with open("enemy_database.json", encoding="utf-8") as f:
    enemy_db = json.load(f)


def translateKey(key):
    if key in KEYS_TO_TRANSLATE:
        key = KEYS_TO_TRANSLATE[key]
    return key


def generate_desc(effects):
    """Returns dict of zh, ja, en"""
    if not effects:
        return {}

    # Language mappings
    lang_configs = {
        'zh': {'all_prefix': '所有敌方单位的', 'name_key': 'name_zh', 'comma': "，", 'stealth': "获得隐匿", 'stat_keys': STAT_KEYS_ZH},
        'ja': {'all_prefix': '敵全員の', 'name_key': 'name_ja', 'comma': "、", 'stealth': "がステルス状態になる", 'stat_keys': STAT_KEYS_JA},
        'en': {'all_prefix': 'All enemy units have ', 'name_key': 'name_en', 'comma': ", ", 'stealth': " gains stealth", 'stat_keys': STAT_KEYS_EN}
    }

    result = {lang: [] for lang in lang_configs}

    for effect in effects:
        texts = {}

        # Generate target text for each language
        for lang, config in lang_configs.items():
            if "ALL" in effect['targets']:
                texts[lang] = config['all_prefix']
            else:
                target_names = []
                for target in effect['targets']:
                    name = enemy_db.get(target, {}).get(
                        config['name_key'], target)
                    target_names.append(f'<{name}>' if lang != 'zh' else name)
                texts[lang] = ''.join(target_names)

        # Add modifications if present
        if 'mods' in effect:
            for i, mod in enumerate(effect['mods']):
                key = mod['key']
                if key not in STATS:
                    continue
                value_str = f"+{round((mod['value'] - 1) * 100)}%" if mod['mode'] == "mul" else f"+{mod['value']}"

                for lang, config in lang_configs.items():
                    stat_key = config['stat_keys'].get(key, key)
                    if lang == 'en':
                        texts[lang] += f"{value_str} {stat_key}"
                    else:
                        texts[lang] += stat_key + value_str
                    if i != len(effect['mods'])-1:
                        texts[lang] += config['comma']
        if 'special' in effect:
            if 'stealth' in effect['special']:
                for lang, config in lang_configs.items():
                    texts[lang] += config['stealth']
            else:
                for lang, config in lang_configs.items():
                    texts[lang] += 'special'
        # Add to results
        for lang in lang_configs:
            result[lang].append(texts[lang])

    return result


def get_crisis_runes(runes):
    mods = []
    for rune in runes:
        effect = parse_rune(rune)
        if effect:
            mods.append(effect)
    return mods


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
    elif key in ['enemy_attribute_mul', 'ebuff_attribute', 'enemy_attribute_additive_mul']:
        for item in rune['blackboard']:
            if item['key'] == "enemy":
                targets = item['valueStr'].split("|")
        for item in rune['blackboard']:
            if item['key'] != "enemy":
                if key == 'enemy_attribute_additive_mul':
                    mods.append(
                        {"key": translateKey(item['key']),
                            "value": item['value'],
                            "mode": "mul",
                            "order": "initial"})
                else:
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
                        "mode": "add",
                        "order": "initial"})
    elif key == 'enemy_weight_add':
        for item in rune['blackboard']:
            if item['key'] == "enemy":
                targets = item['valueStr'].split("|")
        for item in rune['blackboard']:
            if item['key'] == "value":
                mods.append(
                    {"key": "weight",
                        "value": item['value'],
                        "mode": "add"})
    elif key == 'enemy_attackradius_mul':
        for item in rune['blackboard']:
            if item['key'] == "enemy":
                targets = item['valueStr'].split("|")
        for item in rune['blackboard']:
            if item['key'] == "scale":
                mods.append(
                    {"key": "range",
                        "value": item['value'],
                        "mode": "mul"})
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
    elif key in ['level_hidden_group_enable', 'level_hidden_group_disable']:
        targets = ['system']
        for item in rune['blackboard']:
            if item['key'] == "key":
                mods.append(
                    {
                        "key": key,
                        "value": item['value'],
                        "valueStr": item['valueStr']
                    })
    elif key in ['level_enemy_replace']:
        targets = ['system']
        target = next(
            (item['valueStr'] for item in rune['blackboard'] if item['key'] == "key"), None)
        value = next(
            (item['valueStr'] for item in rune['blackboard'] if item['key'] == "value"), None)
        mods.append(
            {
                "key": key,
                "target": target,
                "value": value
            })
    elif key in ['global_forbid_location']:
        targets = ['system']
        value = next(
            (item['valueStr'] for item in rune['blackboard'] if item['key'] == "location"), None)
        if value:
            value = value.replace("(", "").replace(")", "")
        mods.append(
            {
                "key": key,
                "value": value.split("|")
            })
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
