# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:44:35 2020

@author: LeVuong
"""
import firebase_admin
import pandas as pd
import csv 
import datetime
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, jsonify

#Get current temperature
cred = credentials.Certificate('cloud-8b97d-firebase-adminsdk-2kdp3-60ae2f4dfd.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://cloud-8b97d.firebaseio.com/'  
    })
ref = db.reference('DHT11')
ref.get()
a = {}
a = ref.child('Temperature').order_by_key().limit_to_last(1).get()
for key, value in a.items():
	b = value



app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return jsonify({'Nhiet Do Hien Tai':b})

@app.route('/iot', methods=['GET'])
def getNextFromCurrent():
    current_temp = 0.0
    next_temp = 1.0
    
    return jsonify({'current':current_temp, 'next':next_temp})
@app.route('/iot/<float:temperature>', methods=['GET'])
def getNext(temperature):
    next_temp = temperature + 1.0
    return jsonify({'next':next_temp})
if __name__ == '__main__':
    app.run()