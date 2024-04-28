from gensim.models import Word2Vec
import pickle

with open("tokenized_wiki.p", "rb") as f:
    tokenized_data = pickle.load(f)

print("토큰화된 데이터들 로드 완료, word2vec 학습 시작")
model = Word2Vec(sentences = tokenized_data, vector_size = 300, window = 10, min_count = 5, workers = 4, sg = 0)
#model = Word2Vec(sentences = tokenized_data, vector_size = 100, window = 5, min_count = 5, workers = 4, sg = 0)

print(model.wv.vectors.shape)

model.save("trained_word2vec_model.model") # 로드 : model = Word2Vec.load("trained_word2vec_model.model")
#model.save("dim100_trained_word2vec_model.model") # 로드 : model = Word2Vec.load("dim100_trained_word2vec_model.model")