#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import csv
from tweepy import OAuthHandler
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import random
import re
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Consumer keys and access tokens, used for OAuth
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('muslim_hashtag.csv', 'w', encoding='utf-8')
#Use csv Writer
 
HEADER = ["screen_name","location", "language", "text", "created_at", "retweet_count", "likes_count"]
csvWriter = csv.writer(csvFile)
csvWriter.writerow(HEADER)

#request the keyword as an input
a=input("Enter your keyword to start the search: ")
count=input("Enter number of tweets to start the search: ")
#search for a hashtag/keyword and write to the CSV file
for tweet in tweepy.Cursor(api.search,q=str.lower(a),
                           since="2020-03-01", wait_on_rate_limit=True,).items(int(count)):
    #print (tweet.user.screen_name, tweet.user.location, tweet.lang, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count)
    csvWriter.writerow([tweet.user.screen_name, tweet.user.location, tweet.lang, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count])



# ### Make a bar plot from the most frequent languages of the tweets

# In[2]:


#Create a scatter chart with languages
df=pd.read_csv("muslim_hashtag.csv", encoding='utf-8')
freq=df["language"].value_counts()[df["language"].value_counts()>3]

# Get a color map
my_cmap = cm.get_cmap('jet')
# Get normalize function (takes data in range [vmin, vmax] -> [0, 1])
my_norm = Normalize(vmin=0, vmax=8)
#make a bar plot
color=[i for i in range(0, 10)]
freq.plot.bar(color=my_cmap(my_norm(color)), alpha=0.5)
#add the value of each one
for index, value in enumerate(freq):
	plt.text(index, value,  str(value))
plt.ylabel("Number")
plt.xlabel("Language")
plt.title("Tweets Language")
plt.savefig('tweets_lang.pdf', dpi=100)
plt.show()


# ### Show the frequency of location and save it 

# In[3]:


#Create a bar chart with languages
df=pd.read_csv("muslim_hashtag.csv")
freq=df["location"].value_counts()
freq.dropna()
common_freq=df["location"].value_counts()[df["location"].value_counts()>3]
print(common_freq)
freq.to_csv('tweets_location.csv', encoding='utf-8', header=True)


# ### Extract hashtags from English tweets

# In[4]:


#only english text column
df=pd.read_csv("muslim_hashtag.csv")
df_text=df[df.language=="en"][["text"]]
df_text["text"]=df_text["text"].str.lower().str.replace("https:.*","")
hashtag=[]
for line in df_text["text"]:
    x=re.findall(r"#(\w+)", line, re.UNICODE)
    if x!=[]:
        for item in x:
            hashtag.append(item)
word_could_dict=Counter(hashtag)
print(word_could_dict)
df_hashtag = pd.DataFrame(hashtag) 


# ### Create a Wordcloud from the frequency of the hashtags

# In[5]:


wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)

plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('tweets_wordcloud.pdf', dpi=100)
plt.show()


# ### Create a bar chart with most frequent users who tweeted

# In[6]:


users=df["screen_name"]
freq=df["screen_name"].value_counts()[df["screen_name"].value_counts()>3]
my_cmap = cm.get_cmap('jet')
# Get normalize function (takes data in range [vmin, vmax] -> [0, 1])
my_norm = Normalize(vmin=0, vmax=8)
#make a bar plot
freq.plot.bar(color=my_cmap(my_norm(color)), alpha=0.5)
for index, value in enumerate(freq):
	plt.text(index, value,  str(value))
plt.ylabel("Number")
plt.xlabel("Screen_Name")
plt.title("Tweets Screen_Name")
plt.savefig('tweets_screen_name.pdf', dpi=100)
plt.show()


# ### Check those users with botometer (Work in Progress)
