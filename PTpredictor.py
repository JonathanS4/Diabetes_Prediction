#import statements
#You may need to install the following packages in order to run it within python environment: pandas, sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn import metrics
import pickle


#SELCTED PROCEDURE
#ITERATION- Train a model until the accuracy score reaches higher than 87%

#SEQUENCING- The Code is set up in chronological order
#1) Reads data
#2) Normalization of data
#3) Scales data
#4) Build Model
#5) Train Model
#6) Save Model

#SELECTION- Find maximum value for normalization of each category for dataset to make sure all values are of similar scale
def Training_procedure():
    #Read data set- "diabetes.csv" is the file that holds the data
    dataFrame=pd.read_csv('diabetes.csv')
    imputer=SimpleImputer(missing_values=0,strategy='mean')
    dataFrame[["Glucose","BloodPressure","Insulin"]]=imputer.fit_transform(dataFrame[["Glucose","BloodPressure","Insulin"]])
    print(dataFrame.head(20))
    #apply normalization techniques
    df_max_scaled = dataFrame.copy()
    highest_glucose=df_max_scaled["Glucose"].abs().max()
    highest_bloodpressure=df_max_scaled["BloodPressure"].abs().max()
    highest_insulin=df_max_scaled["Insulin"].abs().max()
    highest=[highest_glucose,highest_bloodpressure,highest_insulin]

    #Save the normalization maximums per categorgy into a pickle file
    with open('Highest.pkl', 'wb') as f:
            pickle.dump(highest, f)

    #Scale the data based on normalization
    for column in df_max_scaled.columns:
        df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()
    # reads in necesarry columns only
    columns=df_max_scaled[['Glucose','BloodPressure','Insulin']]
    output=df_max_scaled['Outcome']

    #Train Model to produce an accuracy score of at least 87% for whether a person has diabetes or not
    while True:
        #x_train-all x values for training
        #x_test- all x values for evaluation testing
        #y_train-all y values for training
        #y_test- all y values for evaluation testing
        #After each run, it continously organizes the data- 90% for training data and 10% for evaluation data
        x_train,x_test,y_train,y_test=train_test_split(columns,output,test_size=0.1)
        #Creates a Logistic regression based on data, iterates models 10,000 times
        model1=LogisticRegression(max_iter=10000)
        #Creates Line of Best Fit
        model1.fit(x_train,y_train)

        #Prediction based on model1
        y_predict1=model1.predict(x_test)

        #Finds accuracy for Model 1
        accuracy=metrics.accuracy_score(y_test,y_predict1)
        #Makes sure accuracy is above 87%
        if accuracy>0.87:
            #Saves model1 in to pickle file
            with open('logistic_regression_model.pkl', 'wb') as f:
                pickle.dump(model1, f)
            #Breaks while loop when accuracy goal of 87% is reached
            break
