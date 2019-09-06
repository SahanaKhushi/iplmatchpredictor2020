#!/usr/bin/env python
# coding: utf-8

# In[77]:


import sqlite3
import pandas as pd 
conn=sqlite3.connect('ipl2.db')
cur = conn.cursor()
cur.execute("SELECT * FROM match")
rows = cur.fetchall()


# In[83]:


# for row in rows:
#             print(row)
column_names=['id', 'season', 'city', 'date', 'team1', 'team2', 'toss_winner', 'toss_decision', 'result', 'winner', 'win_by_runs', 'win_by_wickets', 'player_of_match', 'venue']
data=rows
df = pd.DataFrame.from_records(data, columns =column_names) 
df = df.iloc[1:]
print(df)

