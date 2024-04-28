from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request as req
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from gensim.models import Word2Vec
from eunjeon import Mecab
from tqdm import tqdm
import time
import re
import pickle
from book_tokenize_and_doc2vec import stopwords
#from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.linalg import norm
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

#model = Word2Vec.load("dim100_trained_word2vec_model.model") #100차원 벡터의 word2vec 로드
model = Word2Vec.load("trained_word2vec_model.model") #300차원 벡터의 word2vec 로드
with open("info_vector_list.p", "rb") as f: # [[책이름, [벡터]], [책이름, [벡터]], ...]
    info_vector_list = pickle.load(f)
story_vector_list = [v[1] for v in info_vector_list]
'''
new_info_vector_list = []
for i in range(len(info_vector_list)):
    if info_vector_list[i][1] != []:
        new_info_vector_list.append([info_vector_list[i][0], info_vector_list[i][1]])
'''

# https://www.whatismybrowser.com/detect/what-is-my-user-agent/ 에서 user_agent를 알아낼 수 있다.
User_Agent = '' # 본인의 user_agent를 입력
chrome_options = Options()
chrome_options.add_argument(f"user-agent={User_Agent }")

user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")

while user_book != '':
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://search.kyobobook.co.kr/search?keyword=" + user_book + "&gbCode=TOT&target=total"
    while True:
        try:
            driver.get(url)
            break
        except:
            time.sleep(3)
            pass
    
    book_name_list = []
    url_list = []
    try:
        for i in range(1, 11):
            js_path = driver.find_element(By.CSS_SELECTOR, "#shopData_list > ul > li:nth-child(" + str(i) +") > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div.auto_overflow_contents > div > a")
            temp = js_path.get_attribute('onclick').split(',')[1]
            url = js_path.get_attribute('href')
            url_list.append(url)
            j = 2
            s = temp[j]
            cmdtName = ''
            while s != '"':
                cmdtName += s
                j += 1
                s = temp[j]
            book_name = driver.find_element(By.CSS_SELECTOR, "#cmdtName_" + cmdtName).text
            book_name_list.append(book_name)
    except:
        pass
    # 책 검색 결과들을 가져오고 없으면 없다고 출력하고 continue, 한 개인 경우 유사한 책 추천, 두 개 이상인 경우 검색결과 상위 10개를 출력하고 이중에 무슨 책을 검색할 것인지 고르게 함.
    if not book_name_list: #검색 결과가 없는 경우
        print("책이 교보문고 사이트에 존재하지 않거나, 검색어의 철자가 정확한지 다시 한 번 확인해주세요.")
        user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")
        driver.quit()
        continue
    elif len(book_name_list) == 1:
        chosen_book_name = book_name_list[0]
        chosen_number = 1
    else:
        print("입력하신 책 제목에 대한 검색 결과는 다음과 같습니다.")
        for i in range(len(book_name_list)):
            print(str(i + 1) + "." + book_name_list[i])
        chosen_number = input("찾으신 책이 존재하면 책 제목 앞 번호를 입력해주세요. 없다면 x를 입력해주세요: ")
        if chosen_number.lower() == "x":
            print("찾는 책이 없으셨군요. 책 제목을 다시 입력해주세요")
            user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")
            driver.quit()
            continue
        else:
            chosen_number = int(chosen_number)
            chosen_book_name = book_name_list[chosen_number - 1]
    
    
    while True:
        try:
            driver.get(url_list[chosen_number - 1])
            break
        except:
            time.sleep(3)
            pass
    try:
        book_story = driver.find_element(By.CSS_SELECTOR,'div.intro_bottom').text

    except:
        print("검색하신 책의 소개가 교보문고에 기재되어 있지 않아 책 추천에 실패하였습니다.")
        user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")
        driver.quit()
        continue
        
    s = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", book_story)
    mecab = Mecab()

    tokenized_story = mecab.nouns(s) # 토큰화
    stopwords_removed_story = [word for word in tokenized_story if not word in stopwords] # 불용어 제거
    input_story_vector = get_document_vectors([stopwords_removed_story]) # 입력받은 책의 내용에 대한 문서 벡터 생성
    if input_story_vector == []:
        print("책 추천에 실패하였습니다.")
        user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")
        driver.quit()
        continue

    cosine_similarities = []
    '''
    for v in story_vector_list:

        cosine_similarities.append(cosine_similarity(input_story_vector, v))
    '''
    for v in story_vector_list:
        cosine_similarities.append(np.dot(v, input_story_vector[0]) / (norm(v) * norm(input_story_vector[0])))
    # 입력받은 책의 내용과 학습한 책의 내용들 간의 코사인 유사도 계산 
    #sim_scores = list(enumerate(cosine_similarities[0])) 
    sim_scores = list(enumerate(cosine_similarities)) 
    
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True) # 코사인 유사도가 높은 순으로 정렬
    n = 5 # 유사도가 가장 높은 n개의 책 출력
    
    if info_vector_list[sim_scores[0][0]][0] == chosen_book_name:
        for i in range(1, n + 1):
            print("책 제목: " + info_vector_list[sim_scores[i][0]][0] + ", 코사인 유사도:", sim_scores[i][1])
    else:
        for i in range(n):
            print("책 제목: " + info_vector_list[sim_scores[i][0]][0] + ", 코사인 유사도:", sim_scores[i][1])
    
    driver.quit()
    user_book = input("재미있거나 인상깊게 읽은 책 제목을 입력하세요. 아무것도 입력하지 않고 enter를 누르면 프로그램이 종료됩니다: ")