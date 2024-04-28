# 베스트셀러 워드클라우드 & 사용자가 읽었던 책을 기반으로 도서 추천

Windows 환경, python 3.7 환경에서 개발됨.
각 카테고리별 베스트셀러에서 명사들을 추출하여 워드클라우드를 생성 / 사용자가 인상깊거나 흥미롭게 읽은 책을 입력받아 그와 유사한 도서를 추천함.

## 실행 순서

1. 한국어 위키피디아 데이터셋 불러와서 압축 해제하기 
```cmd
pip install wikiextractor
wget https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2
python -m wikiextractor.WikiExtractor kowiki-latest-pages-articles.xml.bz2
```

2. kowikiMerge.py 실행 (merged_wiki.txt 생성됨)

3. kowikiPreprocess.py 실행 (processed_wiki.txt 생성됨)

4. kowikiTokenize.py 실행 (tokenized_wiki.p 생성됨)

5. word2vec_training.py 실행 (trained_word2vec_model.model 생성됨)
  
5-1. 워드 임베딩 모델을 test 해보고 싶으면, load_word2vec.py 실행

5-2. 워드클라우드 생성을 원하면, category_wordcloud.py 실행 (wordclouds 폴더가 생성되고 그 안에 워드클라우드 이미지들 생성됨)

6. book_crawling_and_preprocess.py 실행 (book_info_dicts 폴더가 생성되고 그 안에 book_info_dictNN.p 파일들 생성됨, NN: category number)

7. book_tokenize_and_doc2vec.py 실행 (story_vector_list.p, info_vector_list.p 파일 생성됨)

8. book_recommend.py 실행(메인 프로그램)
