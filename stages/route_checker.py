import json
from pathlib import Path
from typing import Any


ROGUELIKE_LEVELS_DIR = (
    Path(__file__).resolve().parents[1]
    / "cn_data"
    / "zh_CN"
    / "gamedata"
    / "levels"
    / "obt"
    / "roguelike"
)


def check_routes(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return routes that disallow diagonal movement."""
    results = []

    for route_type in ("routes", "extraRoutes"):
        for route_index, route in enumerate(data.get(route_type, [])):
            if route.get("allowDiagonalMove") is False:
                results.append(
                    {
                        "routeType": route_type,
                        "routeIndex": route_index,
                        "motionMode": route.get("motionMode"),
                    }
                )

    return results


def main() -> None:
    files_checked = 0
    matching_files = 0
    matching_actions = 0

    for rogue_number in range(1, 7):
        rogue_dir = ROGUELIKE_LEVELS_DIR / f"ro{rogue_number}"

        for json_path in sorted(rogue_dir.rglob("*.json")):
            files_checked += 1

            with json_path.open(encoding="utf-8") as file:
                data = json.load(file)

            matches = check_routes(data)
            if not matches:
                continue

            matching_files += 1
            matching_actions += len(matches)
            print(json_path.relative_to(ROGUELIKE_LEVELS_DIR))
            for match in matches:
                print(f"  {match}")

    print(
        f"Checked {files_checked} JSON files; found {matching_actions} matching "
        f"actions in {matching_files} files."
    )


if __name__ == "__main__":
    main()
