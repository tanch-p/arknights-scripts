# Type checkers

This directory contains runtime checks that compare downloaded game-data JSON
with the `TypedDict` declarations in `game_types`.

## Enemy database

Run the enemy database checker from the repository root:

```bash
python type_checkers/check_enemy_database_type.py
```

It reads
`cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json` and recursively
checks it against `EnemyFile` in `game_types/enemy_database.py`.

The checker automatically updates annotation changes that are safe to infer:

- JSON primitive changes such as `int` to `float` or `str | None`.
- An existing list or object type becoming nullable.

Structural changes cannot be named reliably without human input. New or missing
object keys, or a field changing into a new list/object shape, are logged and
raised as a `UserWarning`; the command then exits with status 1. Review those
differences and update `game_types/enemy_database.py` manually.

To report all differences without changing the type file, use:

```bash
python type_checkers/check_enemy_database_type.py --check-only
```

The checker can also be called from Python. It returns `True` when the database
matches the declarations after any safe updates:

```python
from type_checkers.check_enemy_database_type import check_enemy_database_type

is_current = check_enemy_database_type()
```
