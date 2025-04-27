import json
import os

def beautify_json(input_path, output_path):
    """Beautify a JSON file."""
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Successfully beautified '{input_path}' and saved to '{output_path}'!")

def find_raw_json_files(folder="lists"):
    """Find all *_raw.json files in the specified folder."""
    return [f for f in os.listdir(folder) if f.endswith("_raw.json")]

def main():
    raw_files = find_raw_json_files()

    if not raw_files:
        print("❌ No raw JSON files found to beautify.")
        return

    for raw_file in raw_files:
        input_path = os.path.join("lists", raw_file)
        output_path = os.path.join("lists", raw_file.replace("_raw.json", "_beautified.json"))
        beautify_json(input_path, output_path)

if __name__ == "__main__":
    main()
