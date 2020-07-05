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
cred = credentials.Certificate('FireBase2\cloud-8b97d-firebase-adminsdk-2kdp3-60ae2f4dfd.json')
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


#Đọc dữ liệu + lấp giá trị bị khuyết
df = pd.read_csv('Data.csv', header=0)
df['Humid'].fillna(df['Humid'].mean(),inplace = True)
df['Temp'].fillna(df['Temp'].mean(),inplace = True)
df['Time']

#Dự báo nhiệt độ tiếp theo
df_temp = df['Temp']
df_humid = df['Humid']
df_time = df['Time']

df_model = pd.DataFrame({"x1":[],
                        "x2":[],
                        "x3":[]})
count = 1
kq = 0
list = []
# print(df_model)
for i in range(20000):
    if(i+1200 <= 20000):
        timeAfter60m = df_time[i+1200] 
        #So sánh th sau 60 phút với thời gian hiện tại
        if int(timeAfter60m) - 3600 == df_time[i]:
                            list.append({"x1":df_temp[i],
                                   "x2":df_humid[i],
                                   "x3":df_temp[i+1200]})
            #df_t = pd.DataFrame({"x1":[df_temp[i]],"x2":[df_humid[i]],"x3":[df_temp[i+1200]]})
        else:
            #Thời gian thực tế sau khi 2600s
            currTimeAdd3600s = df_time[i]+3600
            if((timeAfter60m - 3600 ) - df_time[i] < 0):
                count = 0
                while(not(currTimeAdd3600s >= df_time[i+1200+count] and currTimeAdd3600s <= df_time[i+1200+count+1])):                
                    kq = df_temp[i+1200+count]
                    count=count+1                                       

                list.append({"x1":df_temp[i],
                                   "x2":df_humid[i],
                                   "x3":kq})
            else:
                count = 0
                while(not(currTimeAdd3600s <= df_time[i+1200-count] and currTimeAdd3600s >= df_time[i+1200-count-1])):
                        kq = df_temp[i+1200-count]
                        count=count+1
                list.append({"x1":df_temp[i],
                                   "x2":df_humid[i],
                                   "x3":kq}) 
    else:
        break
    
df_model = pd.DataFrame(list)                  
            


clf = linear_model.LinearRegression()
# Tạo dataframe chỉ chứa data làm biến giải thích
wine_except_quality = df_model.drop('x3', axis=1)
X = wine_except_quality
# Sử dụng quality làm biến mục tiêu
Y = df_model['x3']
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.20, random_state = 5)

# Tạo model
clf.fit(X_train, Y_train) 
df_coef = pd.DataFrame({"Name":wine_except_quality.columns,"Coefficients":clf.coef_}).sort_values(by='Coefficients')

print (df_coef['Coefficients'][0])
print (df_coef['Coefficients'][1])
print (clf.intercept_)
# Sai số
# Hệ số hồi quy
def f(x,h): return  df_coef['Coefficients'][0]*x + df_coef['Coefficients'][1]*h + clf.intercept_
Y_pred = clf.predict(X_test)

#Dự báo nhiệt độ tiếp theo
df_temp = df['Temp']
df_humid = df['Humid']
df_time = df['Time']

app = Flask(__name__)
app.config["DEBUG"] = True


#Get current temp
@app.route('/', methods=['GET'])
def home():
    return jsonify({'Nhiet Do Hien Tai':temp},{'Do Am Hien Tai':humid})

#Get current temp + predictTemp
@app.route('/iot', methods=['GET'])
def getNextFromCurrent():
    current_temp = temp
    next_temp = f(float(temp), float(humid))
    next_temp = "{:10.2f}".format(next_temp)
    
    return jsonify({'current':current_temp, 'next':next_temp})
@app.route('/iot/<float:temperature>', methods=['GET'])

#Get temp from given value
def getNext(temperature):
    next_temp = temperature + 1.0
    return jsonify({'next':next_temp})
if __name__ == '__main__':
    app.run()