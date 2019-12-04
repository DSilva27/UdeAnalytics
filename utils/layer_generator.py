
'''
Tareas 1 y 2
'''
#DavidSS0397 imports
import pandas as pd
import re
import numpy as np
import json

'''jumarulanda imports'''

import tweepy
import datetime
import time

if __name__ == "__main__":
    ''' to import modules on a code outside of utils/ while importing this module '''
    import data_parser as dat_par
    from tp_auth import api_auth
else:
    from utils import data_parser as dat_par
    from utils import tp_auth as api_auth


import networkx as nx
import matplotlib.pyplot as plt

from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

#Creating a DataFrame with tweet and user"
def filterer(filter,data):
    df= pd.DataFrame()
    df['text'] = list(map(lambda tweet: tweet['text'], data))
    df['user'] = list(map(lambda tweet: tweet['user']['screen_name'], data))
    df['user_id'] = list(map(lambda tweet: tweet['user']['id'], data))
    df = df[df['text'].apply(lambda tweet: word_in_text(filter, tweet))]

    return df #Returns a dataframe which contains only the desired information (user and tweet) 


def separator(dataframe): #Separates tweets from retweets

    retweets = []
    common_tweets = []
    
    for user, tweet, user_id in zip(dataframe['user'], dataframe['text'], dataframe['user_id']):
        match = re.search(r'^\bRT\b', tweet)
        
        if match == None:
            common_tweets.append([user,tweet,user_id])
        
        else:
            retweets.append([user,tweet,user_id])

    return np.array(common_tweets), np.array(retweets) #Returns an array with tweet,user for each entry


def get_first_users_layer(array, metric_cut):
    dataframe = pd.DataFrame(array, columns = ["User","Tweet","User_ID"])
    
    # return dataframe.groupby("User").size().sort_values(ascending = False).head()
    
    ''' jumarulanda '''

    ''' Now each user has it's metric calculated with respect to the centroid
     (tweets_by_user/num_of_tweets). Only users with metric above metric_cut are selected '''
    
    n_tweets = array.shape[0]
    
    agg = {'User_ID':'first', 'Tweet':lambda x: x.count()/n_tweets}
    
    user_group = dataframe.groupby("User").agg(agg).sort_values(by='Tweet', ascending = False)
    #user_group = dataframe.groupby("User").size().sort_values(ascending = False)/n_tweets
    
    sel_users = user_group[user_group.Tweet > metric_cut]
    #sel_users = user_group.loc[user_group > metric_cut]
    
    return sel_users
    #return sel_users.index.values, sel_users


'''
Tareas 3 y 4
'''

def set_date(year,month,day,hour,minute,second=0,microsecond=0):
    ''' Creates a datetime object. This allows to compare 
        the date of creation from the tweets '''
    return datetime.datetime(year,month,day,hour,minute,second,microsecond)


def status_iter(statuses, user, dl_lim, dh_lim, n, dates):
    ''' Iterates over the statuses (aka tweets) of an user, and saves the ones 
        between the desired dates (this is used by the get_tweetOnDates function). 
        Returns the updated list of the tweets, and two bool values that indicate 
        whether the desired time interval has been reached '''

    tweet_count = 1
    tweets, date = [],[]
    
    for status in statuses[10*n:10*(n+1)]:

        c_date  = status.created_at

        if c_date < dates[1] and dh_lim == False:
            dh_lim = True
            
        if c_date > dates[0] and dh_lim == True:
            dl_lim = True
        
        if c_date > dates[0] and c_date < dates[1]:
            print("Yey! Tweet count: {}".format(tweet_count))
            tweet_count += 1
            tweets.append(status.text)
            date.append(str(c_date))

    return tweets, date, dl_lim, dh_lim


