import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model
import sklearn
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import sklearn.model_selection

df_ = pd.read_csv('dataCLOUD4.csv', header=0)
#Thêm header cho columns
df_.columns = ["Humid","Temp","Time"]
df_.to_csv('Data.csv')

#Đọc dữ liệu + lấp giá trị bị khuyết
df = pd.read_csv('Data.csv', header=0)
df['Humid'].fillna(df['Humid'].mean(),inplace = True)
df['Temp'].fillna(df['Temp'].mean(),inplace = True)
df['Time']
print(df.shape)
#print(df.describe())

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
print(df_model)
for i in range(10000):
    if(i+1200 <= 10000):
        print(i)  
        print('yess')
        timeAfter60m = df_time[i+1200] 
        print (timeAfter60m)
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
                print("looo",kq)

                list.append({"x1":df_temp[i],
                                   "x2":df_humid[i],
                                   "x3":kq})
            else:
                count = 0
                while(not(currTimeAdd3600s <= df_time[i+1200-count] and currTimeAdd3600s >= df_time[i+1200-count-1])):
                        kq = df_temp[i+1200-count]
                        count=count+1
                print("sdghfg",kq)
                list.append({"x1":df_temp[i],
                                   "x2":df_humid[i],
                                   "x3":kq}) 
    else:
        break
    
df_model = pd.DataFrame(list)
print(df_model)                    
            


clf = linear_model.LinearRegression()
# Tạo dataframe chỉ chứa data làm biến giải thích
wine_except_quality = df_model.drop('x3', axis=1)
X = wine_except_quality
# Sử dụng quality làm biến mục tiêu
Y = df_model['x3']
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.20, random_state = 5)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# Tạo model
clf.fit(X_train, Y_train) 
print(pd.DataFrame({"Name":wine_except_quality.columns,
                    "Coefficients":clf.coef_}).sort_values(by='Coefficients') )
# Sai số
print(clf.intercept_)
# Hệ số hồi quy
def f(x,h): return  0.004243*x + -0.045646*h + 30.971943250380782
Y_pred = clf.predict(X_test)
plt.scatter(Y_test, Y_pred)
plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted")
plt.title("Current")

plt.plot(X_test['x1'],X_test['x2'],f(),c='red')