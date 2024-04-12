for ailment debuffs - value = duration
for buffs/other debuffs like fragile - value = value, duration = duration
all values are to be set as highest values inclusive of module effects: for example, manticores S1M3 50% slow, + module = 60% slow

### tags - for values that don't need comparison ###
cancel_stealth, has_token, burst, target_air



### blackboard keys - for values that need comparison  ###
---stat releated---
reduce_move_speed, reduce_attack_speed
ally_res_up,

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


### change of keys ###
not_combat -> tremble



### keys untouched ###
damage_scale - additional arts dmg...
fake_damage - increase dmg taken

### chars to settle ###
enforcer skchr_forcer_2


### changes from original data ###
added camouflage key to kafka skills