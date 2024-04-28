from gensim.models import Word2Vec
from eunjeon import Mecab
from tqdm import tqdm
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

def get_document_vectors(document_list): # 책 소개 문서에 대한 벡터를 구하는 함수
    document_embedding_list = []

    # 각 문서에 대해서
    for document in tqdm(document_list):
        doc2vec = None
        count = 0
        for word in document:
            if word in list(model.wv.index_to_key):
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = model.wv[word]
                else:
                    doc2vec = doc2vec + model.wv[word]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

        else:
            document_embedding_list.append([])

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list

stopwords = ["수", "책", "저자", "작가", "베스트셀러"] # 불용어 리스트
# https://gist.github.com/chulgil/d10b18575a73778da4bc83853385465c#file-stopwords-txt에서 불용어 목록 가져옴
with open("stopwords.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
    for line in lines:
        stopwords.append(line.strip())

if __name__ == "__main__":
    mecab = Mecab()
    info_dict = {}
    info_list = [file for file in os.listdir("./book_info_dicts")]
    for info in info_list:
        with open("./book_info_dicts/" + info, "rb") as f:
            temp = pickle.load(f)
        print(info + "에 들어있던 책의 수:", len(temp))
        info_dict.update(temp)
    print("수집한 책의 권수:", len(info_dict))



    tokenized_info_list = []

    for story, book in info_dict.items():
        tokenized_story = mecab.nouns(story)
        stopwords_removed_story = [word for word in tokenized_story if not word in stopwords] # 불용어 제거
        tokenized_info_list.append([book, stopwords_removed_story])

    #model = Word2Vec.load("dim100_trained_word2vec_model.model") #100차원 벡터의 word2vec 로드
    model = Word2Vec.load("trained_word2vec_model.model") #300차원 벡터의 word2vec 로드



    story_vector_list = get_document_vectors([info[1] for info in tokenized_info_list])

    with open("story_vector_list.p", "wb") as f:
        pickle.dump(story_vector_list, f)

    info_vector_list = []
    '''
    for story_vector, book in story_vector_list, [info[0] for info in tokenized_info_list]:
        if story_vector is not []:
            info_vector_list.append([book, story_vector])
    print(len(info_vector_list))
    '''

    for i in range(len(story_vector_list)):
        if story_vector_list[i] != []:
            info_vector_list.append([tokenized_info_list[i][0], story_vector_list[i]])
    print(len(info_vector_list))

    with open("info_vector_list.p", "wb") as f:
        pickle.dump(info_vector_list, f)