
# coding: utf-8

# # Monzo Data Visualisation Jupyter Notebook
# 
# This notebook shall outline the steps take to clear the data, and use it for visualisation.
# 
# It's a way for me to apply all my knowledge about data analytics and hopefully make sense of how much money I spend.
# 
# 
# I shall be using Pandas as the data handling library. However, as a learning experience it may not contain "smart" uses of pandas
# 

# In[17]:


## Importing Libraries ##

import pandas as pd
import numpy as np
from datetime import datetime as dt


## Importing Data ##
df = pd.read_csv('./MonzoDataExport_Alltime_2018-08-26_104716.csv');

## Look at Data Structure ##
df.head()

# Decide which columns matter, this can be changed later ##

columnsToKeep = ['amount', 'local_amount', 'category', 'created', 'description'];

df = df[columnsToKeep]


# In[2]:


## We want to replace NaNs with "Unlabelled" to make it clear ##
### This has two cases, for income (+ve numbers) and transactions (-ve numbers) ###
### We can change the category for incoming to "income" and transactions to "unlabelled" ###

df.loc[(df['category'].isnull()) & (df.amount > 0), 'category']='income'
df.loc[(df['category'].isnull()) & (df.amount <= 0), 'category']='unlabelled'

df


# ## Thinking Exercise:
# 
# ### Date-Time:
# 
# Currently the data is sorted by "created", which is the date-time of the transaction.
# If we want any useful visualisations over time, this data is super important and needs to be cleaned up for sure
# 
# **TODO: Clean date-time** 
# 
# ### Incoming vs Outgoing:
# 
# Understandably, the values for outgoing are negative whereas the incoming is +ve. 
# But if we're focusing on spending, it would definitely be easier to deal with all the data as +ve, but have good labels for incoming and outgoing.
# 
# We currently have the label of "incoming" for any values that are coming in, but this doesn't cover any transactions that were 
# 1. Not top-ups
# 2. Were bank transfers
# 3. were refunds
# 
# We need to find a way to distinctly label the data as incoming vs outgoing, we can use the 'local_amount' column for this. Since we need to retain the category label for future classification
# 
# **TODO: Add a new column for incoming/outgoing labels**
# 
# ### Savings transfers:
# 
# A feature of Monzo is being able to transfer money out of current checking account into a "pot", which is just a virtual distinction of money labelled for saving rather than spending.
# 
# This means that any transfers of data from the pots is basically going in or out is going to be unlabelled and will need distinction in comparison to income or outgoing.
# 
# **TODO: Identify pot transfers with the keywords `from pot` and `to pot` and deal with them differently **
# 
# ### Transfers from other accounts:
# 
# Transfers using `monzo.me/` or  simple bank transfers wouldn't have any labels and would be labelled as "income" in general. This needs distinction as well.
# 
# **TODO: Identify monzo.me transactions or simple bank transfers**

# ## Change label and change all values in column:
# 
# We're going to fix the +ve/-ve problem by 
# 1. New label called Spending that says whether it was out or in, True for out False for in.
# 2. Change all values to positive to make it easier to deal with
# 

# In[7]:


## Lets start by fixing the incoming/outgoing labels, and making all numbers +ve.  ##

currentColumnNames = (df.columns.values).tolist()
print(currentColumnNames)

if('local_amount' in currentColumnNames):
    currentColumnNames[currentColumnNames.index('local_amount')] = "Spending" # we'll call the new label spending

df.columns = currentColumnNames

df.loc[(df.amount < 0), 'Spending'] = True;
df.loc[(df.amount > 0 ), 'Spending'] = False;

df.head()

df.amount = abs(df.amount)

df


# # Try some graphics
# 
# Let's try and use some of this data for something useful, a good example is just to see what is the average money spent per day. 
# 
# ### Thinking:
# 
# There's definitely multiple transactions per day, which means we need to group them per day, luckily we have the data sorted under date-time. 
# 
# To group them we can make it easier by turning the date-time format into something easy for python to read, we can use the `datetime` library for this.
# 

# In[10]:


type(df.created.values)


# In[15]:


timeValues = df.created.values
timeValues = timeValues.tolist()
type(timeValues[0])


# In[18]:


def toUTC(x):
    dt = (x).encode('utf-8') # get datetime format
    dTime = (dt.split(" "))[1] # gets the time not the date.
    dt = (dt.split(" "))[0] # get only the date related (not time)
    dt = datetime.strptime(dt,'%Y-%m-%d') # Convert it to DateTime format
    
# df.created = df.created.apply(toUTC);

