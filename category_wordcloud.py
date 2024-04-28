from wordcloud import WordCloud
from book_tokenize_and_doc2vec import stopwords
import matplotlib.pyplot as plt
import os
import pickle
from collections import Counter
from eunjeon import Mecab

try:
    os.mkdir('wordclouds')
except FileExistsError:
    pass

category_list = ['소설', '시,에세이', '인문', '가정,육아', '요리', '건강', '취미,실용,스포츠', 
                 '경제,경영', '자기계발', '정치,사회', '역사,문화', '종교', '예술,대중문화', '중,고등참고서', 
                 '기술,공학', '외국어', '과학', '취업,수험서', '여행', '컴퓨터,IT', '잡지', 
                 '청소년', '초등참고서', '유아(0~7세)', '어린이(초등)', '만화', '한국소개도서']
i = 0
dicts = os.listdir("./book_info_dicts")
mecab = Mecab()
for d in dicts:
    with open('./book_info_dicts/' + d, "rb") as f:
        book_info_dict = pickle.load(f)
    stories = book_info_dict.keys()
    noun_list = []
    for story in stories:
        for noun in mecab.nouns(story):
            if noun not in stopwords:
                noun_list.append(noun)

    counts = Counter(noun_list)
    tags = counts.most_common(70)

    wc = WordCloud(font_path="C:\Windows\Fonts\H2MJRE.ttf", background_color="white")
    cloud = wc.generate_from_frequencies(dict(tags)) 

    cloud.to_file("./wordclouds/wordcloud_" + category_list[i] + ".jpg")        

    i += 1
    '''
    plt.figure(figsize=(10,8))
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    '''