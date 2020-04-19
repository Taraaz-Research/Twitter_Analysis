#!/usr/bin/env python
# coding: utf-8

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
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('muslim_hashtag.csv', 'w')
#Use csv Writer
 
HEADER = ["screen_name","location", "language", "text", "created_at", "retweet_count", "likes_count"]
csvWriter = csv.writer(csvFile)
csvWriter.writerow(HEADER)

#request the keyword as an input
a=input("Enter your keyword to start the search: ")
#search for a hashtag/keyword and write to the CSV file
for tweet in tweepy.Cursor(api.search,q=str.lower(a), count=10000,
                           since="2020-03-01", wait_on_rate_limit=True,).items(10000):
    #print (tweet.user.screen_name, tweet.user.location, tweet.lang, tweet.text, tweet.retweet_count, tweet.favorite_count)
    csvWriter.writerow([tweet.user.screen_name, tweet.user.location, tweet.lang, tweet.text.encode('utf-8'), tweet.retweet_count, tweet.favorite_count])



# ### Make a bar plot from the languages of the tweets

#Create a scatter chart with languages
df=pd.read_csv("muslim_hashtag.csv")
freq=df["language"].value_counts()
print(freq)
x=df["language"].unique()
color=[i for i in range(0, len(x))]
# Get a color map
my_cmap = cm.get_cmap('jet')
# Get normalize function (takes data in range [vmin, vmax] -> [0, 1])
my_norm = Normalize(vmin=0, vmax=8)
#make a scatter plot
plt.bar(x,freq, color=my_cmap(my_norm(color)), alpha=0.5)
#add the value of each one
for index, value in enumerate(freq):
	plt.text(index, value,  str(value))
plt.ylabel("Number")
plt.xlabel("Language")
plt.title("Tweets Language")
plt.savefig('tweets_lang.pdf', dpi=100)
plt.show()


# ### Show the frequency of location and save it 


#Create a bar chart with languages
df=pd.read_csv("muslim_hashtag.csv")
freq=df["location"]
freq.dropna()
freq=freq.value_counts()
print(freq)
x=df["location"].unique()
freq.to_csv('tweets_location.csv', encoding='utf-8', header=True)


# ### Extract hashtags from English tweets

#only english text column
df_text=df[df.language=="en"][["text"]]
df_text["text"]=df_text["text"].str.lower().str.replace("https:.*","")
hashtag=[]
for line in df_text["text"]:
    x=re.findall(r"#(\w+)", line)
    if x!=[]:
        for item in x:
            hashtag.append(item)
word_could_dict=Counter(hashtag)
print(word_could_dict)


# ### Create a Wordcloud from the frequency of the hashtags

wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)

plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('tweets_wordcloud.pdf', dpi=100)
plt.show()






