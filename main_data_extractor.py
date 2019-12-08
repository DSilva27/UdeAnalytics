#---------------------------------------------------------------
#
# Created by vlt-ro, Jumarulanda, DaviSS0397 and CH819
#---------------------------------------------------------------

# Libraries
import pandas as pd
import numpy as np
import json
import re
import tweepy
import datetime
import time
import utils.data_parser as dat_par
import utils.separate_sort as ss
from utils.data_parser import parse_from_txt as ptxt


if __name__ == "__main__":
    
    # 

    file = "data/twitter_data.txt"
    filters = '@QuinteroCalle'

    tweets_data = dat_par.parse_from_txt(file)
    
    tweets_C = ss.filterer(filters,tweets_data)        
    common_tweets, retweets = ss.separator(tweets_C)
    users = ss.get_first_users_layer(common_tweets, 0)
    
    # 
    file_following = "data/data_following.json"
    file_followers = "data/data_followers.json"

    infop = ss.add_follow_list(users,file_following,file_followers)
    infop = infop[infop.Following!=0] 
    #print(infop.index)

    # Metric

    d0to99    = np.squeeze(ptxt("data/tweets_0to99.json"))
    d100to199 = np.squeeze(ptxt("data/tweets_100to199.json"))
    d200to299 = np.squeeze(ptxt("data/tweets_200to299.json"))
    d300to399 = np.squeeze(ptxt("data/tweets_300to399.json"))
    d400toend = np.squeeze(ptxt("data/tweets_400toend.json"))

    data = [*d0to99, *d100to199, *d200to299, *d300to399, *d400toend]
    usr_id_scrn = pd.read_csv("data/user_id.csv", header = None)
    
    counter = ss.RT_REP_Counter(data, usr_id_scrn)
    
    RT = ss.interaction('RT',usr_id_scrn,counter)
    REP = ss.interaction('Rep',usr_id_scrn,counter)
    FF = ss.follower_following_count(infop)

    RT = ss.norm_symmetrize(RT)
    REP = ss.norm_symmetrize(REP)
    FF = ss.norm_symmetrize(FF)

    W1 = 0.25 
    W2 = 0.5
    W3 = 0.75
    EdgeW = RT*W1 + REP*W2 + FF*W3

    np.savetxt('data/EdgesW.csv',EdgeW)

    NodeWeight = ss.node_weight(usr_id_scrn,counter)

    np.savetxt('data/NodeW.csv',NodeWeight)