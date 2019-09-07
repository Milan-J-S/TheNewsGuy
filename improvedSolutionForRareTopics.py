#attempt with Reverse Indexing shiz
from flask import Flask, request, jsonify,session, g, redirect, url_for, abort, \
     render_template, flash
from flask_cors import CORS, cross_origin
import time
import datetime
import json
import requests
import pickle
import sqlite3

import nltk
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

nltk.download('words')
from nltk.corpus import words

import keras
from keras.models import Sequential
from keras.layers import Dense

from sklearn.neighbors import NearestNeighbors


import numpy as np
import string

from gensim.models import word2vec
model = word2vec.Word2Vec.load('text8.model')

model_vocab = list(model.wv.vocab.keys())




f = open("10kwords.txt","r")
tenwords = f.readlines()
f.close()

worddict = {}
i=0
# for word in words.words():
#     worddict[word.strip().lower()] = i
#     i+=1
    
for word in model_vocab:
    if(word.strip().lower() not in worddict):
        worddict[word.strip().lower()] = i
        # print(i, len(list(worddict.keys())))
        i+=1

 


app = Flask(__name__)
CORS(app)

keywordset = set()
keywords = []
g_tensors = []

MAX_LEN = len(list(worddict.keys()))
print("Length of worddict = ",MAX_LEN)

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/getNews", methods = ["GET","POST"])
def getNews():

    mockMatrix = [[1,2,3],[1,3,2], [2,1,3], [2,2,4]]
    scores = [0.9, 0.8, 0.92, 0.7]

    trainNeuralNet(mockMatrix, scores, 'Milan')

    q = request.args.get("q","default")
    user = request.args.get("user","default")
    global g_tensors
    global keywords
    global keywordset
    link = "https://www.googleapis.com/customsearch/v1/siterestrict?cx=018255618520952350685:fthcb7cnd4m&key=AIzaSyBMZdR1aOUuf4LgeWkyvnfk7LKCXBK6t6M&q="+q
    f = requests.get(link)
    print(f)
    arr = json.loads(f.text)
    # for i in range(len(arr)):
    #     arr[i] = str(arr[i], encoding = 'utf-8', errors = 'ignore')
    # print(arr)
    arr = arr['items']
    toSend = []
    # for item in arr:
    #     toSend.append((item['snippet']))
    meaning = arr[0]['snippet']
    tensor = np.zeros(MAX_LEN)
    toSend.append(meaning) 

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    for item in meaning.split():
        if item.lower() in worddict:
            cur.execute("INSERT INTO UserData VALUES (?,?,?)", (user, item, 1))
            con.commit()
            synset = [item.lower()]
            synset.extend([x[0] for x in model.most_similar([model.wv[item.lower()]], topn=10)])
            for syn in synset:
                print(syn.lower())
                print(worddict[syn.lower()])
                tensor[worddict[syn.lower()]] += 1
                toSend.append(syn)
                cur.execute("INSERT INTO UserData VALUES (?,?,?)", (user, syn, 2))
                con.commit()
    if(q not in keywordset):
        g_tensors.append(tensor)
        keywords.append(q)
        keywordset.add(q)
    return jsonify( data=toSend )



@app.route("/getRec", methods = ["GET","POST"])
def getRec():
    Recom = {}
    q = request.args.get("q","default")
    print("q")
    global g_tensors
    global keywords
    global keywordset
    toSend = []
    tensor = np.zeros(MAX_LEN)
    link = "https://www.googleapis.com/customsearch/v1/siterestrict?cx=018255618520952350685:fthcb7cnd4m&key=AIzaSyBMZdR1aOUuf4LgeWkyvnfk7LKCXBK6t6M&q="+q
    f = requests.get(link)
    print(f)
    arr = json.loads(f.text)
    arr = arr['items']

    meaning = arr[0]['snippet']

    for item in meaning.split():
        if item.lower() in worddict and item.lower() not in stop:
            synset = [item.lower()]
            synset.extend([x[0] for x in model.most_similar([item.lower()], topn=20) if x[0] not in stop])
            for syn in synset:
                j = worddict[syn.lower()]
                tensor[j] += 1
                for i in range(len(g_tensors)):
                    if(g_tensors[i][j]>0):
                        if(str(i) in Recom):
                            Recom[str(i)] += g_tensors[i][j]
                        else:
                            Recom[str(i)] = g_tensors[i][j]

    Recom_list = sorted(Recom.items(), key=lambda kv: kv[1], reverse = True)
    print("|",Recom_list,"|")
    if(len(Recom_list) > 3):
        for item in Recom_list[:3]:
            toSend.append(keywords[int(item[0])])



    if(q not in keywordset):
        g_tensors.append(tensor)
        keywords.append(q)
        keywordset.add(q)

    for i in range(len(g_tensors)):
        print(keywords[i], g_tensors[i].sum())

    return render_template('main.html',  items=toSend )

@app.route("/getRUserRec", methods = ["GET","POST"])
def getUserRec():
    Recom  = {}
    user = request.args.get("user","default")

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    rows = con.execute("SELECT word FROM UserData WHERE user = (?) and level = 1", (user,)).fetchall()

    print(rows)


    global g_tensors
    global keywords
    global keywordset
    toSend = []
    tensor = np.zeros(MAX_LEN)

    print(rows)

    

    for item in rows:
        if item[0].lower() in worddict:
            synset = [item[0].lower()]
            print(item[0])
            print([model.wv[item[0].lower()]])
            print("Most Simlar = ", model.most_similar([model.wv[item[0].lower()]], topn=20))
            synset.extend([x[0] for x in model.most_similar([model.wv[item[0].lower()]], topn=20)])
            for syn in synset:
                j = worddict[syn.lower()]
                tensor[j] += 1
                for i in range(len(g_tensors)):
                    if(g_tensors[i][j]>0):
                        if(str(i) in Recom):
                            Recom[str(i)] += g_tensors[i][j]
                        else:
                            Recom[str(i)] = g_tensors[i][j]

    Recom_list = sorted(Recom.items(), key=lambda kv: kv[1], reverse = True)
    print("|",Recom_list,"|")
    if(len(Recom_list) > 5):
        for item in Recom_list:
            toSend.append(keywords[int(item[0])])


    for i in range(len(g_tensors)):
        print(keywords[i], g_tensors[i].sum())

    return jsonify( data=toSend )

 


def save():
    with open("tensors.pickle") as handle:
        pickle.dump(g_tensors, handle, protocol = pickle.HIGHEST_PROTOCOL)
    with open("keywords.pickle") as handle:
        pickle.dump(keywords, handle, protocol = pickle.HIGHEST_PROTOCOL)
    with open("keywordset.pickle") as handle:
        pickle.dump(keywordset, handle, protocol = pickle.HIGHEST_PROTOCOL)
    


import atexit
atexit.register(save)

def trainNeuralNet( inp, scores, personName ):

    
    model = Sequential()
    model.add(Dense(100, input_shape = (3,),activation='elu'))
    model.add(Dense(50, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile( optimizer='adam', loss = 'mse', metrics=['mae'] )

    model.summary()

    model.save( personName+'.h5' )

    model.fit(np.array(inp), scores, batch_size=10, epochs = 1000, verbose =1)

    model.evaluate([inp], scores)

    print(model.predict([inp]))



@app.route('/validated', methods = ["GET","POST"])
def validated():
    q = request.args.get("q","")
    print("USER VALIDATED THE QUERY", q)

    return jsonify(success = 200)


if __name__ == "__main__":
    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = '0.0.0.0', debug= True )