def get_tweetOnDates(api, users, dates):
    ''' Gets the tweets from users over the pair of dates specified 
        in the "dates" list. Returns data frame with username, date of tweet,
        and tweet text per user'''
    
    tweet_json = []
    
    usr_count = 0
    
    for user in users:

        print("User count: {}".format(usr_count))
        usr_count += 1

        cursor = tweepy.Cursor(api.user_timeline, user_id=user)

        date_low_lim, date_high_lim = False, False

        n = 0
        
        try:
            statuses = list(cursor.items(10000))

        except tweepy.TweepError as error:
            if str(error)[-3:] == "401":
                continue
            else:
                time.sleep(60*15)
                statuses = list(cursor.items(10000))

        t_list, d_list = [],[]
            
        while date_low_lim*date_high_lim == False and n < len(statuses)/10:
        
            t_list, d_list, date_low_lim, date_high_lim = status_iter(statuses, user, date_low_lim, date_high_lim, n, dates)
            n += 1

        tweet_json.append({"user_id":user, "dates":d_list, "tweets":t_list})
            
    return tweet_json


def main(file = "../ejemplo_api/twitter_data.txt", filters = '@QuinteroCalle'):

    tweets_data = dat_par.parse_from_txt(file)
    tweets_C = filterer(filters,tweets_data)        
    common_tweets, retweets = separator(tweets_C)
    users = get_first_users_layer(common_tweets, 0)

    return users


# Adds columns for following and followers of all users
# Only works for this dataset
def add_follow_list(df):
    
    following = []
    followers = []
    
    nfile1 = "../data/data_following.json"
    data1 = dat_par.parse_from_txt(nfile1)

    nfile2 = "../data/data_followers.json"
    data2 = dat_par.parse_from_txt(nfile2)

    for i, user_id in enumerate(df.User_ID):
        if (data1[i]['following']==[0]) or (data2[i]['followers']==[0]):

                following.append(0)
        #if (data2[i]['followers']==[0]):
                followers.append(0)
                #print(i)


        
        else:
	        user_following = set(data1[i]['following'])
	        user_following = set(map(str, user_following))
	        following_intersec = user_following.intersection(set(df.User_ID))
	        
	        user_followers = set(data2[i]['followers'])
	        user_followers = set(map(str, user_followers))
	        follower_intersec = user_followers.intersection(set(df.User_ID))
	        
	        following.append(list(following_intersec))
	        followers.append(list(follower_intersec))


    df['Following'] = following
    df['Followers'] = followers
    
    return df

def metric_(infop):

    n_users = len(infop)
    infop['order'] = np.arange(0,n_users,1)
    
    metric = np.zeros((n_users,n_users))
    
    for i, user_id in enumerate(infop.User_ID):
    
        for following in infop.iloc[i].Following:
            row = infop[infop.User_ID==following].order
            metric[i][row] += 1
        for follower in infop.iloc[i].Followers:
            row = infop[infop.User_ID==follower].order
            metric[i][row] += 1

    #distance = pairwise_distances(metric,metric="euclidean")
    
    for i in range(n_users):
        for j in range(n_users):
            if metric[i][j]<metric[j][i]:
            	metric[i][j] = metric[j][i]

    if np.allclose(metric, metric.T) != True:
        print('Metric is not symmetric') 
    
    plt.imshow(metric)
    plt.show()

    return True

if __name__ == "__main__":
    
    info = main()
    
    infop = add_follow_list(info)

    infop = infop[infop.Following!=0] #

    metric_(infop)
    
    
    #add_follow_list(info)
    
    # tweet_data = dat_par.parse_from_txt("./tweets.txt")
    # filters = "pewdiepie"
    # tweet_c = filterer(filters, tweet_data)
    # common_tweets, retweets = separator(tweet_c)
    # users, users_sorted = get_first_users_layer(common_tweets,0.04)

    # api = tp_auth.api_auth("juanpa")

    # dates = [set_date(2019,10,27,0,0), set_date(2019,10,30,0,0)]
    
    # tweets = get_tweetOnDates(api, users, dates) 
    
    # print(tweets)
