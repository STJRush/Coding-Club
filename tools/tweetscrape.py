import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:drg1985').get_items()):
    if i>0:
        break
    tweets_list1.append([tweet.content])
    print(tweets_list1)