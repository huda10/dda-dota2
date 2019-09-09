#!/usr/bin/env python
# coding: utf-8

# In[8]:


from flask import *
import numpy as np
import pandas as pd
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
    fname = path.expanduser('static/dota2 player_skill.csv')
    dataSet = pd.read_csv(fname)
    idn = len(dataSet) + 1
    dataSet = dataSet.append({"id": idn,"matchId": matchid, "kills": kills, "deaths": deaths, "assists": assists, "last_hits": last_hits,
                              "denies": denies, "gold_per_min": gold_per_min, "xp_per_min": xp_per_min,
                             "capability_level": capability_level, "potency_level": potency_level, "time": time,
                             "final_level": final_level} , ignore_index=True)
    dataSet.to_csv(fname, index=False)
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
    fname = path.expanduser('static/dota2 match_info.csv')
    dataSet = pd.read_csv(fname)
    dataSet = dataSet.append({"matchId": matchid, "steamId": steamid, "match_time": match_time, "difficulty_option": DiffOp}, 
                             ignore_index=True)
    dataSet.to_csv(fname, index=False)
    return "information is saved"


# In[ ]:


if __name__ == "__main__":
    app.run(debug=True)

