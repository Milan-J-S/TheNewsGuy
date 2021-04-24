from flask import Flask, request, jsonify,session, g, redirect, url_for, abort, \
     render_template, flash
from flask_cors import CORS, cross_origin
import time
import datetime
import json
import requests



app = Flask(__name__)
CORS(app)

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/getNews")
def getNews():
    link = "https://www.googleapis.com/customsearch/v1?cx=018255618520952350685:8uiwqx6yz7m&key=<Enter Key here>&q=Mod"
    f = requests.get(link)
    print(f)
    arr = json.loads(f.text)
    arr = arr['items']
    toSend = []
    for item in arr:
        print (item['title'],":",item['link'])
        toSend.append((item['link']))
    return jsonify(data=toSend)


if __name__ == "__main__":
    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = '0.0.0.0')


