import os
import sys
import json
import re
from concurrent.futures import ThreadPoolExecutor

out = 'out_chapters'
debug = True

extract_cache = {}

def parse_snbt(snbt):
    def parse_value(s, i):
        if s[i] == '{':
            return parse_object(s, i)
        elif s[i] == '[':
            return parse_array(s, i)
        elif s[i] == '"':
            return parse_string(s, i)
        else:
            m = re.match(r'\d+[bsflBSFL]?', s[i:])
            if m:
                return m.group(0), i + len(m.group(0))
            else:
                print("m=", m, "i=", i, "s[i:]=", s[i:])
                raise ValueError(f"Unexpected character at position {i}: {s[i]}")

    def parse_object(s, i):
        obj = {}
        i += 1  # Skip '{'
        while s[i] != '}':
            key, i = parse_string(s, i)
            i = s.index(':', i) + 1  # Skip ':'
            i = skip_whitespace(s, i)
            value, i = parse_value(s, i)
            obj[key] = value
            i = skip_whitespace(s, i)
            if s[i] == ',':
                i += 1
            i = skip_whitespace(s, i)
        return obj, i + 1  # Skip '}'

    def parse_array(s, i):
        arr = []
        i += 1  # Skip '['
        while s[i] != ']':
            value, i = parse_value(s, i)
            arr.append(value)
            i = skip_whitespace(s, i)
            if s[i] == ',':
                i += 1
            i = skip_whitespace(s, i)
        return arr, i + 1  # Skip ']'

    def parse_string(s, i):
        j = i + 1
        while s[j] != '"' or s[j-1] == '\\':
            j += 1
        return s[i+1:j], j + 1

    def skip_whitespace(s, i):
        while i < len(s) and s[i].isspace():
            i += 1
        return i

    return parse_object(snbt, 0)[0]

def extract_text(text: str, key: str):
    extract_cache[key] = text
    return '{' + key + '}'

def extract_quest_texts(quest, file_name, quest_id):
    if 'title' in quest:
        key = f"{file_name}.{quest_id}.title"
        quest['title'] = extract_text(quest['title'], key)
    
    if 'description' in quest:
        desc = quest['description']
        if isinstance(desc, list):
            for idx, line in enumerate(desc, start=1):
                key = f"{file_name}.{quest_id}.desc.{idx}"
                desc[idx-1] = extract_text(line, key)
        elif isinstance(desc, str):
            key = f"{file_name}.{quest_id}.desc"
            quest['description'] = extract_text(desc, key)

def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        file_name = os.path.splitext(file_path)[0]
        with open(os.path.join(exctra_folder, file_path), 'r', encoding='utf-8') as f:
            content = f.read()

        snbt_data = parse_snbt(content)
        
        if 'quests' in snbt_data:
            for quest in snbt_data['quests']:
                if 'id' in quest:
                    extract_quest_texts(quest, file_name, quest['id'])

        # Convert back to SNBT format
        output_content = json.dumps(snbt_data, indent=4).replace('"', '')
        
        with open(os.path.join(out, file_path), 'w', encoding='utf-8') as f:
            f.write(output_content)
    return file_path

def main():
    if len(sys.argv) < 2:
        print(sys.argv[0] + " <path to extra folder>")
        exit(1)
    global exctra_folder
    exctra_folder = sys.argv[1]
    if not os.path.exists(exctra_folder):
        print(f"Path {exctra_folder} does not exist")
        exit(1)
        
    files = os.listdir(exctra_folder)
    print('Working dir:', exctra_folder, '\nExtracting...')
    if not os.path.exists(out):
        os.mkdir(out)

    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     result = executor.map(work_file, files)
    #     for res in result:
    #         print('[Done]', res)
    for target_list in files:
        res = work_file(target_list)
        print('[Done]', res)
    
    # Save outdict.json in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "outdict.json"), 'w', encoding='utf-8') as f:
        json.dump(extract_cache, f, ensure_ascii=False, indent=4)
    print('All Done.')

if __name__ == '__main__':
    main()
