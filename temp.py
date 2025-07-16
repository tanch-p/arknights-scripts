from os import walk
import pprint
import os
import json

pp = pprint.PrettyPrinter(indent=4)

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
# cn_char_table_path = os.path.join(
#     script_dir, "cn_data/zh_CN/gamedata/excel/character_table.json")
# with open(cn_char_table_path, encoding='utf-8') as f:
#     char_table = json.load(f)

# list = []
# for id in char_table:
#     chara_dict = char_table[id]
#     for pot in chara_dict['potentialRanks']:
#         if pot['buff']:
#             for item in pot['buff']['attributes']['attributeModifiers']:
#                 if not item['attributeType'] in list:
#                     list.append(item['attributeType'])

# print(list)
# return_dict = [ele for ele in list]

# with open('temp.json','w', encoding='utf-8') as f:
#     json.dump(return_dict, f, ensure_ascii=False, indent=4)

# enemy_database_path = os.path.join(
#     script_dir, "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
# )
# with open(enemy_database_path, encoding="utf-8") as f:
#     enemy_database = json.load(f)

# for enemy in enemy_database['enemies']:
#     key = enemy['Key']
#     for stats in enemy['Value']:
#         if stats['enemyData']['attributes']['epDamageResistance']['m_value'] != 0 or stats['enemyData']['attributes']['epResistance']['m_value'] != 0:
#             print(key)

# with open('chara_talents.json', encoding='utf-8') as f:
#     chara_talents = json.load(f)

# return_dict = {}
# for id in chara_talents:
#     talents = []
#     for talent_index, talent in enumerate(chara_talents[id]['talents']):
#         talent_holder = {
#             "prefabKey": talent["prefabKey"], "name_zh": talent["name_zh"], "name_ja": talent['name_ja'], "name_en": talent['name_en'],
#             "desc_zh": talent["description_zh"], "desc_ja":  talent['description_ja'], "desc_en": talent['description_en'], "target_air": None, "tags": talent['tags'] , "blackboard": talent['blackboard']}
#         talents.append(talent_holder)
#     return_dict[id] = {
#         "appellation": chara_talents[id]['appellation'], "talents": talents}

# with open('chara_talents.json', 'w', encoding='utf-8') as f:
#     json.dump(return_dict, f, ensure_ascii=False, indent=4)

# handpicked 50 characters for testing
testing_chars = ['char_4116_blkkgt', 'char_003_kalts', 'char_4048_doroth', '']

