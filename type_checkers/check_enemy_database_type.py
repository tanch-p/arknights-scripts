"""Check enemy_database.json against its TypedDict declarations."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import logging
import sys
import types
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union, cast, get_args, get_origin, get_type_hints, is_typeddict

LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = (
    PROJECT_ROOT / "cn_data/zh_CN/gamedata/levels/enemydata/enemy_database.json"
)
DEFAULT_TYPE_FILE_PATH = PROJECT_ROOT / "game_types/enemy_database.py"

_JSON_PRIMITIVES = (bool, int, float, str, type(None))
_PRIMITIVE_NAMES = {
    bool: "bool",
    int: "int",
    float: "float",
    str: "str",
    type(None): "None",
}


@dataclass(frozen=True)
class TypeIssue:
    """A difference between the JSON data and its declared type."""

    path: str
    expected: str
    actual: str
    reason: str

    def __str__(self) -> str:
        return (
            f"{self.path}: {self.reason} "
            f"(expected {self.expected}, found {self.actual})"
        )


@dataclass
class _CheckResult:
    issues: list[TypeIssue]
    observations: dict[tuple[str, str], list[object]]
    annotations: dict[tuple[str, str], object]


class _Validator:
    def __init__(self, module: types.ModuleType) -> None:
        self.module = module
        self.issues: list[TypeIssue] = []
        self.observations: dict[tuple[str, str], list[object]] = defaultdict(list)
        self.annotations: dict[tuple[str, str], object] = {}

    def check(self, value: object, annotation: object, path: str) -> _CheckResult:
        self._validate(value, annotation, path)
        return _CheckResult(
            self.issues,
            dict(self.observations),
            self.annotations,
        )

    def _hints(self, annotation: object) -> dict[str, object]:
        return get_type_hints(
            annotation,
            globalns=vars(self.module),
            localns=vars(self.module),
        )

    def _validate(self, value: object, annotation: object, path: str) -> None:
        if annotation in (Any, object):
            return

        origin = get_origin(annotation)
        if origin in (Union, types.UnionType):
            options = get_args(annotation)
            if any(self._matches(value, option) for option in options):
                return
            compatible = [
                option for option in options if self._outer_matches(value, option)
            ]
            if compatible:
                self._validate(value, compatible[0], path)
            else:
                self._add_type_issue(path, annotation, value)
            return

        if is_typeddict(annotation):
            if type(value) is not dict:
                self._add_type_issue(path, annotation, value)
                return
            self._validate_typed_dict(cast(dict[str, object], value), annotation, path)
            return

        if origin is list:
            if type(value) is not list:
                self._add_type_issue(path, annotation, value)
                return
            item_type = get_args(annotation)[0] if get_args(annotation) else Any
            for index, item in enumerate(value):
                self._validate(item, item_type, f"{path}[{index}]")
            return

        if origin is dict:
            if type(value) is not dict:
                self._add_type_issue(path, annotation, value)
                return
            key_type, value_type = get_args(annotation) or (Any, Any)
            for key, item in value.items():
                self._validate(key, key_type, f"{path}.<key>")
                self._validate(item, value_type, f"{path}[{key!r}]")
            return

        if isinstance(annotation, type) and type(value) is not annotation:
            self._add_type_issue(path, annotation, value)

    def _validate_typed_dict(
        self,
        value: dict[str, object],
        annotation: object,
        path: str,
    ) -> None:
        hints = self._hints(annotation)
        required = getattr(annotation, "__required_keys__", frozenset(hints))
        type_name = getattr(annotation, "__name__", repr(annotation))

        for key in sorted(required - value.keys()):
            self.issues.append(
                TypeIssue(
                    f"{path}.{key}",
                    _type_name(hints[key]),
                    "missing",
                    "required key is missing",
                )
            )
        for key in sorted(value.keys() - hints.keys(), key=str):
            self.issues.append(
                TypeIssue(
                    f"{path}.{key}",
                    "no key",
                    _type_name(type(value[key])),
                    "unexpected key",
                )
            )

        for key in value.keys() & hints.keys():
            field_annotation = hints[key]
            site = (type_name, key)
            self.observations[site].append(value[key])
            self.annotations[site] = field_annotation
            self._validate(value[key], field_annotation, f"{path}.{key}")

    def _matches(self, value: object, annotation: object) -> bool:
        if annotation in (Any, object):
            return True
        origin = get_origin(annotation)
        if origin in (Union, types.UnionType):
            return any(self._matches(value, option) for option in get_args(annotation))
        if is_typeddict(annotation):
            if type(value) is not dict:
                return False
            hints = self._hints(annotation)
            required = getattr(annotation, "__required_keys__", frozenset(hints))
            if not required <= value.keys() or not value.keys() <= hints.keys():
                return False
            return all(self._matches(value[key], hints[key]) for key in value)
        if origin is list:
            if type(value) is not list:
                return False
            item_type = get_args(annotation)[0] if get_args(annotation) else Any
            return all(self._matches(item, item_type) for item in value)
        if origin is dict:
            if type(value) is not dict:
                return False
            key_type, value_type = get_args(annotation) or (Any, Any)
            return all(
                self._matches(key, key_type) and self._matches(item, value_type)
                for key, item in value.items()
            )
        return isinstance(annotation, type) and type(value) is annotation

    def _outer_matches(self, value: object, annotation: object) -> bool:
        origin = get_origin(annotation)
        if is_typeddict(annotation) or origin is dict:
            return type(value) is dict
        if origin is list:
            return type(value) is list
        return isinstance(annotation, type) and type(value) is annotation

    def _add_type_issue(self, path: str, annotation: object, value: object) -> None:
        self.issues.append(
            TypeIssue(
                path,
                _type_name(annotation),
                _type_name(type(value)),
                "type changed",
            )
        )


def _type_name(annotation: object) -> str:
    if annotation is type(None):
        return "None"
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _load_type_module(type_file_path: Path) -> types.ModuleType:
    module_name = f"_enemy_database_types_{id(type_file_path)}"
    spec = importlib.util.spec_from_file_location(module_name, type_file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load type declarations from {type_file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def _check(
    data: object,
    type_file_path: Path,
    root_type_name: str,
) -> _CheckResult:
    module = _load_type_module(type_file_path)
    try:
        root_type = getattr(module, root_type_name)
    except AttributeError as error:
        raise AttributeError(
            f"{type_file_path} does not define {root_type_name}"
        ) from error
    return _Validator(module).check(data, root_type, "$")


def _annotation_nodes(source: str) -> dict[tuple[str, str], ast.expr]:
    tree = ast.parse(source)
    nodes: dict[tuple[str, str], ast.expr] = {}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for statement in node.body:
                if isinstance(statement, ast.AnnAssign) and isinstance(
                    statement.target, ast.Name
                ):
                    nodes[(node.name, statement.target.id)] = statement.annotation
        elif (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "TypedDict"
            and len(node.value.args) >= 2
            and isinstance(node.value.args[0], ast.Constant)
            and isinstance(node.value.args[0].value, str)
            and isinstance(node.value.args[1], ast.Dict)
        ):
            class_name = node.value.args[0].value
            for key, value in zip(
                node.value.args[1].keys, node.value.args[1].values, strict=True
            ):
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    nodes[(class_name, key.value)] = value
    return nodes


def _replacement_for(
    annotation: object,
    current_source: str,
    values: list[object],
    validator: _Validator,
) -> str | None:
    actual_types = {type(value) for value in values}
    if actual_types == {type(None)}:
        return f"{current_source} | None"
    if actual_types and actual_types <= set(_JSON_PRIMITIVES):
        ordered = [kind for kind in _JSON_PRIMITIVES if kind in actual_types]
        return " | ".join(_PRIMITIVE_NAMES[kind] for kind in ordered)

    non_none = [value for value in values if value is not None]
    if (
        len(non_none) != len(values)
        and non_none
        and all(validator._matches(value, annotation) for value in non_none)
        and not validator._matches(None, annotation)
    ):
        return f"{current_source} | None"
    return None


def _update_annotations(
    type_file_path: Path,
    result: _CheckResult,
) -> list[str]:
    source = type_file_path.read_text(encoding="utf-8")
    nodes = _annotation_nodes(source)
    lines = source.splitlines(keepends=True)
    offsets: list[int] = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    replacements: list[tuple[int, int, str, str]] = []
    validator = _Validator(_load_type_module(type_file_path))
    issue_sites = {
        site
        for site, values in result.observations.items()
        if any(
            not validator._matches(value, result.annotations[site]) for value in values
        )
    }

    for site in issue_sites:
        node = nodes.get(site)
        if node is None or node.end_lineno is None or node.end_col_offset is None:
            continue
        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset
        current = source[start:end]
        replacement = _replacement_for(
            result.annotations[site],
            current,
            result.observations[site],
            validator,
        )
        if replacement is not None and replacement != current:
            replacements.append((start, end, replacement, f"{site[0]}.{site[1]}"))

    if not replacements:
        return []

    for start, end, replacement, _ in sorted(replacements, reverse=True):
        source = source[:start] + replacement + source[end:]
    type_file_path.write_text(source, encoding="utf-8")
    return [description for _, _, _, description in replacements]


def _warn_about_issues(issues: list[TypeIssue], *, update_enabled: bool) -> None:
    details = "\n".join(f"- {issue}" for issue in issues)
    if update_enabled:
        summary = "the remaining changes could not be updated safely"
    else:
        summary = "automatic updates were disabled"
    message = (
        "enemy_database.json does not match game_types/enemy_database.py, and "
        f"{summary}:\n{details}"
    )
    LOGGER.warning(message)
    warnings.warn(message, UserWarning, stacklevel=2)


def check_enemy_database_type(
    database_path: str | Path = DEFAULT_DATABASE_PATH,
    type_file_path: str | Path = DEFAULT_TYPE_FILE_PATH,
    *,
    update: bool = True,
    root_type_name: str = "EnemyFile",
) -> bool:
    """Validate the enemy database and update safe annotation changes.

    Primitive changes (for example, ``int`` to ``float``) and newly nullable
    existing types can be rewritten automatically. Structural changes, such as
    new object keys, are logged and emitted as :class:`UserWarning` instances.

    Returns ``True`` when the database matches after any updates.
    """

    database_path = Path(database_path)
    type_file_path = Path(type_file_path)
    with database_path.open(encoding="utf-8") as database_file:
        data = json.load(database_file)

    result = _check(data, type_file_path, root_type_name)
    if not result.issues:
        LOGGER.info("Enemy database types are up to date")
        return True

    if update:
        updated = _update_annotations(type_file_path, result)
        if updated:
            LOGGER.info("Updated enemy database types: %s", ", ".join(updated))
            result = _check(data, type_file_path, root_type_name)

    if result.issues:
        _warn_about_issues(result.issues, update_enabled=update)
        return False

    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE_PATH)
    parser.add_argument("--types", type=Path, default=DEFAULT_TYPE_FILE_PATH)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="report mismatches without updating safe annotation changes",
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return (
        0
        if check_enemy_database_type(
            args.database,
            args.types,
            update=not args.check_only,
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
