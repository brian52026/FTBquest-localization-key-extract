import os
import sys
import re
import json

from concurrent.futures import ThreadPoolExecutor

base = 'ftbquest\out_chapters'
out = 're_chapters'
debug = True

def refill_text(ctx: str, dicti: str):
    
    tagRegex = r'"{.*\..*\.\d*.*}"'
    tagRegexStr = r'"{(.*\..*\.\d*.*)}"'
    
    targets = re.findall(tagRegex, ctx)
    for tag in targets:
        key = re.match(tagRegexStr, tag).group(1)
        
        ctx = ctx.replace(tag, '"' + dicti[key] + '"')
    

    return ctx

def work_file(file_path):
    if file_path.endswith('.json'):
        return file_path
        
    if file_path == 'outdict.json':
        print('[Skip]', file_path)
        return file_path
    if os.path.isfile(os.path.join(out, file_path)):
        print('[Skip]', file_path, refill_folder)
        return file_path

    print('=>', file_path)
    
    ctx = open(os.path.join(refill_folder, file_path), 'r', encoding='utf-8').read()
    with open(os.path.join(refill_folder, 'outdict.json'), 'r', encoding='utf-8') as jsonfile:
        dicti = json.load(jsonfile)
        
    ctx = refill_text(ctx, dicti)

    with open(os.path.join(out, file_path), 'w', encoding='utf-8') as f:
        f.write(ctx)
        
    return file_path

def main():
    if len(sys.argv) < 2:
        print(sys.argv[0] + " <path to refill folder>")
        exit(1)
    global refill_folder
    refill_folder = sys.argv[1]
    if not os.path.exists(refill_folder):
        print(f"Path {refill_folder} does not exist")
        exit(1)
        
    files = os.listdir(refill_folder)
    print('Working dir:', refill_folder, '\nRefilling...')
    if not os.path.exists(out):
        os.mkdir(out)

    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(work_file, files)
        for res in result:
            print('[Done]', res)
    print('All Done.')


if __name__ == '__main__':
    main()