list1 = [
    {
        "id": "enemy_1112_emppnt_2",
        "prefabKey": "enemy_1112_emppnt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1185_nmekgt_3",
        "prefabKey": "enemy_1185_nmekgt_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1293_duswrd_3",
        "prefabKey": "enemy_1293_duswrd_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1332_cbterm_2",
        "prefabKey": "enemy_1332_cbterm_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1333_cbbgen_2",
        "prefabKey": "enemy_1333_cbbgen_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1284_sgprst",
        "prefabKey": "enemy_1284_sgprst",
        "level": 1,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1415_mmkabi",
        "prefabKey": "enemy_1415_mmkabi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2002_bearmi",
        "prefabKey": "enemy_2002_bearmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2005_axetro",
        "prefabKey": "enemy_2005_axetro",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2006_flsnip",
        "prefabKey": "enemy_2006_flsnip",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2011_csppt",
        "prefabKey": "enemy_2011_csppt",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2013_csbot",
        "prefabKey": "enemy_2013_csbot",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2014_csicer",
        "prefabKey": "enemy_2014_csicer",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2015_csicem",
        "prefabKey": "enemy_2015_csicem",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10020_sgcat",
        "prefabKey": "enemy_10020_sgcat",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1397_dhtsxt_2",
        "prefabKey": "enemy_1397_dhtsxt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10026_vtzepl",
        "prefabKey": "enemy_10026_vtzepl",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1342_frtuna",
        "prefabKey": "enemy_1342_frtuna",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1426_lrthef_2",
        "prefabKey": "enemy_1426_lrthef_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1430_lrrook",
        "prefabKey": "enemy_1430_lrrook",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1347_fyshp_2",
        "prefabKey": "enemy_1347_fyshp_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1005_yokai_3",
        "prefabKey": "enemy_1005_yokai_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1321_wdarft_2",
        "prefabKey": "enemy_1321_wdarft_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2001_duckmi",
        "prefabKey": "enemy_2001_duckmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1041_lazerd_2",
        "prefabKey": "enemy_1041_lazerd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1042_frostd",
        "prefabKey": "enemy_1042_frostd",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1329_cbshld",
        "prefabKey": "enemy_1329_cbshld",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1363_spnshd",
        "prefabKey": "enemy_1363_spnshd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1405_boomer",
        "prefabKey": "enemy_1405_boomer",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1269_nhfly_2",
        "prefabKey": "enemy_1269_nhfly_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10027_vtsk",
        "prefabKey": "enemy_10027_vtsk",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1255_lybgpa_2",
        "prefabKey": "enemy_1255_lybgpa_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1273_stmgun_2",
        "prefabKey": "enemy_1273_stmgun_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1199_sfjin",
        "prefabKey": "enemy_1199_sfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1201_sfzhi",
        "prefabKey": "enemy_1201_sfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1207_sfji_2",
        "prefabKey": "enemy_1207_sfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1209_sfden_2",
        "prefabKey": "enemy_1209_sfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2101_dyspll",
        "prefabKey": "enemy_2101_dyspll",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2121_dyspl2",
        "prefabKey": "enemy_2121_dyspl2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1200_msfjin",
        "prefabKey": "enemy_1200_msfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1202_msfzhi",
        "prefabKey": "enemy_1202_msfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1208_msfji_2",
        "prefabKey": "enemy_1208_msfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1210_msfden_2",
        "prefabKey": "enemy_1210_msfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1345_tplamb_2",
        "prefabKey": "enemy_1345_tplamb_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1367_dseed",
        "prefabKey": "enemy_1367_dseed",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10028_vtswd",
        "prefabKey": "enemy_10028_vtswd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10029_vtshld",
        "prefabKey": "enemy_10029_vtshld",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10030_vtwand",
        "prefabKey": "enemy_10030_vtwand",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10090_hlgrd_2",
        "prefabKey": "enemy_10090_hlgrd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10088_hlsnip_2",
        "prefabKey": "enemy_10088_hlsnip_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10078_mprein_2",
        "prefabKey": "enemy_10078_mprein_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10073_mpcar_2",
        "prefabKey": "enemy_10073_mpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10067_ftsjc_2",
        "prefabKey": "enemy_10067_ftsjc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10066_ftxjl_2",
        "prefabKey": "enemy_10066_ftxjl_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10059_cjgfod",
        "prefabKey": "enemy_10059_cjgfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10060_cjbfod",
        "prefabKey": "enemy_10060_cjbfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10058_cjfrog_2",
        "prefabKey": "enemy_10058_cjfrog_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10054_cjhot_2",
        "prefabKey": "enemy_10054_cjhot_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10049_pcaptn_2",
        "prefabKey": "enemy_10049_pcaptn_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10043_sailor_2",
        "prefabKey": "enemy_10043_sailor_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10048_prtsld_2",
        "prefabKey": "enemy_10048_prtsld_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10036_cnvpvd_2",
        "prefabKey": "enemy_10036_cnvpvd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10037_cnvpcar_2",
        "prefabKey": "enemy_10037_cnvpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10039_cnvber_2",
        "prefabKey": "enemy_10039_cnvber_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10034_cnvsax_2",
        "prefabKey": "enemy_10034_cnvsax_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10035_cnvdnc_2",
        "prefabKey": "enemy_10035_cnvdnc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10019_sgmum_2",
        "prefabKey": "enemy_10019_sgmum_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2104_dycast",
        "prefabKey": "enemy_2104_dycast",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2105_dyrnge",
        "prefabKey": "enemy_2105_dyrnge",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2103_dykens",
        "prefabKey": "enemy_2103_dykens",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2102_dytmbr",
        "prefabKey": "enemy_2102_dytmbr",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    }
]
list3 = [
    {
        "id": "enemy_1112_emppnt_2",
        "prefabKey": "enemy_1112_emppnt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1185_nmekgt_3",
        "prefabKey": "enemy_1185_nmekgt_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1293_duswrd_3",
        "prefabKey": "enemy_1293_duswrd_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1332_cbterm_2",
        "prefabKey": "enemy_1332_cbterm_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1333_cbbgen_2",
        "prefabKey": "enemy_1333_cbbgen_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1284_sgprst",
        "prefabKey": "enemy_1284_sgprst",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1415_mmkabi",
        "prefabKey": "enemy_1415_mmkabi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2002_bearmi",
        "prefabKey": "enemy_2002_bearmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2005_axetro",
        "prefabKey": "enemy_2005_axetro",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2006_flsnip",
        "prefabKey": "enemy_2006_flsnip",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2011_csppt",
        "prefabKey": "enemy_2011_csppt",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2013_csbot",
        "prefabKey": "enemy_2013_csbot",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2014_csicer",
        "prefabKey": "enemy_2014_csicer",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2015_csicem",
        "prefabKey": "enemy_2015_csicem",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10020_sgcat",
        "prefabKey": "enemy_10020_sgcat",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_10026_vtzepl",
        "prefabKey": "enemy_10026_vtzepl",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1342_frtuna",
        "prefabKey": "enemy_1342_frtuna",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1397_dhtsxt_2",
        "prefabKey": "enemy_1397_dhtsxt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1426_lrthef_2",
        "prefabKey": "enemy_1426_lrthef_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1430_lrrook",
        "prefabKey": "enemy_1430_lrrook",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1347_fyshp_2",
        "prefabKey": "enemy_1347_fyshp_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1005_yokai_3",
        "prefabKey": "enemy_1005_yokai_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1321_wdarft_2",
        "prefabKey": "enemy_1321_wdarft_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2001_duckmi",
        "prefabKey": "enemy_2001_duckmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1041_lazerd_2",
        "prefabKey": "enemy_1041_lazerd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1042_frostd",
        "prefabKey": "enemy_1042_frostd",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1329_cbshld",
        "prefabKey": "enemy_1329_cbshld",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1363_spnshd",
        "prefabKey": "enemy_1363_spnshd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1405_boomer",
        "prefabKey": "enemy_1405_boomer",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1269_nhfly_2",
        "prefabKey": "enemy_1269_nhfly_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10027_vtsk",
        "prefabKey": "enemy_10027_vtsk",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1255_lybgpa_2",
        "prefabKey": "enemy_1255_lybgpa_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1273_stmgun_2",
        "prefabKey": "enemy_1273_stmgun_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1199_sfjin",
        "prefabKey": "enemy_1199_sfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1201_sfzhi",
        "prefabKey": "enemy_1201_sfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1207_sfji_2",
        "prefabKey": "enemy_1207_sfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1209_sfden_2",
        "prefabKey": "enemy_1209_sfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2101_dyspll",
        "prefabKey": "enemy_2101_dyspll",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2121_dyspl2",
        "prefabKey": "enemy_2121_dyspl2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1200_msfjin",
        "prefabKey": "enemy_1200_msfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1202_msfzhi",
        "prefabKey": "enemy_1202_msfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1208_msfji_2",
        "prefabKey": "enemy_1208_msfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1210_msfden_2",
        "prefabKey": "enemy_1210_msfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1345_tplamb_2",
        "prefabKey": "enemy_1345_tplamb_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1367_dseed",
        "prefabKey": "enemy_1367_dseed",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10028_vtswd",
        "prefabKey": "enemy_10028_vtswd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10029_vtshld",
        "prefabKey": "enemy_10029_vtshld",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10030_vtwand",
        "prefabKey": "enemy_10030_vtwand",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10090_hlgrd_2",
        "prefabKey": "enemy_10090_hlgrd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10088_hlsnip_2",
        "prefabKey": "enemy_10088_hlsnip_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10078_mprein_2",
        "prefabKey": "enemy_10078_mprein_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10073_mpcar_2",
        "prefabKey": "enemy_10073_mpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10067_ftsjc_2",
        "prefabKey": "enemy_10067_ftsjc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10066_ftxjl_2",
        "prefabKey": "enemy_10066_ftxjl_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10059_cjgfod",
        "prefabKey": "enemy_10059_cjgfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10060_cjbfod",
        "prefabKey": "enemy_10060_cjbfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10058_cjfrog_2",
        "prefabKey": "enemy_10058_cjfrog_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10054_cjhot_2",
        "prefabKey": "enemy_10054_cjhot_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10049_pcaptn_2",
        "prefabKey": "enemy_10049_pcaptn_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10043_sailor_2",
        "prefabKey": "enemy_10043_sailor_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10048_prtsld_2",
        "prefabKey": "enemy_10048_prtsld_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10036_cnvpvd_2",
        "prefabKey": "enemy_10036_cnvpvd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10037_cnvpcar_2",
        "prefabKey": "enemy_10037_cnvpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10039_cnvber_2",
        "prefabKey": "enemy_10039_cnvber_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10034_cnvsax_2",
        "prefabKey": "enemy_10034_cnvsax_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10035_cnvdnc_2",
        "prefabKey": "enemy_10035_cnvdnc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10019_sgmum_2",
        "prefabKey": "enemy_10019_sgmum_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2104_dycast",
        "prefabKey": "enemy_2104_dycast",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2105_dyrnge",
        "prefabKey": "enemy_2105_dyrnge",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2103_dykens",
        "prefabKey": "enemy_2103_dykens",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2102_dytmbr",
        "prefabKey": "enemy_2102_dytmbr",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    }
]
list2 = [
    {
        "id": "enemy_1112_emppnt_2",
        "prefabKey": "enemy_1112_emppnt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1185_nmekgt_3",
        "prefabKey": "enemy_1185_nmekgt_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1293_duswrd_3",
        "prefabKey": "enemy_1293_duswrd_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1332_cbterm_2",
        "prefabKey": "enemy_1332_cbterm_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1333_cbbgen_2",
        "prefabKey": "enemy_1333_cbbgen_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1284_sgprst",
        "prefabKey": "enemy_1284_sgprst",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_1415_mmkabi",
        "prefabKey": "enemy_1415_mmkabi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2002_bearmi",
        "prefabKey": "enemy_2002_bearmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2005_axetro",
        "prefabKey": "enemy_2005_axetro",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2006_flsnip",
        "prefabKey": "enemy_2006_flsnip",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2011_csppt",
        "prefabKey": "enemy_2011_csppt",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2013_csbot",
        "prefabKey": "enemy_2013_csbot",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2014_csicer",
        "prefabKey": "enemy_2014_csicer",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2015_csicem",
        "prefabKey": "enemy_2015_csicem",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10020_sgcat",
        "prefabKey": "enemy_10020_sgcat",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 60000
        }
    },
    {
        "id": "enemy_10026_vtzepl",
        "prefabKey": "enemy_10026_vtzepl",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1342_frtuna",
        "prefabKey": "enemy_1342_frtuna",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1397_dhtsxt_2",
        "prefabKey": "enemy_1397_dhtsxt_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1426_lrthef_2",
        "prefabKey": "enemy_1426_lrthef_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1430_lrrook",
        "prefabKey": "enemy_1430_lrrook",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1347_fyshp_2",
        "prefabKey": "enemy_1347_fyshp_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1005_yokai_3",
        "prefabKey": "enemy_1005_yokai_3",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1321_wdarft_2",
        "prefabKey": "enemy_1321_wdarft_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_2001_duckmi",
        "prefabKey": "enemy_2001_duckmi",
        "level": 2,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1041_lazerd_2",
        "prefabKey": "enemy_1041_lazerd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1042_frostd",
        "prefabKey": "enemy_1042_frostd",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1329_cbshld",
        "prefabKey": "enemy_1329_cbshld",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1363_spnshd",
        "prefabKey": "enemy_1363_spnshd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1405_boomer",
        "prefabKey": "enemy_1405_boomer",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_1269_nhfly_2",
        "prefabKey": "enemy_1269_nhfly_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10027_vtsk",
        "prefabKey": "enemy_10027_vtsk",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1255_lybgpa_2",
        "prefabKey": "enemy_1255_lybgpa_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1273_stmgun_2",
        "prefabKey": "enemy_1273_stmgun_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1199_sfjin",
        "prefabKey": "enemy_1199_sfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1201_sfzhi",
        "prefabKey": "enemy_1201_sfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1207_sfji_2",
        "prefabKey": "enemy_1207_sfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1209_sfden_2",
        "prefabKey": "enemy_1209_sfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2101_dyspll",
        "prefabKey": "enemy_2101_dyspll",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2121_dyspl2",
        "prefabKey": "enemy_2121_dyspl2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1200_msfjin",
        "prefabKey": "enemy_1200_msfjin",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1202_msfzhi",
        "prefabKey": "enemy_1202_msfzhi",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1208_msfji_2",
        "prefabKey": "enemy_1208_msfji_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1210_msfden_2",
        "prefabKey": "enemy_1210_msfden_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_1345_tplamb_2",
        "prefabKey": "enemy_1345_tplamb_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_1367_dseed",
        "prefabKey": "enemy_1367_dseed",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10028_vtswd",
        "prefabKey": "enemy_10028_vtswd",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10029_vtshld",
        "prefabKey": "enemy_10029_vtshld",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10030_vtwand",
        "prefabKey": "enemy_10030_vtwand",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10090_hlgrd_2",
        "prefabKey": "enemy_10090_hlgrd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10088_hlsnip_2",
        "prefabKey": "enemy_10088_hlsnip_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10078_mprein_2",
        "prefabKey": "enemy_10078_mprein_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10073_mpcar_2",
        "prefabKey": "enemy_10073_mpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10067_ftsjc_2",
        "prefabKey": "enemy_10067_ftsjc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10066_ftxjl_2",
        "prefabKey": "enemy_10066_ftxjl_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10059_cjgfod",
        "prefabKey": "enemy_10059_cjgfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10060_cjbfod",
        "prefabKey": "enemy_10060_cjbfod",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10058_cjfrog_2",
        "prefabKey": "enemy_10058_cjfrog_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10054_cjhot_2",
        "prefabKey": "enemy_10054_cjhot_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": {
            "hp": 40000
        }
    },
    {
        "id": "enemy_10049_pcaptn_2",
        "prefabKey": "enemy_10049_pcaptn_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10043_sailor_2",
        "prefabKey": "enemy_10043_sailor_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10048_prtsld_2",
        "prefabKey": "enemy_10048_prtsld_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10036_cnvpvd_2",
        "prefabKey": "enemy_10036_cnvpvd_2",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    },
    {
        "id": "enemy_10037_cnvpcar_2",
        "prefabKey": "enemy_10037_cnvpcar_2",
        "level": 0,
        "min_count": 0,
        "max_count": 0,
        "elite_min_count": 0,
        "elite_max_count": 0,
        "overwrittenData": None
    },
    {
        "id": "enemy_10039_cnvber_2",
        "prefabKey": "enemy_10039_cnvber_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10034_cnvsax_2",
        "prefabKey": "enemy_10034_cnvsax_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10035_cnvdnc_2",
        "prefabKey": "enemy_10035_cnvdnc_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_10019_sgmum_2",
        "prefabKey": "enemy_10019_sgmum_2",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2104_dycast",
        "prefabKey": "enemy_2104_dycast",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2105_dyrnge",
        "prefabKey": "enemy_2105_dyrnge",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2103_dykens",
        "prefabKey": "enemy_2103_dykens",
        "level": 0,
        "min_count": 0,
        "max_count": 3,
        "elite_min_count": 0,
        "elite_max_count": 3,
        "overwrittenData": None
    },
    {
        "id": "enemy_2102_dytmbr",
        "prefabKey": "enemy_2102_dytmbr",
        "level": 0,
        "min_count": 0,
        "max_count": 6,
        "elite_min_count": 0,
        "elite_max_count": 6,
        "overwrittenData": None
    }
]

diff1 = [item for item in list1 if item not in list2]
print(diff1)