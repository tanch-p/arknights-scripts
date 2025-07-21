import traceback
from waves_new import get_wave_spawns_data
from operator import itemgetter
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

test_cases = [
    {
        "path": "ro1/level_rogue1_3-1.json",
        'id': "level_rogue1_3-1",
        "enemy_counts": [64, 65, 66],
        "elite_enemy_counts": [64, 65, 66],
        "sp_count": [67],
        "elite_sp_count": [67],
        "enemy_list": [
            {
                "key": "enemy_1109_uabone",
                "min_count": 5,
                "max_count": 6
            },
            {
                "key": "enemy_3001_upeopl",
                "min_count": 7,
                "max_count": 7
            },
            {
                "key": "enemy_1107_uoffcr",
                "min_count": 17,
                "max_count": 18
            },
            {
                "key": "enemy_1007_slime_3",
                "min_count": 22,
                "max_count": 22
            },
            {
                "key": "enemy_1016_diaman",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1111_ucommd",
                "min_count": 5,
                "max_count": 6
            },
            {
                "key": "enemy_1110_uamord",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1107_uoffcr_2",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1109_uabone_2",
                "min_count": 0,
                "max_count": 1
            },
            {
                "key": "enemy_1111_ucommd_2",
                "min_count": 0,
                "max_count": 1
            }
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_1109_uabone_2",
                "min_count": 5,
                "max_count": 6
            },
            {
                "key": "enemy_3001_upeopl",
                "min_count": 7,
                "max_count": 7
            },
            {
                "key": "enemy_1107_uoffcr",
                "min_count": 17,
                "max_count": 18
            },
            {
                "key": "enemy_1007_slime_3",
                "min_count": 22,
                "max_count": 22
            },
            {
                "key": "enemy_1016_diaman",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1111_ucommd_2",
                "min_count": 6,
                "max_count": 6
            },
            {
                "key": "enemy_1110_uamord",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1107_uoffcr_2",
                "min_count": 3,
                "max_count": 3
            },]
    },
    {
        "path": "ro1/level_rogue1_4-6.json",
        'id': "level_rogue1_4-6",
        "enemy_counts": [19, 20, 21, 22, 23],
        "elite_enemy_counts": None,
        "sp_count": [24],
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_2010_csdcr",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_2009_csaudc",
                "min_count": 6,
                "max_count": 10
            },
            {
                "key": "enemy_2012_csbln",
                "min_count": 10,
                "max_count": 10
            }
        ],
        "elite_enemy_list": None
    },
    {
        "path": "ro2/level_rogue2_1-1.json",
        'id': "level_rogue2_1-1",
        "enemy_counts": [22, 23, 24, 25, 26, 27, 29, 31],
        "elite_enemy_counts": None,
        "sp_count": [28, 30, 32],
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_1007_slime_2",
                "min_count": 8,
                "max_count": 14
            },
            {
                "key": "enemy_1007_slime",
                "min_count": 9,
                "max_count": 14
            },
            {
                "key": "enemy_1158_divman",
                "min_count": 3,
                "max_count": 4
            },
            {
                "key": "enemy_1159_swfmob",
                "min_count": 0,
                "max_count": 5
            }
        ],
        "elite_enemy_list": None
    },
    {
        "path": "ro2/level_rogue2_3-5.json",
        'id': "level_rogue2_3-5",
        "enemy_counts": [47],
        "elite_enemy_counts": [46],
        "sp_count": [48],
        "elite_sp_count": [47],
        "enemy_list": [
            {
                "key": "enemy_1062_rager",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_1000_gopro_3",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_1008_ghost",
                "min_count": 15,
                "max_count": 15
            },
            {
                "key": "enemy_1021_bslime",
                "min_count": 19,
                "max_count": 19
            },
            {
                "key": "enemy_1021_bslime_2",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1026_aghost",
                "min_count": 2,
                "max_count": 2
            }
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_1000_gopro_3",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_1063_rageth",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1008_ghost",
                "min_count": 15,
                "max_count": 15
            },
            {
                "key": "enemy_1021_bslime",
                "min_count": 19,
                "max_count": 19
            },
            {
                "key": "enemy_1021_bslime_2",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1026_aghost",
                "min_count": 2,
                "max_count": 2
            },
        ]
    },
    {
        "path": "ro3/level_rogue3_1-2.json",
        'id': "level_rogue3_1-2",
        "enemy_counts": [31],
        "elite_enemy_counts": [31],
        "sp_count": [32],
        "elite_sp_count": [32],
        "enemy_list": [
            {
                "key": "enemy_1007_slime",
                "min_count": 16,
                "max_count": 16
            },
            {
                "key": "enemy_1007_slime_2",
                "min_count": 11,
                "max_count": 11
            },
            {
                "key": "enemy_1101_plkght",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1075_dmgswd",
                "min_count": 2,
                "max_count": 2
            },
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_1007_slime",
                "min_count": 16,
                "max_count": 16
            },
            {
                "key": "enemy_1007_slime_2",
                "min_count": 11,
                "max_count": 11
            },
            {
                "key": "enemy_1101_plkght",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1074_dbskar",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_1075_dmgswd",
                "min_count": 1,
                "max_count": 1
            },
        ]
    },
    {
        "path": "ro3/level_rogue3_3-2.json",
        'id': "level_rogue3_3-2",
        "enemy_counts": [33, 34],
        "elite_enemy_counts": None,
        "sp_count": [35],
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_2043_smsbr",
                "min_count": 25,
                "max_count": 25
            },
            {
                "key": "enemy_2044_smwiz",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_1075_dmgswd",
                "min_count": 2,
                "max_count": 5
            },
            {
                "key": "enemy_1084_sotidm",
                "min_count": 0,
                "max_count": 2
            },
        ],
        "elite_enemy_list": None
    },
    {
        "path": "ro4/level_rogue4_4-10.json",
        'id': "level_rogue4_4-10",
        "enemy_counts": [42],
        "elite_enemy_counts": None,
        "sp_count": [43],
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_1076_bsthmr_2",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_1171_durokt_2",
                "min_count": 16,
                "max_count": 16
            },
            {
                "key": "enemy_2064_skzwdd",
                "min_count": 10,
                "max_count": 10
            },
            {
                "key": "enemy_1174_duholy_2",
                "min_count": 6,
                "max_count": 6
            },
            {
                "key": "enemy_1175_dushdo_2",
                "min_count": 6,
                "max_count": 6
            },
            {
                "key": "enemy_2073_skzrck",
                "min_count": 0,
                "max_count": 1
            },
        ],
        "elite_enemy_list": None
    },
    {
        "path": "ro4/level_rogue4_t-4.json",
        'id': "level_rogue4_t-4",
        "enemy_counts": [33, 34, 35],
        "elite_enemy_counts": [52],
        "sp_count": None,
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_1263_durbus",
                "min_count": 39,
                "max_count": 39
            },
            {
                "key": "enemy_2070_skzfbx",
                "min_count": 6,
                "max_count": 6
            },
            {
                "key": "enemy_2046_smwar",
                "min_count": 11,
                "max_count": 11
            },
            {
                "key": "enemy_1283_sgkill_2",
                "min_count": 0,
                "max_count": 8
            },
            {
                "key": "enemy_1311_mhkryk_2",
                "min_count": 0,
                "max_count": 7
            },
            {
                "key": "enemy_2001_duckmi",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2085_skzjxd",
                "min_count": 0,
                "max_count": 1
            },
            {
                "key": "enemy_2034_sythef",
                "min_count": 0,
                "max_count": 1
            },
            {
                "key": "enemy_1092_mdgint",
                "min_count": 0,
                "max_count": 6
            },
            {
                "key": "enemy_2002_bearmi",
                "min_count": 0,
                "max_count": 1
            }
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_1263_durbus",
                "min_count": 39,
                "max_count": 39
            },
            {
                "key": "enemy_2046_smwar",
                "min_count": 13,
                "max_count": 13
            },
            {
                "key": "enemy_1092_mdgint",
                "min_count": 7,
                "max_count": 7
            },
            {
                "key": "enemy_1283_sgkill_2",
                "min_count": 11,
                "max_count": 11
            },
            {
                "key": "enemy_1311_mhkryk_2",
                "min_count": 11,
                "max_count": 11
            },
            {
                "key": "enemy_2001_duckmi",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2085_skzjxd",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2034_sythef",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2002_bearmi",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2070_skzfbx",
                "min_count": 6,
                "max_count": 6
            }
        ]
    },
    {
        "path": "ro4/level_rogue4_b-8.json",
        'id': "level_rogue4_b-8",
        "enemy_counts": [55],
        "elite_enemy_counts": [60],
        "sp_count": None,
        "elite_sp_count": None,
        "enemy_list": [
            {
                "key": "enemy_2092_skzamy",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2094_skzamb",
                "min_count": 15,
                "max_count": 15
            },
            {
                "key": "enemy_2096_skzamj_03",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2095_skzamf_04",
                "min_count": 10,
                "max_count": 14
            },
            {
                "key": "enemy_2095_skzamf_16",
                "min_count": 19,
                "max_count": 19
            },
            {
                "key": "enemy_2095_skzamf_18",
                "min_count": 7,
                "max_count": 7
            },
            {
                "key": "enemy_2095_skzamf_19",
                "min_count": 4,
                "max_count": 8
            },
            {
                "key": "enemy_2096_skzamj_01",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_05",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_07",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_06",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2094_skzamb_2",
                "min_count": 5,
                "max_count": 5
            }
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_2092_skzamy",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2094_skzamb",
                "min_count": 15,
                "max_count": 15
            },
            {
                "key": "enemy_2096_skzamj_03",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_04",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2095_skzamf_04",
                "min_count": 7,
                "max_count": 11
            },
            {
                "key": "enemy_2095_skzamf_16",
                "min_count": 12,
                "max_count": 12
            },
            {
                "key": "enemy_2095_skzamf_18",
                "min_count": 7,
                "max_count": 7
            },
            {
                "key": "enemy_2095_skzamf_19",
                "min_count": 6,
                "max_count": 10
            },
            {
                "key": "enemy_2095_skzamf_20",
                "min_count": 4,
                "max_count": 4
            },
            {
                "key": "enemy_2096_skzamj_01",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2095_skzamf_13",
                "min_count": 2,
                "max_count": 5
            },
            {
                "key": "enemy_2095_skzamf_17",
                "min_count": 2,
                "max_count": 5
            },
            {
                "key": "enemy_2096_skzamj_02",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_05",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_07",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2096_skzamj_06",
                "min_count": 1,
                "max_count": 1
            },
            {
                "key": "enemy_2094_skzamb_2",
                "min_count": 5,
                "max_count": 5
            }
        ]
    },
    {
        "path": "ro5/level_rogue5_3-4.json",
        'id': "level_rogue5_3-4",
        "enemy_counts": [38],
        "elite_enemy_counts": [38],
        "sp_count": [39],
        "elite_sp_count": [39],
        "enemy_list": [
            {
                "key": "enemy_1173_duspfr",
                "min_count": 21,
                "max_count": 21
            },
            {
                "key": "enemy_1165_duhond",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1176_dusocr",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1166_dusbr",
                "min_count": 12,
                "max_count": 12
            }
        ],
        "elite_enemy_list": [
            {
                "key": "enemy_1173_duspfr",
                "min_count": 21,
                "max_count": 21
            },
            {
                "key": "enemy_1165_duhond",
                "min_count": 3,
                "max_count": 3
            },
            {
                "key": "enemy_1176_dusocr",
                "min_count": 2,
                "max_count": 2
            },
            {
                "key": "enemy_1166_dusbr",
                "min_count": 12,
                "max_count": 12
            }
        ]
    }
]


def convert_enemy_list(enemy_list):
    return {
        item["key"]: {
            "min": item["min_count"],
            "max": item["max_count"]
        } for item in enemy_list
    }


def test_waves():
    for case in test_cases:
        stage_data_path = os.path.join(
            script_dir,
            f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{case['path']}",
        )
        with open(stage_data_path, encoding="utf-8") as f:
            stage_data = json.load(f)
            print(case['id'])
            wave_data = get_wave_spawns_data(stage_data, case['id'], log=True)
            enemy_list, elite_enemy_list, sp_count, elite_sp_count, enemy_counts, elite_enemy_counts = itemgetter(
                "enemy_list", "elite_enemy_list", "sp_count", "elite_sp_count", "enemy_counts", "elite_enemy_counts")(wave_data)
            try:
                assert (sp_count) == case['sp_count']
                assert (elite_sp_count) == case['elite_sp_count']
                assert (enemy_counts) == case['enemy_counts']
                assert (elite_enemy_counts) == case['elite_enemy_counts']
                for enemy in enemy_list:
                    case_enemy = next(
                        (item for item in case['enemy_list'] if item['key'] == enemy['key']), None)
                    if not case_enemy:
                        assert False
                    else:
                        assert case_enemy['min_count'] == enemy['min_count']
                        assert case_enemy['max_count'] == enemy['max_count']
                if elite_enemy_list:
                    for enemy in elite_enemy_list:
                        case_enemy = next(
                            (item for item in case['elite_enemy_list'] if item['key'] == enemy['key']), None)
                        if not case_enemy:
                            assert False
                        else:
                            assert case_enemy['min_count'] == enemy['min_count']
                            assert case_enemy['max_count'] == enemy['max_count']

            except AssertionError as e:
                traceback.print_exc()
                pp.pprint(enemy_list)
