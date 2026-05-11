import pprint
import json
from pathlib import Path
from walk import get_all_file_paths

pp = pprint.PrettyPrinter(indent=4)

BASE_DIR = Path(__file__).resolve().parent
ROGUELIKE_TOPIC_TABLE_PATH = (
    BASE_DIR / "cn_data/zh_CN/gamedata/excel/roguelike_topic_table.json"
)


def iter_roguelike_topic_stages(
    topic_table_path=ROGUELIKE_TOPIC_TABLE_PATH,
    topic_ids=None,
):
    with Path(topic_table_path).open(encoding="utf-8") as f:
        roguelike_topic_table = json.load(f)

    details = roguelike_topic_table["details"]
    topics_to_iterate = topic_ids or details.keys()

    for topic_id in topics_to_iterate:
        topic_detail = details.get(topic_id, {})
        stages = topic_detail.get("stages", {})
        for stage_id, stage_info in stages.items():
            vutresProb = stage_info.get("vutresProb", None)
            if len(vutresProb) > 0:
                print(stage_id, vutresProb)


def runes_check(stage_data):
    if stage_data["runes"]:
        for rune in stage_data["runes"]:
            if rune["key"] == "level_predefine_tokens_random_spawn_on_tile":
                keys = [item["key"] for item in rune["blackboard"]]
                if "tile" not in keys:
                    print(levelId)
            # if rune['difficultyMask'] not in ['FOUR_STAR','NORMAL',"ALL"]:
            #     print(rune['difficultyMask'])
            #     print(levelId)
            # key = rune['key']
            # if not key in parsed_rune_keys:
            #     print(levelId)
            #     print(key)

            # # if('add' in key):
            # if key == 'enemy_dynamic_ability_new':
            #     print(levelId)
            #     print(key)


def waves_check(stage_data, levelId):
    for wave_index, wave in enumerate(stage_data["waves"]):
        for frag_index, fragment in enumerate(wave["fragments"]):
            pack_key_dict = {}
            for action in fragment["actions"]:
                group_key = action.get("randomSpawnGroupKey")
                pack_key = action.get("randomSpawnGroupPackKey")
                if pack_key is not None and group_key is not None:
                    if pack_key not in pack_key_dict:
                        pack_key_dict[pack_key] = []
                    pack_key_dict[pack_key].append(group_key)
            for pack_key in pack_key_dict:
                if len(pack_key_dict[pack_key]) > 1:
                    print(f"{levelId} w{wave_index}f{frag_index} more than 1 packKey")


folders = ["ro1", "ro2", "ro3", "ro4", "ro5"]
parsed_rune_keys = [
    "enemy_attribute_mul",
    "ebuff_attribute",
    "enemy_attribute_add",
    "char_attribute_mul",
    "char_attribute_add",
    "enemy_skill_blackb_add",
    "enemy_skill_blackb_mul",
    "enemy_dynamic_ability_new",
    "level_hidden_group_enable",
    "level_hidden_group_disable",
    "level_enemy_replace",
    "level_predefines_enable",
    "global_forbid_location",
    "env_gbuff_new",
    "env_system_new",
    "enemy_talent_blackb_mul",
    "enemy_talent_blackb_add",
    "level_predefines_skill_replace",
    "enemy_attackradius_mul",
    "map_tile_blackb_mul",
    "global_cost_recovery_mul",
    "default_key",
    "char_respawntime_mul",
    "char_skill_cd_add",
    "enemy_skill_cd_mul",
    "enemy_skill_init_cd_mul",
    "cbuff_max_cost",
    "char_skill_cd_mul",
    "global_lifepoint",
    "char_skill_blackb_mul",
]


def main():
    iter_roguelike_topic_stages()
    # for folder in folders:
    #     path = BASE_DIR / f"cn_data/zh_CN/gamedata/levels/obt/roguelike/{folder}"
    #     file_paths = get_all_file_paths(str(path))
    #     for file_path in file_paths:
    #         with Path(file_path).open(encoding="utf-8") as f:
    #             stage_data = json.load(f)
    #         levelId = Path(file_path).name

    #         # waves_check(stage_data, levelId)
    #         if "rogue5" not in levelId:
    #             continue
    #         # for enemy in stage_data['enemyDbRefs']:
    #         #     if enemy['useDb'] is False:
    #         #         print(levelId,enemy['id'])


if __name__ == "__main__":
    main()
