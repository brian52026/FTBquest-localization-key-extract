import os
import sys
import json
import re

def fill_translations(file_path, translations):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for key, value in translations.items():
        placeholder = '{' + key + '}'
        content = content.replace(placeholder, value)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

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
            fill_translations(file_path, translations)

    print("All translations filled successfully.")

if __name__ == '__main__':
    main()
