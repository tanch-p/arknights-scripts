import json
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

cn_enemy_handbook_path = os.path.join(
    script_dir, "zh_CN/gamedata/excel/enemy_handbook_table.json"
)

with open(cn_enemy_handbook_path, encoding="utf-8") as f:
    cn_enemy_handbook = json.load(f)

enemies_to_parse = ['enemy_2056_smedzi', 'enemy_2055_smlead', 'enemy_2054_smdeer', 'enemy_2053_smgia2',
                    'enemy_2052_smgia', 'enemy_2051_smsha2', 'enemy_2050_smsha', 'enemy_2049_smgrd2',
                    'enemy_2048_smgrd', 'enemy_1303_mhshep', 'enemy_1304_mhwolf', 'enemy_1306_mhtrtl',
                    'enemy_1307_mhrhcr', 'enemy_1309_mhboar', 'enemy_1310_mhprpn', 'enemy_1299_ymkilr', 
                    'enemy_1300_ymmir', 'enemy_2043_smsbr','enemy_2044_smwiz','enemy_2045_smdrn']
data={}
for key in enemies_to_parse:
    skill_id = key.split("_")[-1]
    enemy_data = cn_enemy_handbook['enemyData'][key]
    for index, ability in enumerate(enemy_data['abilityList']):
        holder = {
            "type":"others",
            "tooltip": {
			"en": [
				ability['text']
			],
			"ja": [ability['text']],
			"zh": [ability['text']]
		}
        }
        data[f'{skill_id}_{index+1}'] = holder

with open("enemy_skills.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
