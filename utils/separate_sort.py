#------------------------------------------------
# This file.....
# Created by vlt-ro, Jumarulanda, DaviSS0397 and CH819
#------------------------------------------------

import pandas as pd
import re
import numpy as np
import json
from utils.data_parser import *

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


def separator(dataframe): # Separates tweets from retweets

    retweets = []
    common_tweets = []
    
    for user, tweet, user_id in zip(dataframe['user'], dataframe['text'], dataframe['user_id']):
        match = re.search(r'^\bRT\b', tweet)
        
        if match == None:
            common_tweets.append([user,tweet,user_id])
        
        else:
            retweets.append([user,tweet,user_id])

    return np.array(common_tweets), np.array(retweets) # Returns an array with tweet,user for each entry


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



# Adds columns for following and followers of all users
# Only works for this dataset
def add_follow_list(df,nfile1,nfile2):
    
    following = []
    followers = []
    
    data1 = parse_from_txt(nfile1)
    data2 = parse_from_txt(nfile2)

    for i, user_id in enumerate(df.User_ID):
        if (data1[i]['following']==[0]) or (data2[i]['followers']==[0]):

                following.append(0)
                followers.append(0)

        
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

def follower_following_count(infop):

    n_users = len(infop)
    
    metric = np.zeros((n_users,n_users))
    
    for i, user_id in enumerate(infop.User_ID):
    
        for following in infop.iloc[i].Following:

            try:
                row = np.where(infop.User_ID==following)[0][0]
            except IndexError: continue

            metric[i][row] += 1

        for follower in infop.iloc[i].Followers:

            try:
                row = np.where(infop.User_ID==follower)[0][0]
            except IndexError: continue

            metric[i][row] += 1

    for i in range(n_users):
        for j in range(n_users):
            if metric[i][j]<metric[j][i]:
                metric[i][j] = metric[j][i]

    if np.allclose(metric, metric.T) != True:
        print('Metric is not symmetric') 

    return metric


def RT_REP_Counter(s,users):
    '''
    INPUT: s: list contaning the timelines of our users
           users: dataframe containing id (0) and screen_name (1) of the users we're interested in
           
    OUTPUT: h: dictionary with the following architechture:
                { usr_id : { RT: { rt_usr: freq }, Rep: { Rep_usr: freq } } }
    '''
    
    s = np.squeeze(s) #squeezes the data if there are redudant dimensions
    h = {} 
    #Since we are only interested in the users that are part of the csv, I'll just skip the ones
    #that aren't of our interest
    for i in s:
        if i["user_id"] not in users[1].values: continue 
            
        d = {"RT": {}, "Qt": [], "Rep" : {},"NTweets":{},"DQTweets":0}
        
        d["NTweets"] = len(i["tweets"]) 
         
        for tweet in i["tweets"]:
            usrs = re.findall(r"@(\w+)", tweet)
            if "QuinteroCalle" in usrs:
                    d["DQTweets"] += 1
                    
            if "RT" in tweet:        
                #usr = re.findall(r"@(\w+)", tweet)[0] #We find all str that start with a @
                usr = usrs[0]
                    
                if usr not in users[0].values: continue
                    
                index = users[users[0] == usr].index[0]
                usr_id = str(users[1][index])
             
                if usr_id in d["RT"]:
                    d["RT"][usr_id] += 1

                else:
                    d["RT"][usr_id] = 1

            else:
                #usrs = re.findall(r"@(\w+)", tweet)
                          
                    
                for j in usrs:
                    if j not in users[0].values: continue
                        
                    index = users[users[0] == j].index[0]
                    usr_id = str(users[1][index])
                        
                    if usr_id in d["Rep"]:
                        d["Rep"][usr_id] += 1

                    else:
                        d["Rep"][usr_id] = 1

        h[i["user_id"]] = d
        
    return h

def interaction(typ,usr_id,counter):
    n_user = len(usr_id)    
    matrix = np.zeros((n_user,n_user))
    
    for i in range(n_user):

        a = usr_id[1][i]

        try:
            if bool(counter[a][typ]): 
                for b, value in counter[a][typ].items():
                    j = np.where(usr_id[1] == int(b))[0][0]
                    matrix[i][j] = int(value)

        except KeyError:continue
        
    return matrix

def norm_symmetrize(matrix):
    matrix = matrix/np.max(matrix)
    return (matrix+matrix.T)/2.

def node_weight(usr_id_scrn,counter):

    NodeWeight = np.ones(len(usr_id_scrn))*0.01
    for i,count in enumerate(counter):
        if (counter[count]['NTweets'] != 0 and counter[count]['DQTweets'] != 0):
            NodeWeight[i] = counter[count]['DQTweets']/counter[count]['NTweets']
    return NodeWeight