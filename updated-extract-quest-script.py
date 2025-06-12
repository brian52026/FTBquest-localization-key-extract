import os
import sys
import re
import json
from concurrent.futures import ThreadPoolExecutor

out = 'out_chapters'
debug = True

extract_cache = {}

def extract_text(text: str, key: str):
    extract_cache[key] = text
    return '{' + key + '}'

def extract_title_and_desc(ctx, file_name, quest_id):
    title_regex = r'title: "(.+)"'
    desc_regex = r'description: \[((?:\s*)".*"(?:\s*),?)+\]'
    
    title_match = re.search(title_regex, ctx)
    if title_match:
        title = title_match.group(1)
        key = f"{file_name}.{quest_id}.title"
        ctx = ctx.replace(title, extract_text(title, key))
    
    desc_match = re.search(desc_regex, ctx, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1)
        lines = re.findall(r'"(.+)"', desc)
        for idx, line in enumerate(lines, start=1):
            key = f"{file_name}.{quest_id}.desc.{idx}"
            ctx = ctx.replace(line, extract_text(line, key))
    
    return ctx

def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        file_name = os.path.splitext(file_path)[0]
        with open(os.path.join(exctra_folder, file_path), 'r', encoding='utf-8') as f:
            ctx = f.read()

        quests_regex = r'quests: \[(.*)\]'
        quests_match = re.search(quests_regex, ctx, re.DOTALL)
        if quests_match:
            quests = quests_match.group(1)
            quest_blocks = re.findall(r'\{(.*?)\}', quests, re.DOTALL)
            
            for quest_block in quest_blocks:
                id_match = re.search(r'id: "(\w+)"', quest_block)
                if id_match:
                    quest_id = id_match.group(1)
                    updated_block = extract_title_and_desc(quest_block, file_name, quest_id)
                    ctx = ctx.replace(quest_block, updated_block)

        with open(os.path.join(out, file_path), 'w', encoding='utf-8') as f:
            f.write(ctx)
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

    """ with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(work_file, files)
        for res in result:
            print('[Done]', res) """
    for file in files:
        result = work_file(file)
        print('[Done]', result)
    
    # Save outdict.json in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "outdict.json"), 'w', encoding='utf-8') as f:
        json.dump(extract_cache, f, ensure_ascii=False, indent=4)
    print('All Done.')

if __name__ == '__main__':
    main()
