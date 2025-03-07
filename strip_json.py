import json

def read_and_write_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False,separators=(',', ':'))

# Example usage
# read_and_write_json("data.json")


def main():
    file_path = "enemy_database.json"  # Change this to your actual file path
    read_and_write_json(file_path)

if __name__ == "__main__":
    main()