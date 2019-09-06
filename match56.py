#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import csv
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
import operator
kkrw = 0#, cskw, ddw, miw, srhw, rrw, rcbw, kxipw = 0
cskw = 0
ddw = 0
miw = 0
srhw = 0
rrw = 0
rcbw = 0
kxipw = 0
#from sklearn.metrics import roc_curve, auc
#import sqlite3
#conn=sqlite3.connect(r'C:\xampp\htdocs\DevFolio\writef.db')
#cur = conn.cursor()
#cur.execute("SELECT * FROM input")
#rows = cur.fetchall()
#print(rows)

def predict(home_team, away_team, city, toss_winner, toss_decision):
#predict('Jaipur', 'Hyderabad', 'City: Jaipur', 'RR', 'Bat')
    matches_cleaned_data = pd.read_csv(r'C:\xampp\htdocs\DevFolio\c.csv')
    matches_df = matches_cleaned_data[['t1_score', 't2_score', 'team1', 'team2', 'city', 'toss_winner', 'toss_decision', 'winner']]
    #print(away_team)
    # Split-out validation dataset
    array = matches_df.values
    x = array[:, 0:7]
    y = array[:, 7]
    validation_size = 0.10
    seed = 7
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x, y, test_size=validation_size, random_state=seed)

    # Test options and evaluation metric
    knn = DecisionTreeClassifier(criterion="entropy", max_depth=50)
    #knn = DecisionTreeClassifier()
    knn.fit(x_train, y_train)
    #print(knn.score(x_train,y_train))
    results1 = convert_to_numerical_field1(home_team, away_team)
    #print(results1)
    #ht = results1[0]
    #at = results1[1]
    #print(ht,at)
    tn = pd.read_csv(r'C:\xampp\htdocs\DevFolio\teamn.csv')
    #h = tn.loc[tn['Team'] == ht, 'sum']
    #t = tn.loc[tn['Team'] == at, 'sum']
    h = 0.4
    t = 0.2
    arg = []
    arg.append(h)
    arg.append(t)
    #print(arg)
    #h = tn.query('Team == ht')['sum']
    #t = tn.query('Team == at')['sum']
    #results1.append(h)
    #results1.append(t)
    results = convert_to_numerical_field(home_team, away_team, city, toss_winner, toss_decision)
    #print(results)
    arg.extend(results)
    #print(arg)
    predictions = knn.predict([arg])
    #print(arg)

    team = ''
    if predictions[0] == '6':
        team = 'KKR'
    if predictions[0] == "5":
        team = 'RCB'
    if predictions[0] == "9":
        team = 'CSK'
    if predictions[0] == "10":
        team = 'RR'
    if predictions[0] == "7":
        team = 'DD'
    if predictions[0] == "8":
        team = 'KXIP'
    if predictions[0] == "1":
        team = 'SRH'
    if predictions[0] == "2":
        team = 'MI'

    #print("model->" + team)
    #print(type(team))
    if int(predictions) != convert_again(home_team).__int__() and int(predictions) != convert_again(away_team).__int__():
            #print("Exception Case")
            winner = convert_to_shortform(calculate_ef_score(home_team, away_team))
            #print("EF score data ->" + winner)
            return winner
    else:
        return team.__str__()
    
    #team = [(team)]
    #conn.execute("INSERT INTO results (winner_name) VALUES (?)",team)
    #conn.commit()

def convert_to_shortform(winning_team):
    if winning_team == 'Kolkata':
        return 'KKR'
    if winning_team == "Bangalore":
        return 'RCB'
    if winning_team == "Chennai":
        return 'CSK'
    if winning_team == "Rajasthan":
        return 'RR'
    if winning_team == "Delhi":
        return 'DD'
    if winning_team == "Punjab":
        return 'KXIP'
    if winning_team == "Hyderabad":
        return 'SRH'
    if winning_team == "Mumbai":
        return 'MI'


def convert_again(home_team):
    if home_team == 'Kolkata':
        return 6
    if home_team == "Bangalore":
        return 5
    if home_team == "Chennai":
        return 9
    if home_team == "Rajasthan":
        return 10
    if home_team == "Delhi":
        return 7
    if home_team == "Punjab":
        return 8
    if home_team == "Hyderabad":
        return 1
    if home_team == "Mumbai":
        return 2


def convert_to_numerical_field(home_team, away_team, city, toss_winner, toss_decision):
    list = []
    if home_team == 'Kolkata':
        list.append(6)
    if home_team == "Bangalore":
        list.append(5)
    if home_team == "Chennai":
        list.append(9)
    if home_team == "Rajasthan":
        list.append(10)
    if home_team == "Delhi":
        list.append(7)
    if home_team == "Punjab":
        list.append(8)
    if home_team == "Hyderabad":
        list.append(1)
    if home_team == "Mumbai":
        list.append(2)

    if away_team == "Kolkata":
        list.append(6)
    if away_team == "Bangalore":
        list.append(5)
    if away_team == "Chennai":
        list.append(9)
    if away_team == "Rajasthan":
        list.append(10)
    if away_team == "Delhi":
        list.append(7)
    if away_team == "Punjab":
        list.append(8)
    if away_team == "Hyderabad":
        list.append(1)
    if away_team == "Mumbai":
        list.append(2)

    if city[6:] == "Kolkata":
        list.append(7)
    if city[6:] == "Bangalore":
        list.append(5)
    if city[6:] == "Chennai":
        list.append(2)
    if city[6:] == "Jaipur":
        list.append(11)
    if city[6:] == "Delhi":
        list.append(8)
    if city[6:] == "Dharamshala":
        list.append(24)
    if city[6:] == "Hyderabad":
        list.append(1)
    if city[6:] == "Mumbai":
        list.append(6)

    if toss_winner == "KKR":
        list.append(6)
    if toss_winner == "RCB":
        list.append(5)
    if toss_winner == "CSK":
        list.append(9)
    if toss_winner == "RR":
        list.append(10)
    if toss_winner == "DD":
        list.append(7)
    if toss_winner == "KXIP":
        list.append(8)
    if toss_winner == "SRH":
        list.append(1)
    if toss_winner == "MI":
        list.append(2)

    if toss_decision == "Bat":
        list.append(2)
    if toss_decision == "Field":
        list.append(1)
    return list

