from os import walk
import pprint
import os
import json

pp = pprint.PrettyPrinter(indent=4)
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

def get_all_tiles():
    f = []
    for (dirpath, dirnames, filenames) in walk(os.path.join(script_dir, "cn_data/zh_CN/gamedata/levels/obt")):
        for filename in filenames:
            f.append(os.path.join(dirpath, filename))

    tiles = []
    for path in f:
        with open(path, encoding="utf-8") as f:
            stage_data = json.load(f)
        mapTiles = stage_data['mapData']['tiles']

        for tile in mapTiles:
            if tile['tileKey'] == 'tile_flower':
                print(path)
            if tile['tileKey'] not in tiles:
                tiles.append(tile['tileKey'])
    # pp.pprint(tiles)


ALL_TILES = ['tile_forbidden',
             'tile_start',
             'tile_wall',
             'tile_road',
             'tile_floor',
             'tile_end',
             'tile_healing',
             'tile_telout',
             'tile_telin',
             'tile_flystart',
             'tile_infection',
             'tile_hole',
             'tile_fence',
             'tile_yinyang_wall',
             'tile_yinyang_road',
             'tile_deepwater',
             'tile_smog',
             'tile_fence_bound',
             'tile_deepsea',
             'tile_wooden_wall',
             'tile_defup',
             'tile_empty',
             'tile_volspread',
             'tile_bigforce',
             'tile_rcm_crate',
             'tile_volcano',
             'tile_icetur_lb',
             'tile_icestr',
             'tile_icetur_rb',
             'tile_icetur_rt',
             'tile_icetur_lt',
             'tile_rcm_operator',
             'tile_corrosion',
             'tile_mire',
             'tile_reed',
             'tile_grass',
             'tile_creep',
             'tile_gazebo',
             'tile_defbreak',
             'tile_pollution_road',
             'tile_pollution_wall',
             'tile_creepf',
             'tile_yinyang_switch',
             'tile_stairs',
             'tile_passable_wall',
             'tile_reedw',
             'tile_reedf',
             'tile_xbdpsea',
             'tile_puddle',
             'tile_steam',
             'tile_corrosion_2',
             'tile_flowerf',
             'tile_flower']

NORMAL_TILES = ['tile_forbidden',
                'tile_start',
                'tile_wall',
                'tile_road',
                'tile_floor',
                'tile_end', 'tile_telout',
                'tile_telin',
                'tile_flystart', 'tile_fence', 'tile_fence_bound', 'tile_empty', 'tile_stairs', 'tile_passable_wall']

SP_TILES = ["tile_hole",
            "tile_deepsea",
            "tile_grass",
            "tile_infection",
            "tile_volcano",
            "tile_defbreak",
            "tile_defup",
            "tile_gazebo",
            "tile_healing",
            "tile_pollution_road",
            "tile_creep",
            "tile_bigforce"]


def get_special_tiles(tiles):
    tiles_list = []
    for tile in tiles:
        if tile['tileKey'] in SP_TILES:
            bb = {}
            if tile['blackboard'] is not None:
                for item in tile['blackboard']:
                    bb[item['key']] = item['value']
            tiles_list.append({
                "tileKey": tile['tileKey'],
                "alias": None,
                "blackboard": bb if len(bb) > 0 else None
            })
    unique_list = []
    for item in tiles_list:
        if not item in unique_list:
            unique_list.append(item)
    return unique_list
