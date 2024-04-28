import re
import os

def list_wiki(dirname):
    filepaths = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        filepath = os.path.join(dirname, filename)

        if os.path.isdir(filepath):
            filepaths.extend(list_wiki(filepath))
        else:
            find = re.findall(r"wiki_[0-9][0-9]", filepath)
            if 0 < len(find):
                filepaths.append(filepath)
    return sorted(filepaths)

filepaths = list_wiki('text')

with open("merged_wiki.txt", "w", encoding="utf8") as f:
    for filename in filepaths:
        with open(filename, "r", encoding="utf8") as infile:
            contents = infile.read()
            f.write(contents)