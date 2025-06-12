import os
import sys
import json
import re

def parse_snbt(snbt):
    # (与 extract_quest.py 中的 parse_snbt 函数相同)
    ...

def fill_translations(snbt_data, translations):
    def replace_text(text):
        if isinstance(text, str) and text.startswith('{') and text.endswith('}'):
            key = text[1:-1]
            return translations.get(key, text)
        return text

    def process_value(value):
        if isinstance(value, dict):
            return {k: process_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [process_value(v) for v in value]
        else:
            return replace_text(value)

    return process_value(snbt_data)

def main():
    if len(sys.argv) < 3:
        print(sys.argv[0] + " <path to out_chapters folder> <path to translated outdict.json>")
        exit(1)

    out_chapters_folder = sys.argv[1]
    translations_file = sys.argv[2]

    if not os.path.exists(out_chapters_folder):
        print(f"Path {out_chapters_folder} does not exist")
        exit(1)

    if not os.path.exists(translations_file):
        print(f"Translations file {translations_file} does not exist")
        exit(1)

    with open(translations_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    for file_name in os.listdir(out_chapters_folder):
        if file_name.endswith('.snbt'):
            file_path = os.path.join(out_chapters_folder, file_name)
            print(f"Filling translations for {file_name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            snbt_data = parse_snbt(content)
            translated_data = fill_translations(snbt_data, translations)

            # Convert back to SNBT format
            output_content = json.dumps(translated_data, indent=4).replace('"', '')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output_content)

    print("All translations filled successfully.")

if __name__ == '__main__':
    main()
