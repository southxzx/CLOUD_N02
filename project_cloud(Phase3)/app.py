# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:44:35 2020

@author: LeVuong
"""
import firebase_admin
import pandas as pd
import csv 
import datetime
from sklearn import linear_model
from firebase_admin import credentials
from firebase_admin import db
import sklearn
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import sklearn.model_selection
from flask import Flask, jsonify

#Get current temperature
cred = credentials.Certificate('cloud-8b97d-firebase-adminsdk-2kdp3-60ae2f4dfd.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://cloud-8b97d.firebaseio.com/'  
    })
ref = db.reference('DHT11')
ref.get()
a = {}
a2 = {}
a = ref.child('Temperature').order_by_key().limit_to_last(1).get()
a2 = ref.child('Humidity').order_by_key().limit_to_last(1).get()
for key, value in a.items():
    temp = value
for key, value in a2.items():
    humid = value


def f(x,h): return  0.685024*x + -0.011961*h + 10.244637736759962

app = Flask(__name__)
app.config["DEBUG"] = True

#Get current temp
@app.route('/', methods=['GET'])
def home():
    return jsonify({'CurrentTemp':temp,'CurrentHumid':humid})

#Get current temp + predictTemp
@app.route('/iot', methods=['GET'])
def getNextFromCurrent():
    current_temp = temp
    next_temp = f(float(temp), float(humid))
    next_temp = "{:.2f}".format(next_temp)
    return jsonify({'CurrentTemp':current_temp,'NextTemp':next_temp})

@app.route('/iot/<string:temperature>/<string:humid>', methods=['GET'])
#Get temp from given value
def getNext(temperature,humid):
    next_temp = f(float(temperature), float(humid))
    next_temp = "{:.2f}".format(next_temp)
    return jsonify({'Temp':next_temp})

if __name__ == '__main__':
    app.run()    


