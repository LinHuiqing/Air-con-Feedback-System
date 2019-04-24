import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

def generateEQN(data):
    #select data
    y_data  = data[:,[0]]
    
    poly = PolynomialFeatures(6,include_bias = False)
    # make x1 -> x1  x1**2 x1**3 x1**4 x1**5 x1**6
    c_1_data = poly.fit_transform(data[:,[1]])
    # make x2 -> x2  x2**2 x2**3 x2**4 x2**5 x2**6
    c_2_data = poly.fit_transform(data[:,[2]])
    
    #make a numpy array of the form of 
    #[[x1 x2 x1**2 x2**2 x1**3 x2**3 x1**4 x2**4 x1**5 x2**5 x1**6 x2**6]]    
    overall_list = []
    number_of_rows = c_1_data.shape[0]
    number_of_cols = c_1_data.shape[1]
    for i in range(number_of_rows):
        rows_list = []
        for j in range(number_of_cols):
            rows_list.append(c_1_data[i,j])
            rows_list.append(c_2_data[i,j])
            
        overall_list.append(rows_list)
    
    #there are 12 variables 
    #in the order of x1,x2,x1^2,x2^2,x1^3,x2^3......
    overall_c_matrix  =np.array(overall_list)  
    c_train,c_test,y_train,y_test = train_test_split(overall_c_matrix,y_data,test_size = 0.40,random_state=42)
    
    #create model
    regr = linear_model.LinearRegression()
    regr.fit(c_train,y_train)
    
    y_pred = regr.predict(c_test)
    MSE = mean_squared_error(y_pred,y_test)
    R2 = r2_score(y_pred,y_test)
    
    info_dict = {"MSE":MSE, "R2":R2}
    print(info_dict)
    
    return regr

def improved_getprediction(x1,x2,regr):
    ''''function will return desired temp 
    x1  = real live outside temperature (pull from firebase) 
    x2 = real live inside temperature (pull from firebase)
    regr = regression model created from data collected'''
    
    poly = PolynomialFeatures(6,include_bias = False)
    # make x1 -> x1  x1**2 x1**3 x1**4 x1**5 x1**6
    order_x1 = poly.fit_transform(np.array([[x1]]))
    # make x2 -> x2  x2**2 x2**3 x2**4 x2**5 x2**6
    order_x2 = poly.fit_transform(np.array([[x2]]))
    
    # make x input in a form of numpy array 
    prep_x = [[]]
    
    for i in range(6):
        prep_x[0].append(order_x1[0][i])
        prep_x[0].append(order_x2[0][i])
    x_input = np.array(prep_x)
    # get corresponding y value of x value
    y_pred = regr.predict(x_input)
    
    return y_pred

mylist = [[25,30,24],[26,32,22],[27,32,21],[25,32,25],[21,32,23],[20,34,23],[25,26,23]]
data = np.array(mylist)

regr = generateEQN(data)
x1 = 30
x2 = 25
print(getprediction(x1,x2,regr))
print(type(getprediction(x1,x2,regr)))
print(improved_getprediction(x1,x2,regr))
print(type(improved_getprediction(x1,x2,regr)))

mylist = [[26.0, 23.0, 16.0], [25.5, 23.6, 16.0], [25.6, 23.4, 16.5], [25.0, 23.8, 16.8], [24.7, 24.1, 16.9],
          [24.7, 24.3, 17.0], [25.0, 24.6, 17.4], [24.7, 24.9, 17.5], [24.3, 25.3, 17.8], [24.5, 25.7, 17.9],
          [24.2, 26.1, 18.0], [23.9, 26.3, 18.4], [23.7, 26.9, 18.6], [23.6, 27.3, 18.8], [23.0, 27.5, 19.0],
          [22.6, 27.6, 19.5], [22.5, 28.0, 19.8], [22.0, 28.2, 20.0], [22.0, 28.5, 20.4], [21.6, 29.0, 20.6],
          [21.1, 29.1, 20.8], [20.9, 29.4, 21.0], [20.7, 29.6, 21.4], [20.0, 30.4, 21.9], [19.8, 30.9, 22.4],
          [18.5, 31.5, 22.9], [18.4, 31.4, 23.0], [18.1, 31.7, 23.8], [19.2, 30.5, 24.0], [18.2, 31.6, 25.5],
          [18.0, 31.8, 26.5], [18.0, 32.0, 26.6], [18.0, 32.1, 26.9], [18.0, 32.5, 26.0], [18.1, 32.8, 27.0],
          [18.0, 33.1, 27.5], [18.0, 33.4, 27.6], [18.0, 30.4, 27.9], [18.0, 34.0, 28.0], [18.0, 34.1, 28.0],
          [18.0, 34.4, 27.1], [18.0, 34.6, 27.6], [18.0, 34.8, 26.8], [18.0, 35.0, 26.4], [18.2, 35.2, 26.9],
          [18.0, 35.3, 26.1], [18.0, 35.6, 25.0], [18.0, 35.9, 25.6], [18.0, 35.7, 25.7], [18.0, 36.0, 27.0],
          [25.0, 22.9, 16.2], [24.8, 23.4, 16.5], [24.4, 23.2, 16.8], [24.3, 23.6, 17.0], [24.0, 23.9, 17.8],
          [23.8, 24.1, 18.2], [23.5, 24.4, 18.3], [23.3, 24.7, 18.5], [23.2, 25.1, 18.7], [23.1, 25.5, 18.8],
          [22.8, 25.9, 18.9], [22.3, 26.1, 19.0], [22.1, 26.7, 19.1], [22.0, 27.2, 19.1], [22.0, 27.5, 19.3],
          [21.8, 27.6, 19.5], [21.5, 27.8, 19.6], [21.1, 28.0, 19.6], [21.0, 28.3, 19.7], [20.7, 28.7, 19.8],
          [20.5, 28.7, 19.8], [20.3, 29.0, 20.0], [20.0, 29.3, 20.0], [20.0, 29.5, 20.1], [22.7, 26.0, 20.3],
          [22.2, 26.2, 20.4], [22.0, 26.8, 20.5], [21.9, 27.4, 20.7], [21.8, 27.6, 20.7], [21.7, 27.7, 20.9],
          [21.4, 27.9, 21.0], [21.0, 28.1, 21.1], [20.9, 28.4, 21.3], [20.6, 28.8, 21.3], [20.4, 28.8, 21.4],
          [20.2, 29.1, 21.5], [19.8, 29.4, 21.7], [19.7, 29.6, 21.7], [19.5, 30.0, 21.9], [19.2, 30.5, 22.0],
          [18.5, 30.9, 26.5], [18.0, 31.8, 26.6], [18.0, 32.0, 26.9], [18.0, 32.4, 26.0], [18.0, 32.7, 27.0],
          [18.0, 32.9, 27.5], [18.0, 33.0, 27.6], [18.0, 34.0, 27.9], [18.2, 34.6, 28.0]]

data = np.array(mylist)
regr = generateEQN(data)

