#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sqlite3
import pandas as pd 
conn=sqlite3.connect('ipldb.db')

row<-"Chennai"
# In[8]:


conn.execute("INSERT INTO results (winner_name) VALUES ('AFGHANISTAN')")
conn.commit()


# In[ ]:




