#!/usr/bin/env python
# coding: utf-8

# In[8]:


from flask import *
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import numpy as np
from os import path
import math
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import tensorflow as tf
import operator
np.random.seed(7)


# In[2]:


f = open("static/Maximum Values.txt", "r")
A = f.read().split(',')
f.close()


# In[5]:


for i in range(len(A)):
    A[i] = int(A[i])


# In[9]:


json_file = open("static/model1 with 1hl 30 hnodes.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model1 = model_from_json(loaded_model_json)
 #load weights into new model
loaded_model1.load_weights("static/model1 with 1hl 30 hnodes.h5")
loaded_model1._make_predict_function()
graph = tf.get_default_graph()


# In[10]:


loaded_model1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[11]:


json_file = open("static/model2 with 1hl 32 hnodes.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model2 = model_from_json(loaded_model_json)
# load weights into new model
loaded_model2.load_weights("static/model2 with 1hl 32 hnodes.h5")
loaded_model2._make_predict_function()


# In[12]:


loaded_model2.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[7]:


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

class Dataskills(db.Model):
    __tablename__ = "Dataskills"
    id = db.Column(db.Integer, primary_key=True)
    matchId = db.Column(db.String(32))
    kills = db.Column(db.Float)
    deaths = db.Column(db.Float)
    assists = db.Column(db.Float)
    last_hits = db.Column(db.Float)
    denies = db.Column(db.Float)
    gold_per_min = db.Column(db.Float)
    xp_per_min = db.Column(db.Float)
    capability_level = db.Column(db.Float)
    potency_level = db.Column(db.Float)
    time = db.Column(db.Float)
    final_level = db.Column(db.Float)

    def __init__ (self, matchId, kills, deaths, assists, last_hits, denies, gold_per_min, xp_per_min, capability_level, potency_level, 
                 time, final_level):
        self.matchId = matchId
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.last_hits = last_hits
        self.denies = denies
        self.gold_per_min = gold_per_min
        self.xp_per_min = xp_per_min
        self.capability_level = capability_level
        self.potency_level = potency_level
        self.time = time
        self.final_level = final_level

class Matchinfo(db.Model):
    __tablename__ = "Matchinfo"
	id = db.Column(db.Integer, primary_key=True)
    matchId = db.Column(db.String(32))
    steamId = db.Column(db.String(32))
    match_time = db.Column(db.Float)
    difficulty_option = db.Column(db.String(32))

    def __init__ (self, matchId, steamId, match_time, difficulty_option):
        self.matchId = matchId
        self.steamId = steamId
        self.match_time = match_time
        self.difficulty_option = difficulty_option

# In[14]:


@app.route("/save", methods = ['GET'])
def save():
    input1 = np.empty(5)
    input2 = np.empty(2)
    matchid = request.args.get('matchid')
    kills = float(request.args.get('kills'))
    deaths = float(request.args.get('deaths'))
    assists = float(request.args.get('assists'))
    last_hits = float(request.args.get('last_hits'))
    denies = float(request.args.get('denies'))
    gold_per_min = float(request.args.get('gold_per_min'))
    xp_per_min = float(request.args.get('xp_per_min'))
    time = float(request.args.get('time'))
    input1[0] = kills / float(A[0])
    input1[1] = deaths / float(A[1])
    input1[2] = assists / float(A[2])
    input1[3] = last_hits / float(A[3])
    input1[4] = denies / float(A[4])
    input2[0] = gold_per_min / float(A[5])
    input2[1] = xp_per_min / float(A[6])
    global graph
    with graph.as_default():
        p=loaded_model1.predict(np.array([input1]))[0]
    capability_level, value = max(enumerate(p), key=operator.itemgetter(1))
    with graph.as_default():
        p=loaded_model2.predict(np.array([input2]))[0]
    potency_level, value = max(enumerate(p), key=operator.itemgetter(1))
    final_level = math.ceil((capability_level + potency_level) / 2.0)
    indata = Dataskills(matchid, kills, deaths, assists, last_hits, denies, gold_per_min, xp_per_min, capability_level, potency_level,
                       time, final_level)
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(indata)))
        print(e)
        sys.stdout.flush()
    return "%i" %final_level 


# In[ ]:


@app.route("/saveMatchInfo", methods = ['GET'])
def saveMatchInfo():
    matchid = request.args.get('matchid')
    steamid = request.args.get('steamid')
    match_time = float(request.args.get('match_time'))
    difficulty_option = int(request.args.get('difficulty_option'))
    DiffOp = ""
    if difficulty_option == 0:
        DiffOp = "Passive"
    elif difficulty_option == 1:
        DiffOp = "Easy"
    elif difficulty_option == 2:
        DiffOp = "Medium"
    elif difficulty_option == 3:
        DiffOp = "Hard"
    elif difficulty_option == 4:
        DiffOp = "Unfair"
    elif difficulty_option == 5:
        DiffOp = "Dynamic"
    indata = Matchinfo(matchid, steamid, match_time, DiffOp)
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(indata)))
        print(e)
        sys.stdout.flush()
    return "information is saved"


# In[ ]:


if __name__ == "__main__":
    app.run(debug=True)
