#!/usr/bin/env python
# coding: utf-8

# In[1]:

while True:
    import pandas as pd
    from sklearn import model_selection
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import roc_curve, auc
    # import sqlite3
    # conn=sqlite3.connect(r'C:\Users\asahana\Desktop\IPL Project\IPL-ML-2018-master\writef.db')
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM input")
    # rows = cur.fetchall()
    #print(rows)


    # In[31]:


    import pymysql
    db = pymysql.connect("localhost","root","","demo" )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM input")
    rows = cursor.fetchall()
    data=rows


    # In[17]:


    def predict(home_team, away_team, city, toss_winner, toss_decision):
    #predict('Rajasthan', 'Hyderabad', 'City: Rajasthan', 'RR', 'Bat')
        matches_cleaned_data = pd.read_csv(r'c.csv')
        matches_df = matches_cleaned_data[['t1_score', 't2_score', 'team1', 'team2', 'city', 'toss_winner', 'toss_decision', 'winner']]
        
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
        print(knn.score(x_train,y_train))
        #results1 = convert_to_numerical_field1(home_team, away_team)
        #print(results1)
        #ht = results1[0]
        #at = results1[1]
        #print(ht,at)
        tn = pd.read_csv(r'teamn.csv')
        #h = tn.loc[tn['Team'] == ht, 'sum']
        #t = tn.loc[tn['Team'] == at, 'sum']
        h = 1.3
        t = 0.7
        arg = []
        arg.append(h)
        arg.append(t)
        #h = tn.query('Team == ht')['sum']
        #t = tn.query('Team == at')['sum']
        #results1.append(h)
        #results1.append(t)
        results = convert_to_numerical_field(home_team, away_team, city, toss_winner, toss_decision)
        print(results)
        arg.extend(results)
        print(arg)
        predictions = knn.predict([arg])
        #print(results)

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

        print("model->" + team)
        #print(type(team))
        if int(predictions) != convert_again(home_team).__int__() and int(predictions) != convert_again(away_team).__int__():
                print("Exception Case")
                winner = convert_to_shortform(calculate_ef_score(home_team, away_team))
                print("EF score data ->" + winner)
                return winner
        else:
            return team.__str__()
        
        #team = [(team)]
        #conn.execute("INSERT INTO results (winner_name) VALUES (?)",team)
        #conn.commit()


    # In[18]:


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
        if city[6:] == "Rajasthan":
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
        if away_team == "Punjab":
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


    # In[19]:


    # prediction from site scrape data
    def calculate_ef_score(home, away):
        data = pd.read_csv(r'_team_rank.csv')
        home_score = list(data.loc[data['Team'] == home]['sum'])
        away_score = list(data.loc[data['Team'] == away]['sum'])
        if home_score > away_score:
            return home
        else:
            return away


    # In[32]:


    # column_names=['team1', 'team2', 'city', 'toss_winner', 'toss_decision']
    # data = rows
    # df = pd.DataFrame.from_records(data,columns=column_names)
    print(data)


    # In[35]:


    column_names=['team1', 'team2', 'city', 'toss_winner', 'toss_decision']
    df = pd.DataFrame.from_records(list(data),columns=column_names)
    df1 = df.tail(1)
    print(df1)
    home_team = df1['team1'].values[0]
    away_team = df1['team2'].values[0]
    var="City: "
    city = df1['city'].values[0]
    city_final=var+city
    toss_winner = df1['toss_winner'].values[0]
    toss_decision = df1['toss_decision'].values[0]
    #print(city)
    #predict(df1['team1'].values[0],df1['team2'].values[0],df1['city'].values[0],df1['toss_winner'].values[0],df1['toss_decision'].values[0])
    #print(df1['toss_winner'].values[0])
    #predict('Hyderabad', 'Rajasthan', 'City: Hyderabad', 'SRH', 'Bat')
    team = predict(home_team, away_team, city_final, toss_winner, toss_decision)
    team = [(team)]
    #conn.execute("INSERT INTO results (winner_name) VALUES (?)",team)
    #conn.commit()


    # In[51]:



    #sql = ("""INSERT INTO results (winner_name) VALUES (%s) %""",(team))
    cursor.execute("""INSERT INTO results (winner_name) VALUES (%s)""",(team))
    db.commit()


    # In[49]:





    # In[ ]:





    # In[ ]:





