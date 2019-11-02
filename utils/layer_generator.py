'''
Tareas 1 y 2
'''

import pandas as pd
import re
import numpy as np
import json
import data_parser as dat_par

'''jumarulanda imports'''

import tweepy
from tp_auth import api_auth
import datetime

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

def get_first_users_layer(array, metric_cut):
    dataframe = pd.DataFrame(array, columns = ["User","Tweet"])

    # return dataframe.groupby("User").size().sort_values(ascending = False).head()
    
    ''' jumarulanda '''

    ''' Now each user has it's metric calculated with respecto to the centroid (tweets_by_user/num_of_tweets). Only users with metric above metric_cut are selected '''
    
    n_tweets = array.shape[0]
    user_group = dataframe.groupby("User").size().sort_values(ascending = False)/n_tweets

    sel_users = user_group.loc[user_group > metric_cut]
    
    return sel_users.index.values, sel_users  


'''
Tareas 3 y 4
'''

def set_date(year,month,day,hour,minute,second=0,microsecond=0):
    ''' Creates a datetime object. This allows to compare 
        the date of creation from the tweets '''
    return datetime.datetime(year,month,day,hour,minute,second=0,microsecond=0)



def status_iter(statuses, user, tweets, dl_lim, dh_lim, n, dates):
    ''' Iterates over the statuses (aka tweets) of an user, and saves the ones 
        between the desired dates (this is used by the get_tweetOnDates function). 
        Returns the updated list of the tweets, and two bool values that indicate 
        whether the desired time interval has beeb reached '''
    
    for status in statuses[10*n:10*(n+1)]:

        c_date  = status.created_at

        if c_date < dates[1] and dh_lim == False:
            dh_lim = True
            
        if c_date > dates[0] and dh_lim == True:
            dl_lim = True
        
        if c_date > dates[0] and c_date < dates[1]:
            tweets = tweets.append({"user":user, "date":c_date, "text":status.text}, ignore_index = True)

    return tweets, dl_lim, dh_lim

def get_tweetOnDates(api, users, dates):
    ''' Gets the tweets from users over the pair of dates specified 
        in the "dates" list. Returns data frame with username, date of tweet,
        and tweet text per user'''
    
    tweets = pd.DataFrame(columns=["user","date","text"])

    for user in users:

        time_line = api.user_timeline(user)

        cursor = tweepy.Cursor(api.user_timeline, screen_name = user)

        date_low_lim, date_high_lim = False, False

        n = 0

        statuses = list(cursor.items(1000))
                
        while date_low_lim*date_high_lim == False and n < len(statuses)/10:
        
            tweets, date_low_lim, date_high_lim = status_iter(statuses, user, tweets, date_low_lim, date_high_lim, n, dates)
            n += 1
            
    return tweets
            


def main():

    tweets_data = parse_from_txt("../ejemplo_api/twitter_data.txt")
    filters = '@QuinteroCalle'
    tweets_C = filterer(filters,tweets_data)        
    common_tweets, retweets = separator(tweets_C)
    users = get_first_users_layer(common_tweets)

    return users


if __name__ == "__main__":

    print(main())
    
    # tweet_data = dat_par.parse_from_txt("./tweets.txt")
    # filters = "pewdiepie"
    # tweet_c = filterer(filters, tweet_data)
    # common_tweets, retweets = separator(tweet_c)
    # users, users_sorted = get_first_users_layer(common_tweets,0.04)

    # api = api_auth("juanpa")

    # dates = [set_date(2019,10,27,0,0), set_date(2019,10,30,0,0)]
    
    # tweets = get_tweetOnDates(api, users, dates) 
    
    # print(tweets)
