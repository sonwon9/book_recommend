import re
import tqdm

processed_file = open("processed_wiki.txt", "w", encoding="utf8")
with open("merged_wiki.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
    for line in tqdm.tqdm(lines):
        if line:
            processed_file.write(re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", line)+"\n")

processed_file.close()