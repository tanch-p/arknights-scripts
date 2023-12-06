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
            "tile_creep"]


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