for ailment debuffs - value = duration
for buffs/other debuffs like fragile - value = value, duration = duration
all values are to be set as highest values inclusive of module effects: for example, manticores S1M3 50% slow, + module = 60% slow

### tags - for values that don't need comparison ###
cancel_stealth, has_token, burst, target_air
stop_attack
reflect_dmg
block_phys (拉普兰德)
taunt
taunt_level_down
def_penetrate
range_up
heal_ally
phys_evasion
self_heal
no_healing - cannot be healed by allies
unlimited_duration
infinite_range_straight
global_range
follow_target
limited_use - skill with limited usage times
multi_target
undying
target_hp
aoe
ally_sp
anti_invisible
skill_time_invincible
stealth
remove_status
teleport_enemy
status_immune
starting_cost
ele_heal
heal_scale - nearl
change_direction - jessica alter
respawn_time - silverash
remaining_spawn_time - gravel
token_deploy_free
deploy_all - doberman/ela
ally_sp_gain - saria
ally_sp_regen - suzuran
抵挡 - nullify_damage
protect - protect (because of same name take highest value issue)
ignore_evasion
def_scale_dmg - ceobe
fast_redeploy
damage_taken_scale - for increased damage taken
activate_skill - 烈夏
share_dmg - skadi

### blackboard keys - for values that need comparison  ###
---stat releated---
reduce_move_speed -> move_speed_down, reduce_attack_speed -> aspd_down
,
self_magic_resistance
ep_damage_resistance
ally_cost
damage_scale - sesa

heal_scale,
token_deploy_free,


---ailments---
self_stun, ally_stun
stun, sleep, tremble

---buffs---
peak_performance, damage_scale, damage_resistance


### conditions ###
hp_above_50
token_hp_below_50
not_blocked|blocked
melee
ranged
various professions
various groups
melee_attack - indra
ranged_attack - fuze
first_deploy - ash
shield_break - archetto
first_hit
dmg_below_200 - lin
when_attacked - lin
skill_atk_def_recovery


### change of keys ###
not_combat -> tremble
magic_resistance -> res
anti_invisible -> cancel_stealth
damage_scale -> fragile
damage_scale -> magicfragile


### keys untouched ###
damage_scale - additional arts dmg...
fake_damage - increase dmg taken

### chars to settle ###
enforcer skchr_forcer_2
cqbw_equip_1_3_p2

### changes from original data ###
added camouflage key to kafka skills

### quirky behaviour in chara_skills string replace ###
1. ABILITY_RANGE_FORWARD_EXTEND... (example: catapult,shirayuki)
2. negative values % have 2 minus (example: haze)
3. 攻击间隔 (example: 深靛)
4. skchr_peacok_1
5. skchr_frncat_1
6. skchr_aurora_2
7. skchr_slbell_1



conditions to add
ranged_attack
highest_max_hp
hp_above_70
hp_above_50
hp_under_40
hp_under_30
bunker_defense
skill_1
skill_2
weight_gte_3
shield_usage
first_deploy
first_hit
four_tile_enemy_defeat
dmg_below_200
condition_laoli
weight_under_3 (char_474_glady)
heal
ally_behind
token_attacked (jessica)
skill_atk_def_recovery
croc_duel
enemy_3_around (mlynar)
skill_active
collision_wall (enforcer)
next_hit
own_barrier (judge)
no_ally_8tiles

keys not in list
ele_heal
ranged (Firewatch)
def_scale_dmg (ceobe)
add_sp_gain_option (blemishine)
change_direction (jessica)
range_scale (catapult)

SCHEMA
{
            "key": "stun",
            "targets": 99,
            "value": 3.5,
            "prob": 0.2,
            "conditions": ["defeat"],
            "target_air": true
          }