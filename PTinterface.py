#import statements
#You may need to install the following packages in order to run it within python environment: tkinter, sqlite3, sklearn
from tkinter import *
from tkinter import messagebox
import sqlite3
import pickle
import warnings
from sklearn.exceptions import DataConversionWarning
import PTpredictor as PTpredict

#Takes care of some warning but not all
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)

#Running prediction algorithm
#CALLS FUNCTION
PTpredict.Training_procedure()

#Opens file after running prediction algorithm
with open('logistic_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('Highest.pkl', 'rb') as f:
    highest = pickle.load(f)
#Creates base loading screen for Tkinter
screen=Tk()
screen.title("Diabetes Predicter")
#Creates a sqlite database
conn=sqlite3.connect("Login.db")
c=conn.cursor()
c.execute("create table if not exists users (name text, password text, diabetes text);")
prediction_score=0
e1=None
e2=None
e3=None
e4=None

#PROCEDURE- predicts whether a user has diabetes or not; takes 3 parameters for all 3 catgories that user inputs
#GL- Glucose Level provided by users which is a float
#BP- Blood Pressure provided by users which is a float
#IL- Insulin Level provided by users which is a float
def get_score(GL,BP,IL):
    global e3,e4
    #LIST- holds on to all 3 data values for each catgeory provided by users
    userdata=[GL/highest[0],BP/highest[1],IL/highest[2]]
    #Only possible predictions are 0 or 1
    #Predicts model based on user input
    prediction_score=model.predict([userdata])
    #Prediction==1 means you have diabetes
    if int(prediction_score[0])==1:
        #OUTPUT- if model belives you have diabetes
        print("You have a higher chance of being diabetic")
        #Store that you have diabetes in database
        c.execute('update users set diabetes="yes" where name==(?) and password==(?);',(e3.get(),e4.get(),))
        conn.commit()
    #Prediction==0 means you don't have diabetes
    else:
        #OUTPUT- if model believes you don't have diabetes
        print("You have a lower chance of being diabetic")
        #Store that you don't have diabetes in database
        c.execute('update users set diabetes="no" where name==(?) and password==(?);',(e3.get(),e4.get(),))
        conn.commit()

#Store user username and password into sqlite database
def Store():
    #Gets user inputs for username and password
    global e1, e2
    user=e1.get()
    pw=e2.get()
    #Inserts data into database
    c.execute('insert into users(name,password,diabetes) values(?,?,?);',(user,pw,''))
    conn.commit()

#Makes sure user exists by checking through database
def Check():
    #Gets user inputs for username and password
    global e3, e4
    user=e3.get()
    pw=e4.get()
    #Checks through database for the inputed username and password
    a=c.execute('select * from users where name==(?) and password==(?);',(user,pw,))
    b=list(a)
    #Makes sure the username and password actually exist(user is already registered)
    if b!=[]:
        #Creates a new Tkinter screen asking for users to input information
        T3=Toplevel()
        #INPUT- User already Login so they can enter their glucose level, blood pressure, and insulin level to get a result
        #Input Glucose Levels
        l2=Label(T3,text="Glucose Level")
        l2.grid(row=1,column=0)
        GL=Entry(T3)
        GL.grid(row=1,column=1)

        #Input Blood Pressure Levels
        l3=Label(T3,text="Blood Pressure")
        l3.grid(row=2,column=0)
        BP=Entry(T3)
        BP.grid(row=2,column=1)

        #Input Insulin Level
        l4=Label(T3,text="Insulin Level")
        l4.grid(row=3,column=0)
        IL=Entry(T3)
        IL.grid(row=3,column=1)

        #Once user inputs are entered, they can submit their inputs
        b1=Button(T3,text="Get Prediction",command=lambda:get_score(float(GL.get()),float(BP.get()),float(IL.get())))
        b1.grid(row=4,column=0,columnspan=2)
    #If username and password doesn't actually exist in database(user is not already registered)
    else:
        #A messagebox is shown that the user hasn't inputed the correct username or password
        m1=messagebox.showerror(title="ERROR", message="Wrong Username or Password")

#Signing up function for database user
def SignUP():
    #Makes user inputs global so that the otehr functions can use them
    global e1, e2
    #Creates new screen for signup part
    T1=Toplevel()
    #INPUT- User chooses Signup which means it asks for user to enter name and password
    #Ask user for name
    l1=Label(T1,text="Name")
    l1.grid(row=0,column=0)
    e1=Entry(T1)
    e1.grid(row=0,column=1)

    #Ask users for password
    l2=Label(T1,text="Password")
    l2.grid(row=1,column=0)
    e2=Entry(T1,show="*")
    e2.grid(row=1,column=1)

    #Enter Button to store user's name and password
    b1=Button(T1,text="Complete",command=Store)
    b1.grid(row=2,column=0,columnspan=2)

def LogIN():
    #Makes user inputs global so that the otehr functions can use them
    global e3, e4
    #Creates new screen for signup part
    T2=Toplevel()
    #INPUT- User chooses Login which means it asks for user to enter name and password
    #Ask users for name
    l3=Label(T2,text="Name")
    l3.grid(row=0,column=0)
    e3=Entry(T2)
    e3.grid(row=0,column=1)

    #Ask users for password
    l2=Label(T2,text="Password")
    l2.grid(row=1,column=0)
    e4=Entry(T2,show='*')
    e4.grid(row=1,column=1)

    #Enter Button to check user's name and password
    b2=Button(T2,text="Complete",command=Check)
    b2.grid(row=2,column=0,columnspan=2)



#Creates screen for initial Login/Signup screen
F1=Frame(screen)
F1.pack()

#INPUT- User chooses Login or Signup
#Button to Signup
b1=Button(F1,text="Signup",command=SignUP)
b1.grid(row=0,column=0)

#Button to Login
b2=Button(F1,text="Login",command=LogIN)
b2.grid(row=1,column=0)

#Updates the computer
screen.mainloop()