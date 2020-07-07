import firebase_admin
import pandas as pd
import csv 
import datetime
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('cloud-8b97d-firebase-adminsdk-2kdp3-60ae2f4dfd.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://cloud-8b97d.firebaseio.com/'  
    })

ref = db.reference('DHT11')
ref.get()
a = {}
a3 = {}
b = []
b2 = []
b3 = []
b4 = []
a = ref.child('Humidity').get()  
a2 = ref.child('Temperature').get()
a3 = ref.child('Time').get()
#print (a)
for key, value in a.items():
	b.append(value)
for key, value in a2.items():
	b2.append(value)
for key, value in a3.items():
	print (value)
	#timestamp = datetime.datetime.fromtimestamp(int(value)/1000)
	#b3.append(timestamp.strftime('%M:%S'))
	b4.append(int(value/1000))
##################################33
count = 0
for i in range(0,len(b4)-1):
	row = [b[count], b2[count], b4[count]]  
	with open('dataCLOUD4.csv', 'a+') as csvFile: 		
	    writer = csv.writer(csvFile, delimiter=',', lineterminator='\n') 	 
	    writer.writerow(row)
	count += 1
print (b)
print (b2)
print (b4)
    
