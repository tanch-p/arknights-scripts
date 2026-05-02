import json
import re
from chara_skills import insert_attack_interval, DEGREE_TIERS


def bb(base_attack_time):
    return [{"key": "base_attack_time", "value": base_attack_time}]


# --- unit tests ---

def test_inserts_zh():
    text = "攻击间隔<@ba.vdown>大幅延长</>"
    assert insert_attack_interval(text, bb(1.7)) == "攻击间隔<@ba.vdown>大幅延长(+1.7)</>"


def test_inserts_ja_with_no_particle():
    # JA variant "通常攻撃の間隔" with particle の — must also match.
    text = "通常攻撃の間隔を<@ba.vup>やや短縮</>し、続く"
    expected = "通常攻撃の間隔を<@ba.vup>やや短縮(*0.65)</>し、続く"
    assert insert_attack_interval(text, bb(0.65)) == expected


def test_integer_bat_formats_without_decimal():
    text = "Attack Interval <@ba.vdown>increases</>"
    assert insert_attack_interval(text, bb(2.0)) == "Attack Interval <@ba.vdown>increases(+2)</>"


def test_idempotent_numeric_value_already_present():
    text = "攻击间隔<@ba.vdown>大幅延长(+1.7)</>"
    assert insert_attack_interval(text, bb(1.7)) == text


def test_idempotent_percent_value_already_present():
    text = "Attack Interval <@ba.vdown>increases a bit (+50%)</>"
    assert insert_attack_interval(text, bb(0.5)) == text


def test_no_insert_when_vup_already_has_value():
    # existing value in vup block — idempotent
    text = "Attack Interval <@ba.vup>reduces (*0.6)</>"
    assert insert_attack_interval(text, bb(0.5)) == text


def test_inserts_into_vup_when_value_missing():
    # bat > 0 with vup → multiplier notation
    text = "Attack Interval <@ba.vup>reduces</>"
    assert insert_attack_interval(text, bb(0.5)) == "Attack Interval <@ba.vup>reduces(*0.5)</>"


def test_no_insert_when_no_base_attack_time_in_blackboard():
    text = "Attack Interval <@ba.vdown>greatly increases</>"
    assert insert_attack_interval(text, [{"key": "atk_scale", "value": 2.4}]) == text


def test_prefixed_key_attack_at_base_attack_time_matches():
    # attack@base_attack_time picked up via substring match; bat > 0 with vup → multiplier
    bb_prefixed = [{"key": "attack@base_attack_time", "value": 0.2}]
    text = "攻击间隔<@ba.vup>大幅度缩短</>"
    assert insert_attack_interval(text, bb_prefixed) == "攻击间隔<@ba.vup>大幅度缩短(*0.2)</>"


def test_none_text_returns_none():
    assert insert_attack_interval(None, bb(1.7)) is None


def test_no_insert_when_vdown_too_far_from_interval_keyword():
    # vdown block is for an unrelated stat — value goes into plain text, not the vdown block
    text = "Attack Interval reduces slightly, attacks deal <@ba.vdown>20</> Arts damage to self"
    expected = "Attack Interval reduces slightly (-0.5), attacks deal <@ba.vdown>20</> Arts damage to self"
    assert insert_attack_interval(text, bb(0.5)) == expected


def test_no_insert_when_interval_used_as_noun_reference():
    # 攻击间隔 appears as a noun (not as a stat change), no adjacent vdown
    text = "counterattack frequency no less than <@ba.vup>50%</> of Attack Interval"
    assert insert_attack_interval(text, bb(0.5)) == text


def test_no_insert_when_interval_keyword_after_vdown_tag():
    # vdown tag precedes the keyword — EN wording variant
    text = "<@ba.vup>Significant</> Attack Interval reduction (-60%)"
    assert insert_attack_interval(text, bb(-0.6)) == text


def test_taraxa_1():
    # Real skill: attack@base_attack_time key, vup (interval shortened), no existing value
    blackboard = [
        {"key": "attack@base_attack_time", "value": 0.2},
        {"key": "attack@heal_scale", "value": 0.6},
        {"key": "attack@fly_height", "value": 0.4},
        {"key": "attack@fly_duration", "value": 0.5},
        {"key": "attack@fly_end_duration", "value": 0.35},
    ]
    text = "立刻<ba.liftoff>起飞</>，攻击间隔<@ba.vup>大幅度缩短</>，每次随机回复攻击范围内已受伤的一名单位相当于攻击力<@ba.vup>60%</>的生命"
    expected = "立刻<ba.liftoff>起飞</>，攻击间隔<@ba.vup>大幅度缩短(*0.2)</>，每次随机回复攻击范围内已受伤的一名单位相当于攻击力<@ba.vup>60%</>的生命"
    assert insert_attack_interval(text, blackboard) == expected


def test_mortis_2_no_existing_value():
    blackboard = [{"key": "base_attack_time", "value": -0.3}]
    zh = "攻击范围扩大，攻击间隔略微缩短，每次攻击变为攻击力<@ba.vup>120%</>法术伤害的三连发，随机攻击范围内的目标，每次攻击到敌人时自身受到<@ba.vdown>20</>点法术伤害"
    ja = "攻撃範囲拡大、攻撃間隔をわずかに短縮し、攻撃が攻撃力の<@ba.vup>120%</>の術ダメージを与える3連撃になる。ランダムで攻撃範囲内にいる敵を攻撃し、攻撃が命中するたびに、自身は<@ba.vdown>20</>の術ダメージを受ける"
    en = "Attack Range expands, Attack Interval reduces slightly, attacks become triple attacks that deal <@ba.vup>120%</> of ATK as Arts damage to random targets within Attack Range; every attack deals <@ba.vdown>20</> Arts damage to self when the attack hits the enemy"
    expected_zh = "攻击范围扩大，攻击间隔略微缩短(-0.3)，每次攻击变为攻击力<@ba.vup>120%</>法术伤害的三连发，随机攻击范围内的目标，每次攻击到敌人时自身受到<@ba.vdown>20</>点法术伤害"
    expected_ja = "攻撃範囲拡大、攻撃間隔をわずかに短縮し(-0.3)、攻撃が攻撃力の<@ba.vup>120%</>の術ダメージを与える3連撃になる。ランダムで攻撃範囲内にいる敵を攻撃し、攻撃が命中するたびに、自身は<@ba.vdown>20</>の術ダメージを受ける"
    expected_en = "Attack Range expands, Attack Interval reduces slightly (-0.3), attacks become triple attacks that deal <@ba.vup>120%</> of ATK as Arts damage to random targets within Attack Range; every attack deals <@ba.vdown>20</> Arts damage to self when the attack hits the enemy"

    assert insert_attack_interval(zh, blackboard) == expected_zh
    assert insert_attack_interval(ja, blackboard) == expected_ja
    assert insert_attack_interval(en, blackboard) == expected_en


def test_does_not_affect_text_without_interval_mention():
    text = "ATK <@ba.vup>+100%</>, range <@ba.vdown>expands</>"
    assert insert_attack_interval(text, bb(1.0)) == text


def test_only_first_interval_vdown_pair_is_modified():
    # Two interval+vdown pairs; only the first should be updated
    text = (
        "Attack Interval <@ba.vdown>increases</>, "
        "then Attack Interval <@ba.vdown>increases again</>"
    )
    result = insert_attack_interval(text, bb(0.5))
    assert result.count("(+0.5)") == 1
    assert "Attack Interval <@ba.vdown>increases(+0.5)</>" in result


# --- tier-aware form selection (base_attack_time provided) ---

def test_tier_switches_to_percent_when_absolute_out_of_tier():
    # indigo_1: bat=-0.8, BAT=3.0. Absolute = -26.7% (NOT in 大幅度缩短 tier -90..-35);
    # Percent = -80% (fits tier) → function must pick percent form.
    text = "攻击间隔<@ba.vup>大幅度缩短</>"
    assert insert_attack_interval(text, bb(-0.8), 3.0) == "攻击间隔<@ba.vup>大幅度缩短(-80%)</>"


def test_tier_keeps_absolute_when_in_tier():
    # rdoc_1: bat=-0.7, BAT=1.05. Absolute = -66.7% (fits 大幅度缩短) → keep absolute.
    text = "攻击间隔<@ba.vup>大幅度缩短</>"
    assert insert_attack_interval(text, bb(-0.7), 1.05) == "攻击间隔<@ba.vup>大幅度缩短(-0.7)</>"


def test_tier_keeps_multiplier_when_in_tier():
    # indigo_2: bat=0.6 (vup, >0 → multiplier *0.6 = -40%). Fits 缩短 tier → keep multiplier.
    text = "攻击间隔<@ba.vup>缩短</>"
    assert insert_attack_interval(text, bb(0.6), 3.0) == "攻击间隔<@ba.vup>缩短(*0.6)</>"


def test_tier_keeps_absolute_for_vdown_slight():
    # glaze_2: bat=+0.9, BAT=2.7. Absolute = +33.3% (fits 略微增大 20..55) → keep absolute.
    text = "攻击间隔<@ba.vdown>略微增大</>"
    assert insert_attack_interval(text, bb(0.9), 2.7) == "攻击间隔<@ba.vdown>略微增大(+0.9)</>"


def test_tier_switches_vdown_to_percent():
    # Hypothetical: bat=+0.5, BAT=5.0. Absolute = +10% (NOT in 增大 tier 15..230).
    # Percent = +50% (fits) → switch to percent.
    text = "攻击间隔<@ba.vdown>增大</>"
    assert insert_attack_interval(text, bb(0.5), 5.0) == "攻击间隔<@ba.vdown>增大(+50%)</>"


def test_tier_without_bat_uses_default_form():
    # No base_attack_time → falls back to original heuristic.
    text = "攻击间隔<@ba.vup>大幅度缩短</>"
    assert insert_attack_interval(text, bb(-0.8)) == "攻击间隔<@ba.vup>大幅度缩短(-0.8)</>"


def test_tier_without_degree_keyword_uses_default_form():
    # No recognized degree keyword in context → keep default even with BAT supplied.
    text = "攻击间隔<@ba.vup>变化</>"
    assert insert_attack_interval(text, bb(-0.8), 3.0) == "攻击间隔<@ba.vup>变化(-0.8)</>"


def test_tier_table_contains_expected_keywords():
    # Guard: the exported tier table is the source of truth for tier matching.
    for kw in ["超大幅度缩短", "大幅度缩短", "缩短", "略微缩短", "略微增大", "增大"]:
        assert kw in DEGREE_TIERS, f"missing tier keyword: {kw}"
        lo, hi = DEGREE_TIERS[kw]
        assert lo < hi, f"tier range for {kw} is not ordered: ({lo}, {hi})"


# --- integration test against chara_skills.json ---

def test_all_skills_in_chara_skills_json():
    combined = re.compile(
        r"(攻击间隔|攻撃間隔|[Aa]ttack\s+[Ii]nterval)(.{0,20}?)<@ba\.vdown>(.*?)</>",
        re.DOTALL,
    )
    pat_value = re.compile(r"\([+-][^)]+\)")

    with open("chara_skills.json", encoding="utf-8") as f:
        data = json.load(f)

    for sid, skill in data.items():
        last = skill["levels"][-1]
        blackboard = last.get("blackboard", [])
        bat = next((x["value"] for x in blackboard if x["key"] == "base_attack_time"), None)
        if bat is None:
            continue
        val_str = f"+{bat}" if (isinstance(bat, float) and str(bat)[-1] != "0") else f"+{round(bat)}"

        for lang in ["description_zh", "description_ja", "description_en"]:
            text = last.get(lang, "")
            if not text:
                continue
            result = insert_attack_interval(text, blackboard)

            for m in combined.finditer(text):
                content = m.group(3)
                if pat_value.search(content):
                    # already had a value — result must be idempotent
                    assert insert_attack_interval(result, blackboard) == result, (
                        f"{sid} [{lang}]: not idempotent"
                    )
                else:
                    # missing value — must be inserted
                    assert val_str in result, (
                        f"{sid} [{lang}]: expected '{val_str}' to be inserted\n"
                        f"  original: {text[:200]}\n"
                        f"  result:   {result[:200]}"
                    )


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
