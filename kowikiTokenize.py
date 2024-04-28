#from gensim.models import Word2Vec
import pickle
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import re
from tqdm import tqdm
from eunjeon import Mecab
#from sklearn.metrics.pairwise import cosine_similarity

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # 불용어 리스트
token = []
mecab = Mecab()
with open("processed_wiki.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
    for line in tqdm(lines):
        if line and line != '\n':
            tokenized_line = mecab.morphs(line)
            stopwords_removed_sentence = [word for word in tokenized_line if not word in stopwords] # 불용어 제거
            token.append(stopwords_removed_sentence)

print("토큰화 완료. 토큰화된 문장의 일부:",token[:3])
print("토큰화된 문장 수:", len(token))
with open("tokenized_wiki.p", "wb") as f:
    pickle.dump(token, f)