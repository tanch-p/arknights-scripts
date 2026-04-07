import os
import shutil
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")
DEST_DIR = os.getenv("DEST_DIR")

# TARGET_FILES = ["char_4224_turdus", "char_4223_botany","char_1051_headb2"]
TARGET_FILES = [
    "skchr_headb2_1",
    "skchr_headb2_2",
    "skchr_headb2_3",
    "skchr_botany_1",
    "skchr_botany_2",
    "skchr_turdus_1",
    "skchr_turdus_2",
]


def get_images(category, file_names):
    if category == "char":
        folder_prefix = "ui_char_avatar_"
    elif category == "skill":
        folder_prefix = "skill_icons_"
        file_names = [f"skill_icon_{name}" for name in file_names]

    ensure_dest()
    results = find_and_copy(folder_prefix, file_names)

    print("Copied files:" if results else "No matching files found.")
    for r in results:
        print(r)


def ensure_dest():
    os.makedirs(DEST_DIR, exist_ok=True)


def get_unique_path(dest_path):
    base, ext = os.path.splitext(dest_path)
    counter = 1

    while os.path.exists(dest_path):
        dest_path = f"{base}({counter}){ext}"
        counter += 1

    return dest_path


def get_target_folders(folder_prefix):
    """Find folders that start with the prefix"""
    folders = []

    for name in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, name)

        if os.path.isdir(full_path) and name.startswith(folder_prefix):
            folders.append(full_path)

    return folders


def find_and_copy(folder_prefix, keys):
    found = []

    folders = get_target_folders(folder_prefix)

    for folder_path in folders:
        for file in os.listdir(folder_path):
            file_name, _ = os.path.splitext(file)

            if file_name in keys:
                src_path = os.path.join(folder_path, file)

                dest_path = get_unique_path(os.path.join(DEST_DIR, file))
                shutil.copy2(src_path, dest_path)

                found.append(dest_path)

    return found


if __name__ == "__main__":
    get_images("skill",TARGET_FILES)
