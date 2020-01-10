#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from textblob import TextBlob
import seaborn as sns
import numpy as np
from numpy.random import randn
from numpy.random import seed
from numpy import cov
from scipy.stats import pearsonr
from collections import Counter


# In[29]:


ls


# In[30]:


df = pd.read_csv("Desktop/Project_2/USvideos.csv")


# In[31]:


df.head()


# In[32]:


df['description'] = df['description'].astype(str)


# In[33]:


df['description'][2]


# In[34]:


df['description'] = df['description'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['description'][2]


# In[35]:


df['description'] = df['description'].str.replace('\W',' ')
df['description'][2]


# In[36]:


stop = stopwords.words('english')
df['description'] = df['description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['description'][2]


# In[37]:


st = PorterStemmer()
df['description'] = df['description'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
df['description'][2]


# In[38]:


## Define a function which can be applied to calculate the score for the whole dataset

def getPol(x):
    return TextBlob(x).sentiment.polarity

def getSub(x):
    return TextBlob(x).sentiment.subjectivity

def getSent(x):
    if x == 0:
      return 'The text is neutral'
    elif x > 0:
      return 'The text is positive'
    else:
      return 'The text is negative'
    

df['senti_score_polarity'] = df['title'].apply(getPol)
df['senti_score_subjectivity'] = df['title'].apply(getSub)
df['sentiment'] = df['senti_score_polarity'].apply(getSent)
df.head()


# In[39]:


#boxplot for df

boxplot = df.boxplot(column=['senti_score_polarity','senti_score_subjectivity'], 
                     fontsize = 15,grid = True, vert=True,figsize=(7,7,))
plt.ylabel('Range')


# In[40]:


#scatter for df

sns.lmplot(x='senti_score_subjectivity',y='senti_score_polarity',data=df,fit_reg=True,scatter=True, height=7,palette="mute") 


# In[41]:


# prepare data
data1 = df['senti_score_subjectivity']
data2 = data1 + df['senti_score_polarity']
# calculate covariance matrix
covariance = cov(data1, data2) 
print(covariance)

corr, _ = pearsonr(data1, data2)
print('correlation: %.5f' % corr)


# In[42]:


#Polarity Distribution for dffilter

plt.hist(df['senti_score_polarity'], color = 'darkred', edgecolor = 'black', density=False,
         bins = int(30))
plt.title('Polarity Distribution')
plt.xlabel("Polarity")
plt.ylabel("Number of Times")

from pylab import rcParams
rcParams['figure.figsize'] = 10,15


# In[43]:


sns.distplot(df['senti_score_polarity'], hist=True, kde=True, 
             bins=int(30), color = 'darkred',
             hist_kws={'edgecolor':'black'},axlabel ='Polarity')
plt.title('Polarity Density')

from pylab import rcParams
rcParams['figure.figsize'] = 3,3


# In[44]:


alltitles = ""
for idx, row in df.iterrows():
    alltitles += row["title"] + " "


# In[45]:


split_alltitles = alltitles.split()


# In[46]:


len(split_alltitles)


# In[47]:


cntr_titles = Counter(split_alltitles)


# In[49]:


cntr_titles.most_common(25)


# In[50]:


# Data to plot
labels = 'Video', 'Trailer', 'How', '2018', 'Official', 'You', 'My'
sizes = [1901, 1868, 1661, 1613, 1594, 1254, 1080]
colors = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'skyblue']
explode = ((0.1, 0.12, 0.122, 0,0,0,0))  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()


# In[ ]:




