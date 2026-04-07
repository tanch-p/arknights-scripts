# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Data extraction and processing toolkit that transforms raw Arknights game data (CN and Global servers) into structured JSON for downstream consumers (tools, simulators).

## Tech Stack

- **Language:** Python 3.12+
- **Package manager:** `uv`
- **Dependencies:** Standard library only (`json`, `os`, `re`, `itertools`, `collections`)

## External Data Sources

- **CN data:** `cn_data/` — sourced from [Kengxxiao/ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData)
- **Global data:** `global_data/` — sourced from [ArknightsAssets/ArknightsGamedata](https://github.com/ArknightsAssets/ArknightsGamedata)

These directories are populated manually by pulling from upstream repos. Scripts read from them but never write to them.

## Key Scripts

| Script | Output | Purpose |
|---|---|---|
| `chara.py` | `characters.json` | Aggregates character stats, skills, talents, modules |
| `chara_skills.py` | `chara_skills.json` | Skill text with blackboard values interpolated |
| `split_chara_json.py` | `characters_en/ja/zh.json` | Splits multilingual character data by language |
| `enemy.py` | `enemy_database.json` | Enemy stats, type flags, status immunities |
| `stages.py` | `is_stages_list.json`, etc. | Stage wave/spawn/terrain data |
| `waves_new.py` | — | Wave spawn analysis and probability calculations |
| `tiles.py` | — | Map tile extraction and special tile handling |
| `get_ro_topic_data.py` | `ro1-5.json` | Roguelike stage data per topic |
| `crisis.py` | `crisis_runes.json` | CC/Crisis stage rune effects |
| `runes.py` | — | Roguelike rune effect descriptions |
| `uniequip.py` | `uniequip.json` | Module equipment stats and effects |
| `tokens.py` | `tokens.json` | Deployed token/summon statistics |
| `update_stage_extrainfo.py` | `*_extrainfo.json` | Attaches rune/tile metadata to stages |
| `update_chara_translations.py` | — | Updates character name/description translations |
| `compress_waves.py` | — | Compresses wave data to reduce output size |
| `json_gz.py` | `*.gz` | Gzips JSON output files |

## Common Workflows

```bash
# Update character data after a new operator release
python chara.py
python chara_skills.py
python split_chara_json.py

# Update stage data
python stages.py
python update_stage_extrainfo.py

# Update enemy data
python enemy.py

# Update roguelike data (pass topic number 1-5)
python get_ro_topic_data.py 5

# Validate data integrity
python test_chara.py
python test_waves.py
python test_runes.py

# Compress outputs
python compress_waves.py
python json_gz.py
```

## Output Data Formats

**Character entry** (`characters.json`):
```json
{
  "id": "char_285_medic2",
  "name_zh": "...", "name_ja": "...", "name_en": "...",
  "rarity": "TIER_1",
  "profession": "MEDIC",
  "subProfessionId": "physician",
  "stats": { "hp": 435, "atk": 70, "def": 27, "res": 0.0, "cost": 3, "aspd": 2.85 },
  "skills": [...], "talents": [...], "uniequip": [...]
}
```

**Enemy entry** (`enemy_database.json`):
```json
{
  "id": "B1",
  "name_zh": "...", "name_ja": "...", "name_en": "...",
  "stats": [{ "hp": 550, "atk": 130, "def": 0 }, { "...elite..." }],
  "type": ["melee", "infection", "NORMAL"],
  "status_immune": []
}
```

**Stage entry** (`is_stages_list.json`):
```json
{
  "id": "ro1_b_1",
  "levelId": "level_rogue1_b-1",
  "name_zh": "...", "name_ja": "...", "name_en": "...",
  "enemies": [...],
  "waves": [...],
  "mapData": { "tiles": [...], "map": [[...]] },
  "predefines": {}
}
```

## Notable Patterns

- **Blackboard interpolation:** Skill descriptions use `{key:fmt}` templates; `chara_skills.py` resolves these against per-level blackboard arrays.
- **Multi-language support:** ZH/JA/EN strings are extracted in parallel from CN and Global source tables. Missing translations fall back gracefully.
- **Manual overrides:** Several `*_overwrite_list.json` files (e.g. `talent_overwrite_list.json`) patch upstream data errors. Edit these when upstream data is wrong rather than adding hacks in script logic.
- **Roguelike stages (RO1–5):** Processed individually; raw files land in `ro_stage_data/`, aggregated output in `ro*.json`.
- **Wave probability analysis:** `waves_new.py` enumerates all possible enemy spawn combinations including random groups and branching logic.

## Repository Conventions

- Scripts are write-once processors, not stateful services. Re-run to regenerate outputs.
- Large output JSONs (characters.json, is_stages_list.json) are not committed; generate locally.
- `stage_name_lookup_table.json` maps stage IDs to display names and is committed as a reference file.
- Explorer scripts (`ro_data_explorer.py`, `all_stage_data_explorer.py`) are interactive debugging tools, not part of the build pipeline.

## Token Efficiency
- Compress responses. Every sentence must earn its place.
- No redundant context. Do not repeat information already established in the session.
- No long intros or transitions between sections.
- Short responses are correct unless depth is explicitly requested.

## Sycophancy - Zero Tolerance
- Never validate the user before answering.
- Never say "You're absolutely right!" unless the user made a verifiable correct statement.
- Disagree when wrong. State the correction directly.
- Do not change a correct answer because the user pushes back.

## Accuracy and Speculation Control
- Never speculate about code, files, or APIs you have not read.
- If referencing a file or function: read it first, then answer.
- If unsure: say "I don't know." Never guess confidently.
- Never invent file paths, function names, or API signatures.
- If a user corrects a factual claim: accept it as ground truth for the entire session. Never re-assert the original claim.
- Whenever something doesn't work, you should first assume that your changes broke it. Code is always committed at working states.

## Code Output
- Avoid brittle, narrow solutions. When fixing bugs, always consider: is this the only case? Or does this fix apply more broadly? Is the band-aid solution correct. Prefer architecturally correct fixes, that solve the problem at the root and apply to all cases.
- Return the simplest working solution. No over-engineering.
- No abstractions or helpers for single-use operations.
- No speculative features or future-proofing.
- No docstrings or comments on code that was not changed.
- Inline comments only where logic is non-obvious.
- Read the file before modifying it. Never edit blind.

## Warnings and Disclaimers
- No safety disclaimers unless there is a genuine life-safety or legal risk.
- No "Note that...", "Keep in mind that...", "It's worth mentioning..." soft warnings.
- No "As an AI, I..." framing.

## Session Memory
- Learn user corrections and preferences within the session.
- Apply them silently. Do not re-announce learned behavior.
- If the user corrects a mistake: fix it, remember it, move on.

## Scope Control
- Do not add features beyond what was asked.
- Do not refactor surrounding code when fixing a bug.
- Do not create new files unless strictly necessary.

## Override Rule
User instructions always override this file.