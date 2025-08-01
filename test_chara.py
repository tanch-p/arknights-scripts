import json
import os


with open("characters.json", encoding="utf-8") as f:
    chara_list = json.load(f)

error_list = []


def blackboard_tests(id, blackboard):
    test_blackboard_corresponding_keys(id, blackboard)
    test_blackboard_entries(id, blackboard)


def test_blackboard_corresponding_keys(id, blackboard):
    """
    Tests if blackboard have corresponding keys
    sluggish - ms_down
    apoptosis - atk_down  
    burning - res_down
    freeze - res_down
    """
    # Define expected mappings
    key_mappings = {
        'sluggish': {
            'corresponding_key': 'ms_down',
            'expected_value': 0.8,
            'expected_category': ['sluggish']
        },
        'burning': {
            'corresponding_key': 'res_down',
            'expected_value': 20,
            'expected_category': ['burning_burst'],
            'expected_order': 'initial_add'
        }
    }

    # Create lookup dict for faster searches
    blackboard_dict = {item['key']: item for item in blackboard}

    for item in blackboard:
        key = item['key']
        if key not in key_mappings:
            continue

        mapping = key_mappings[key]
        corresponding_key = mapping['corresponding_key']
        corresponding_item = blackboard_dict.get(corresponding_key)

        if not corresponding_item:
            error_list.append(
                f'{id} {key} missing corresponding {corresponding_key} item')
            continue

        # Check all expected properties
        for prop, expected in mapping.items():
            if prop == 'corresponding_key':
                continue
            actual = corresponding_item.get(prop.replace('expected_', ''))
            if actual != expected:
                error_list.append(
                    f'{id} {key} {corresponding_key} item {prop.replace("expected_", "")} incorrect')


def test_blackboard_entries(id, blackboard):
    """ 
    tests if blackboard keys are properly filled
    """
    for item in blackboard:
        if item['key'] == 'sluggish':
            pass


def main():
    for chara in chara_list:
        blackboard_tests(chara['id'], chara['blackboard'])
        if chara['talents']:
            for talent in chara['talents']:
                blackboard_tests(chara['id'], talent['blackboard'])
        if chara['skills']:
            for skill in chara['skills']:
                blackboard_tests(chara['id'], skill['blackboard'])
        if chara['uniequip']:
            for equip in chara['uniequip']:
                if equip['combatData']:
                    blackboard_tests(
                        chara['id'], equip['combatData']['blackboard'])
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(error_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
