#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


df = pd.read_csv("Desktop/Project_2/GBvideos.csv")


# In[3]:


df['description'] = df['description'].astype(str)


# In[4]:


df['description'][2]


# In[5]:


df['description'] = df['description'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['description'][2]


# In[6]:


df['description'] = df['description'].str.replace('\W',' ')
df['description'][2]


# In[7]:


stop = stopwords.words('english')
df['description'] = df['description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['description'][2]


# In[8]:


st = PorterStemmer()
df['description'] = df['description'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
df['description'][2]


# In[9]:


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
    

df['senti_score_polarity'] = df['description'].apply(getPol)
df['senti_score_subjectivity'] = df['description'].apply(getSub)
df['sentiment'] = df['senti_score_polarity'].apply(getSent)
df.head()


# In[10]:


#boxplot for df

boxplot = df.boxplot(column=['senti_score_polarity','senti_score_subjectivity'], 
                     fontsize = 15,grid = True, vert=True,figsize=(7,7,))
plt.ylabel('Range')


# In[11]:


# prepare data
data1 = df['senti_score_subjectivity']
data2 = data1 + df['senti_score_polarity']
# calculate covariance matrix
covariance = cov(data1, data2) 
print(covariance)

corr, _ = pearsonr(data1, data2)
print('correlation: %.5f' % corr)


# In[12]:


#Polarity Distribution for dffilter

plt.hist(df['senti_score_polarity'], color = 'darkred', edgecolor = 'black', density=False,
         bins = int(30))
plt.title('Polarity Distribution')
plt.xlabel("Polarity")
plt.ylabel("Number of Times")

from pylab import rcParams
rcParams['figure.figsize'] = 10,15


# In[13]:


#words = df['title']
#
## generate DF out of Counter
#rslt = pd.DataFrame(Counter(words).most_common(10),
#                    columns=['Word', 'Frequency']).set_index('Word')
#rslt
alltitles = ""
for idx, row in df.iterrows():
    alltitles += row["title"] + " "


# In[14]:


split_alltitles = alltitles.split()


# In[15]:


cntr_titles = Counter(split_alltitles)


# In[16]:


cntr_titles.most_common(25)


# In[19]:


# Data to plot
labels = 'Video', 'Official', 'Trailer', 'Music', '2018', 'Me', 'My'
sizes = [3757, 3526, 2394, 1659, 1343, 1092, 1000]
colors = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'skyblue']
explode = ((0.1, 0.12, 0.122, 0,0,0,0))  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()


# In[ ]:




