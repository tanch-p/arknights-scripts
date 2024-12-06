def get_sub_profession_tags(char, id):
    tags = []
    if char['subProfessionId'] == "stalker":
        tags.append("lower_target_priority")
    if char['subProfessionId'] == "loopshooter":
        tags.append("aspd_unrelated")
    if char['subProfessionId'] == "fastshot":
        tags.append("priority_flying")
    if char['subProfessionId'] == "longrange":
        tags.append("priority_def_low")
    if char['subProfessionId'] == "siegesniper":
        tags.append("priority_highest_weight")
    if char['subProfessionId'] == "bard":
        tags.append("heal_unhealable")
    if char['subProfessionId'] in ["executor", "merchant", "agent"] and id != "char_376_therex":
        tags.append("fast_redeploy")
    if char['subProfessionId'] in ["pusher", "hookmaster"]:
        tags.append("position_all")
    if char['subProfessionId'] in ["unyield", "musha"]:
        tags.append("no_healing")
    if char['subProfessionId'] in ["reaper", "guardian","bard"]:
        tags.append("heal_self")
    if char['subProfessionId'] in ["skywalker"]:
        tags.append("block_flying")
    if char['subProfessionId'] in ["guardian","bard"]:
        tags.append("heal_ally")
    if char['subProfessionId'] in ["splashcaster",'blastcaster', "stalker", "hammer", "reaper", "aoesniper", "reaperrange", "bombarder", "phalanx"]:
        tags.append("aoe")
    if char['subProfessionId'] in ["instructor"]:
        tags.extend(["no_block_enemy","bonus_no_block_enemy","self_no_block_enemy"]) 
    if char['subProfessionId'] in ["tactician", "agent", "lord",
                                   "fastshot", "closerange", "aoesniper", "longrange", "reaperrange", "siegesniper", "loopshooter", "hunter"
                                   "shotprotector", "incantationmedic", "slower", "summoner", "underminer", "blessing", "ritualist", "corecaster",
                                   "splashcaster", "blastcaster", "funnel", "phalanx", "mystic", "chain", "primcaster", "hookmaster", "geek", "traper","alchemist","skywalker"]:
        tags.append("target_air")
    if char['subProfessionId'] in ["charger", "pioneer", "bearer", "tactician", "agent",
                                   "sword", "fearless", "lord", "centurion", "reaper", "instructor", "fighter", "musha", "librator", "crusher", "hammer"
                                   "fastshot", "closerange", "aoesniper", "longrange", "reaperrange", "siegesniper", "bombarder", "loopshooter", "hunter"
                                   "protector", "guardian", "shotprotector", "artsprotector", "duelist", "fortress", "unyield"
                                   "craftsman", "executor", "stalker", "pusher", "hookmaster", "merchant", "geek", "dollkeeper", "traper","alchemist","skywalker","primprotector"]:
        tags.append("phys")
    if char['subProfessionId'] in ["artsfghter", "artsprotector", "incantationmedic",
                                   "slower", "summoner", "underminer", "blessing", "ritualist",
                                   "corecaster", "splashcaster", "blastcaster", "funnel", "phalanx", "mystic", "chain", "primcaster","soulcaster"]:
        tags.append("arts")
    return tags
