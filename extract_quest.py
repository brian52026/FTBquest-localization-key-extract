import os
import sys
import re
import json

from concurrent.futures import ThreadPoolExecutor


# from pygtrans import Translate

base = 'ftbquest\quests\chapters'
out = 'out_chapters'
debug = True

exctract_cache = {}


def extract_text(text: str, key: str):
    exctract_cache[key] = text
    text = '{' + key + '}'

    return text


def exctract_title(ctx, file_name):
    titleRegex = r'title: ".*"'
    titleRegexStr = r'title: "(.+)"'
    titles = re.findall(titleRegex, ctx)
    count = 0
    for i in titles:
        count += 1
        src = re.match(titleRegexStr, i).group(1)
        dst = extract_text(src, file_name + ".title." + str(count))
        ctx = ctx.replace(i, i.replace(src, dst))
    return ctx


def exctract_desc(ctx, file_name):
    descRegex = r'description: \[(?:\s*)?(?:".*"(?:\s*)?)+\]'
    targets = re.findall(descRegex, ctx, )
    count = 0
    for desc in targets:
        count += 1
        desc_old = desc
        srcs = re.findall('"(.+)"', desc)
        count2 = 0
        for src in srcs:
            count2 += 1
            dst = extract_text(src, file_name + ".desc." + str(count) + "." + str(count2))
            desc = desc.replace(src, dst)
        ctx = ctx.replace(desc_old, desc)
    return ctx


def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        file_name = os.path.splitext(file_path)[0]
        ctx = open(os.path.join(exctra_folder, file_path), 'r', encoding='utf-8').read()
        ctx = exctract_title(ctx, file_name)
        ctx = exctract_desc(ctx, file_name)
        fp = open(os.path.join(out, file_path), 'w', encoding='utf-8')
        fp.write(ctx)
        fp.close()
    return file_path


def main():
    if len(sys.argv) < 1:
        print(sys.argv[0] + " <path to exctra folder>")
        exit(1)
    global exctra_folder
    exctra_folder = sys.argv[1]
    if not os.path.exists(exctra_folder):
        print(f"Path {exctra_folder} does not exist")
        exit(1)
        
    files = os.listdir(exctra_folder)
    print('Working dir:', exctra_folder, '\nExtracting...')
    # shutil.rmtree(out)
    if not os.path.exists(out):
        os.mkdir(out)

    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(work_file, files)
        for res in result:
            print('[Done]', res)
    with open(os.path.join(out, "outdict.json"), 'w', encoding='utf-8') as f:
            json.dump(exctract_cache, f, ensure_ascii=False, indent=4)
    print('All Done.')


if __name__ == '__main__':
    main()