def convert_to_numerical_field1(home_team, away_team):
    list = []
    if home_team == 'Kolkata':
        list.append(6)
    if home_team == "Bangalore":
        list.append(5)
    if home_team == "Chennai":
        list.append(9)
    if home_team == "Rajasthan":
        list.append(10)
    if home_team == "Delhi":
        list.append(7)
    if home_team == "Punjab":
        list.append(8)
    if home_team == "Hyderabad":
        list.append(1)
    if home_team == "Mumbai":
        list.append(2)

    if away_team == "Kolkata":
        list.append(6)
    if away_team == "Bangalore":
        list.append(5)
    if away_team == "Chennai":
        list.append(9)
    if away_team == "Rajasthan":
        list.append(10)
    if away_team == "Delhi":
        list.append(7)
    if away_team == "Punjab":
        list.append(8)
    if away_team == "Hyderabad":
        list.append(1)
    if away_team == "Mumbai":
        list.append(2)
    return list

# prediction from site scrape data
def calculate_ef_score(home, away):
    data = pd.read_csv(r'C:\xampp\htdocs\DevFolio\_team_rank.csv')
    home_score = list(data.loc[data['Team'] == home]['sum'])
    away_score = list(data.loc[data['Team'] == away]['sum'])
    if home_score > away_score:
        return home
    else:
        return away


"""column_names=['team1', 'team2', 'city', 'toss_winner', 'toss_decision']
#data = rows
#df = pd.DataFrame.from_records(data,columns=column_names)
#df1 = df.tail(1)
***print(df1)
home_team = df1['team1'].values[0]
away_team = df1['team2'].values[0]
var="City: "
city = df1['city'].values[0]
city_final=var+city
toss_winner = df1['toss_winner'].values[0]
toss_decision = df1['toss_decision'].values[0]***
#print(city)
#predict(df1['team1'].values[0],df1['team2'].values[0],df1['city'].values[0],df1['toss_winner'].values[0],df1['toss_decision'].values[0])
#print(df1['toss_winner'].values[0])"""
data = pd.read_csv(r'C:\xampp\htdocs\DevFolio\dummy\upload\Fixtures.csv')
var="City: "
for i in range(0,56):
    #print(i)
    data1 = data.iloc[i][0]
    data2 = data.iloc[i][1]
    var="City: "
    data3 = var+data.iloc[i][2]
    data4 = data.iloc[i][3]
    data5 = data.iloc[i][4]
    a = predict(data1, data2, data3, data4, data5)
    #print(a) 
    if a == "KKR":
        kkrw = kkrw + 1
    if a == "RCB":
        rcbw = rcbw + 1
    if a == "CSK":
        cskw = cskw + 1
    if a == "RR":
        rrw = rrw + 1
    if a == "DD":
        ddw = ddw + 1
    if a == "KXIP":
        kxipw = kxipw + 1
    if a == "SRH":
        srhw = srhw + 1
    if a == "MI":
        miw = miw + 1

#print(kkrw,rcbw,cskw,rrw,ddw,kxipw,srhw,miw)
released = {
    "KKR" : kkrw,
    "RCB" : rcbw,
    "CSK" : cskw,
    "RR" : rrw,
    "DD" : ddw,
    "KXIP" : kxipw,
    "SRH" : srhw,
    "MI" : miw
}
sorted_d = sorted(released.items(), key=operator.itemgetter(1))
print(sorted_d)
b = list(sorted_d)

    
"""data1 = data.iloc[1][0]
data2 = data.iloc[1][1]
var="City: "
data3 = var+data.iloc[1][2]
data4 = data.iloc[1][3]
data5 = data.iloc[1][4]"""
#print(data1,data2,data3,data4,data5)
#a = predict(data1, data2, data3, data4, data5)

#predict('Delhi', 'Kolkata', 'City: Delhi', 'KKR', 'Bat')
#predict(home_team, away_team, city_final, toss_winner, toss_decision)
#team = [(team)]
#conn.execute("INSERT INTO results (winner_name) VALUES (?)",team)
#conn.commit()
#df1['toss_winner'].values[0]


# In[10]:


T1 = b[7][0]
T2 = b[6][0]
T3 = b[5][0]
T4 = b[4][0]
print(T1)


# In[11]:


import pymysql
db = pymysql.connect("localhost","root","","demo" )
cursor = db.cursor()


# In[12]:


cursor.execute("""INSERT INTO seasonresult (season_winner) VALUES (%s)""",(T1))
cursor.execute("""INSERT INTO seasonresult (season_winner) VALUES (%s)""",(T2))
cursor.execute("""INSERT INTO seasonresult (season_winner) VALUES (%s)""",(T3))
cursor.execute("""INSERT INTO seasonresult (season_winner) VALUES (%s)""",(T4))
db.commit()


# In[ ]:




