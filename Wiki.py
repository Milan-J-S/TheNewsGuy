#attempt one failed due to the Chappati anomaly
from flask import Flask, request, jsonify,session, g, redirect, url_for, abort, \
     render_template, flash
from flask_cors import CORS, cross_origin
import time
import datetime
import json
import requests
import pickle

from sklearn.neighbors import NearestNeighbors


import numpy as np
import string

f = open("10kwords.txt","r")
tenwords = f.readlines()
f.close()

worddict = {}
i=0
for word in tenwords:
    worddict[word.strip().lower()] = i
    i+=1 

app = Flask(__name__)
CORS(app)

keywordset = set()
keywords = []
g_tensors = []

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/getNews", methods = ["GET","POST"])
def getNews():
    q = request.args.get("q","default")
    global g_tensors
    global keywords
    global keywordset
    link = "https://www.googleapis.com/customsearch/v1?cx=018255618520952350685:fthcb7cnd4m&key=AIzaSyBMZdR1aOUuf4LgeWkyvnfk7LKCXBK6t6M&q="+q
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
    tensor = np.zeros(10000)
    toSend.append(meaning)
    for item in meaning.split():
        if item.lower() in worddict:
            tensor[worddict[item.lower()]] += 1
            toSend.append(item)
    if(q not in keywordset):
        g_tensors.append(tensor)
        keywords.append(q)
        keywordset.add(q)
    return jsonify( data=toSend )

@app.route("/getRec", methods = ["GET","POST"])
def getRec():
    q = request.args.get("q","default")
    print("q")
    global g_tensors
    global keywords
    global keywordset
    tensor = np.zeros(10000)
    link = "https://www.googleapis.com/customsearch/v1?cx=018255618520952350685:fthcb7cnd4m&key=AIzaSyBMZdR1aOUuf4LgeWkyvnfk7LKCXBK6t6M&q="+q
    f = requests.get(link)
    print(f)
    arr = json.loads(f.text)
    arr = arr['items']

    meaning = arr[0]['snippet']

    for item in meaning.split():
        if item.lower() in worddict:
            tensor[worddict[item.lower()]] += 1
    if(q not in keywordset):
        g_tensors.append(tensor)
        keywords.append(q)
        keywordset.add(q)

    for i in range(len(g_tensors)):
        print(keywords[i], g_tensors[i].sum())
    
    nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(g_tensors)
    distances, indices = nbrs.kneighbors([tensor])
    # res = nbrs.kneighbors([tensor])

    toSend = []
    for item in indices[0]:
        print(item)
        print(keywords[item])
        toSend.append(keywords[item])
    # for i in range(len(res[0])):
    #     print(res[0][i])
    #     print(res[1][i])
    #     print(keywords[res[1][i]])
    #     toSend.append(keywords[res[1][i]])

    

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


if __name__ == "__main__":
    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = '0.0.0.0')


