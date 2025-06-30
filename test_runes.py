import traceback
from runes import get_runes
from operator import itemgetter
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

test_cases = [
    {
        "path": "ro1/level_rogue1_2-3.json",
        'id': "level_rogue1_2-3",
        'all_mods': None,
        'elite_mods': [{'targets': ['ALL'],
                        'mods': [{'key': 'atk',
                                  'mode': 'mul',
                                  'value': 1.3},
                                 {'key': 'def',
                                  'mode': 'mul',
                                  'value': 1.2},
                                 {'key': 'hp',
                                  'mode': 'mul',
                                  'value': 1.3}],
                        },
                       {'targets': ['enemy_1103_wdkght',
                                    'enemy_1103_wdkght_2'],
                        'special': {'stealth': {'tooltip': {'en': ['$Stealth$'],
                                                            'ja': ['$ステルス$'],
                                                            'zh': ['$隐匿$']}}},
                        }],
        'normal_mods': None
    },
    {
        "path": "ro3/level_rogue3_5-6.json",
        'id': "level_rogue3_5-6",
        'all_mods': [{'targets': ['trap_096_gflag'],
                      'mods': [{'key': 'hp',
                                'mode': 'add',
                                'value': 10000.0}]}],
        'elite_mods': [{
            'targets': ['ALL'],
            'mods': [{'key': 'atk',
                      'mode': 'mul',
                      'value': 1.1},
                     {'key': 'def',
                      'mode': 'mul',
                      'value': 1.2},
                     {'key': 'hp',
                      'mode': 'mul',
                      'value': 1.5}]
        },
            {'targets': ['enemy_1299_ymkilr_2'],
             'special': {'InvisibleCombat': {'atk_scale': 2.0,
                                             'key': 'enemy_skill_blackb_mul'}},
             },
            {'targets': ['enemy_1300_ymmir_2'],
             'special': {'Guide': {'attack_speed': 1.5,
                                   'duration': 1.5,
                                   'key': 'enemy_skill_blackb_mul'}},
             }],
        'normal_mods': None
    }
]


def test_runes():
    for case in test_cases:
        stage_data_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{case['path']}",
        )
        with open(stage_data_path, encoding="utf-8") as f:
            stage_data = json.load(f)
            runes_data = get_runes(
                stage_data['runes']) if stage_data['runes'] else None
            all_mods, elite_mods, normal_mods = itemgetter(
                'all_mods', 'elite_mods', 'normal_mods')((runes_data))
            try:
                assert (all_mods) == case['all_mods']
                assert (elite_mods) == case['elite_mods']
                assert (normal_mods) == case['normal_mods']

            except AssertionError as e:
                traceback.print_exc()


def main():
    test_runes()


if __name__ == "__main__":
    main()
