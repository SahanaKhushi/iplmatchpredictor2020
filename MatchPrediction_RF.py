#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,accuracy_score
import WicketPrediction as wp
import cloudpickle as cp
import sys


# In[2]:


batsman=pd.read_excel('C:/Users/plokesh/Downloads/IPL Project/IPL dataset/Batsman/Batsman.xlsx','Sheet2')


# In[3]:


Bat=batsman['Batsman']
Bat=Bat.drop_duplicates()
Bowler=batsman['Bowler']
Bowler=Bowler.drop_duplicates()
Venue=batsman['Venue']
Venue=Venue.drop_duplicates()
Ground=batsman['Ground']
Ground=Ground.drop_duplicates()
Score=batsman['Score']
Score=Score.drop_duplicates()
Batsman_num=pd.DataFrame({'Batsman':[],'Index':[]})
i=0
for row in Bat:
    i=i+1
    Batsman_num=Batsman_num.append({'Batsman':row,'Index':i},ignore_index=True)
    batsman.Batsman[batsman.Batsman==row]=i
        
Bowler_num=pd.DataFrame({'Bowler':[],'Index':[]})
i=0
for row in Bowler:
    i=i+1
    Bowler_num=Bowler_num.append({'Bowler':row,'Index':i},ignore_index=True)
    batsman.Bowler[batsman.Bowler==row]=i
    
city_num=pd.DataFrame({'Venue':[],'Index':[]})
i=0
for row in Venue:
    i=i+1
    city_num=city_num.append({'City':row,'Index':i},ignore_index=True)
    batsman.Venue[batsman.Venue==row]=i
    
ground_num=pd.DataFrame({'Ground':[],'Index':[]})
i=0
for row in Ground:
    i=i+1
    ground_num=ground_num.append({'Ground':row,'Index':i},ignore_index=True)
    batsman.Ground[batsman.Ground==row]=i

Score_num=pd.DataFrame({'Score':[],'Index':[]})
i=0
for row in Score:
    i=i+1
    Score_num=Score_num.append({'Score':row,'Index':i},ignore_index=True)
    batsman.Score[batsman.Score==row]=i


batsman=batsman.fillna(0)


# In[4]:


def Build_Train_Save():
    rf=RandomForestClassifier()
    
    x=batsman.drop('Score',axis=1)
    y=batsman['Score']
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)
    rf.fit(x_train,y_train)
    cp.dump(rf,open("C:/Users/plokesh/Downloads/IPL Project/Match Prediction Trained Models/mp.pkl",'wb'))
    
    p=rf.predict(x_test)
    print("Accuracy = "+str(accuracy_score(y_test, p)))


# In[ ]:





# In[ ]:





# In[5]:


def Predict(b,bo,v,g):
    test=pd.DataFrame({'Batsman':[],'Bowler':[],'Venue':[],'Ground':[]})
    test=test.append({'Batsman':b,'Bowler':bo,'Venue':v,'Ground':g},ignore_index=True)
    model=cp.load(open("C:/Users/plokesh/Downloads/IPL Project/Match Prediction Trained Models/mp.pkl",'rb'))
    
    p=model.predict(test)
    flag=True
    
    res=""
    
    for row in Score_num.itertuples():
        if(p[0]==row[2]):
            res=row[1]
            flag=False
    return res


# In[ ]:





# In[6]:


def perform_prediction(team1,batsman1,bowler1,team2,batsman2,bowler2,city,ground):
    team1_index=0
    team2_index=0
    b=0
    bo=0
    v=0
    g=0
    flag=True
    for row in city_num.itertuples():
        if(city==row[1]):
            v=row[2]
            flag=False
            
    flag=True
    for row in ground_num.itertuples():
        if(ground==row[1]):
            g=row[2]
            flag=False
            
    for row in batsman1:
        Wicket=False
        for Row in bowler2:
            
            flag=True
            for r in Batsman_num.itertuples():
                if(r[1]==row):
                    b=r[2]
                    flag=False
            flag=True
            for r in Bowler_num.itertuples():
                if(r[1]==Row):
                    bo=r[2]
                    flag=False
                    
            res=Predict(b,bo,v,g)
            
            if(res=="Less than 5" and not Wicket):
                team1_index+=2
            elif(res=="5 to 10" and not Wicket):
                team1_index+=4
            elif(res=="10 to 15" and not Wicket):
                team1_index+=6
            elif(res=="15 to 20" and not Wicket):
                team1_index+=8
            elif(res=="20 to 25" and not Wicket):
                team1_index+=10
            elif(res=="25 to 30" and not Wicket):
                team1_index+=12
            elif(res=="30 to 35" and not Wicket ):
                team1_index+=14
            elif(res=="35 to 40" and not Wicket):
                team1_index+=16
            elif(res=="40 to 45" and not Wicket):
                team1_index+=18
            elif(res=="45 to 50" and not Wicket):
                team1_index+=20
            elif(res=="More than 50" and not Wicket):
                team1_index+=22
                
            w=wp.predict_wicket(row,Row,city,ground)
            if(w==1):
                Wicket=True
                
            print(row+" "+Row+" "+res+" "+str(team1_index))
            
            
    for row in batsman2:
        Wicket=False
        for Row in bowler1:
            
            flag=True
            for r in Batsman_num.itertuples():
                if(r[1]==row):
                    b=r[2]
                    flag=False
            flag=True
            for r in Bowler_num.itertuples():
                if(r[1]==Row):
                    bo=r[2]
                    flag=False
                    
            res=Predict(b,bo,v,g)
            
            if(res=="Less than 5" and not Wicket):
                team2_index+=2
            elif(res=="5 to 10" and not Wicket):
                team2_index+=4
            elif(res=="10 to 15" and not Wicket):
                team2_index+=6
            elif(res=="15 to 20" and not Wicket):
                team2_index+=8
            elif(res=="20 to 25" and not Wicket):
                team2_index+=10
            elif(res=="25 to 30" and not Wicket):
                team2_index+=12
            elif(res=="30 to 35" and not Wicket):
                team2_index+=14
            elif(res=="35 to 40" and not Wicket):
                team2_index+=16
            elif(res=="40 to 45" and not Wicket):
                team2_index+=18
            elif(res=="45 to 50" and not Wicket):
                team2_index+=20
            elif(res=="More than 50" and not Wicket):
                team2_index+=22
                
            w=wp.predict_wicket(row,Row,city,ground)
            if(w==1):
                Wicket=True
                
            print(row+" "+Row+" "+res+" "+str(team2_index))   
            
    if(team1_index>team2_index):
        return team1
    elif(team1_index<team2_index):
        return team2
    
    return "Draw"


# In[ ]:


if __name__=="__main__":
    batsman1=sys.argv[2].split(',')
    batsman2=sys.argv[5].split(',')
    bowler1=sys.argv[3].split(',')
    bowler2=sys.argv[6].split(',')
    print perform_prediction(sys.argv[1],batsman1,bowler1,sys.argv[4],batsman2,bowler2,sys.argv[7],sys.argv[8])


# In[ ]:





# In[ ]:





# In[ ]:




