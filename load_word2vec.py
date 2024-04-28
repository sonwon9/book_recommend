from gensim.models import Word2Vec

#model = Word2Vec.load("dim100_trained_word2vec_model.model") #100차원 벡터의 word2vec 로드
model = Word2Vec.load("trained_word2vec_model.model") #300차원 벡터의 word2vec 로드


print("word2vec 모델 로드 완료.")

a = input()

while a:
    print(model.wv.most_similar(a))
    a = input()
