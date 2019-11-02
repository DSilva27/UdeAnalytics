'''
Tareas 1 y 2
'''

import pandas as pd
import re
import numpy as np
import json
from data_parser import *

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

def separator(dataframe):

    retweets = []
    common_tweets = []
    
    for user, tweet in zip(dataframe['user'], dataframe['text']):
        match = re.search(r'^\bRT\b', tweet)
        
        if match == None:
            common_tweets.append([user,tweet])
        
        else:
            retweets.append([user,tweet])

    return np.array(common_tweets), np.array(retweets)


#Creating a DataFrame with tweet and user"
def filterer(filter,data):
    df= pd.DataFrame()
    df['text'] = list(map(lambda tweet: tweet['text'], data))
    df['user'] = list(map(lambda tweet: tweet['user']['screen_name'], data))
    df = df[df['text'].apply(lambda tweet: word_in_text(filter, tweet))]

    return df

def get_first_users_layer(array):
    dataframe = pd.DataFrame(array, columns = ["User","Tweet"])

    return dataframe.groupby("User").size().sort_values(ascending = False).head()



def main(file = "../ejemplo_api/twitter_data.txt", filters = '@QuinteroCalle'):

    tweets_data = parse_from_txt(file)
    tweets_C = filterer(filters,tweets_data)        
    common_tweets, retweets = separator(tweets_C)
    users = get_first_users_layer(common_tweets)

    return users


if __name__ == "__main__":
    print(main())
