from gensim.models import word2vec
from sklearn.neighbors import NearestNeighbors

sentences = word2vec.Text8Corpus('text8')


words = []
f = open("10kwords.txt","r")
tenwords = f.readlines()
f.close()
for item in tenwords:
    words.append(item.strip().lower())

model = word2vec.Word2Vec(sentences, size=50, window=5, min_count=1, workers=4,hs=1,negative=0)

# tensor = []
# for word in words:
#     tensor.append(model.wv[word])

# nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(tensor)
# distances, indices = nbrs.kneighbors([model.wv['juice']])

# for index in indices[0]:
#     print(words[index])

#  pickle the entire model to disk, so we can load&resume training later
model.save('text8.model')
# store the learned weights, in a format the original C tool understands
model.wv.save_word2vec_format('text8.model.bin', binary=True)

model = word2vec.Word2Vec.load('text8.model')

model.train([words], epochs=1000 , total_words=len(words))

model.save('text8.model')
model.wv.save_word2vec_format('text8.model.bin', binary=True)

model = word2vec.Word2Vec.load('text8.model')
print(list(model.wv.vocab.keys()))

print(model.most_similar([    
    "president", 
    ]))

