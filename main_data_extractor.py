#---------------------------------------------------------------
#
# Created by vlt-ro, Jumarulanda, DaviSS0397 and CH819
#---------------------------------------------------------------

# Libraries
import sys
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
    
    # Get users that mention @QuinteroCalle

    file = "data/twitter_data.txt"
    filters = '@QuinteroCalle'

    tweets_data = dat_par.parse_from_txt(file)
    
    tweets_C = ss.filterer(filters,tweets_data)        
    common_tweets, retweets = ss.separator(tweets_C)
    users = ss.get_first_users_layer(common_tweets, 0)
    
    # Create a dataframe with the user's followers and following and eliminate private counts
    file_following = "data/data_following.json"
    file_followers = "data/data_followers.json"

    infop = ss.add_follow_list(users,file_following,file_followers)
    n_users = len(infop)
    infop = infop[infop.Following!=0] 

    # Create a metric based on users interaction

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


    clusters = pd.read_csv("data/node_segmentation.csv",sep=';' )
    groups = clusters.groupby('NODE_NUM')     

    f = open('data/estadistica.txt', 'w')

    print("----------------Estadistica general-------------",file=f)
    print("Numero de usuarios:",n_users,file=f)
    print("Numero de usuarios con cuentas no privadas:",len(infop),file=f)
    print("Numero de parejas de usuarios que se siguen entre si:",int(len(FF[FF==2])/2),file=f)
    print("Numero maximo de RT entre usuarios:",int(np.max(RT)),file=f)
    print("Numero maximo de Rep de un usuario a otro:",int(np.max(REP)),file=f)
    print("Promedio de RT entre usuarios:",int(np.mean(RT)),file=f)
    print("Promedio de Rep entre usuarios:",int(np.mean(REP)),file=f)
    print("Numero de clusters:",len(groups),file=f)
    print("Numero de clusters con mas de una persona:",len(groups.count().NODE_RANK[groups.count().NODE_RANK>1]),file=f)

    # Interactions analysis in each cluster
    for group in groups:
        if len(group[1])>1: 
            usr_id_scrn['bool'] = np.zeros(len(usr_id_scrn))

            for user in group[1]["SCREEN_NAME"]:
                 usr_id_scrn.loc[usr_id_scrn[0]==user,'bool'] = 1

            user_id = usr_id_scrn.groupby('bool').get_group(1.0)
            info_cluster = infop.loc[group[1]["SCREEN_NAME"]]

            
            counter_cluster = ss.RT_REP_Counter(data, user_id)

            RT = ss.interaction('RT',user_id,counter_cluster)
            REP = ss.interaction('Rep',user_id,counter_cluster)

            FF = ss.follower_following_count(info_cluster)
            
            print("----------------Estadistica Cluster %i-------------"%group[0],file=f)
            print("Numero de usuarios:",len(group[1]),file=f)
            print("Numero de parejas de usuarios que se siguen entre si:",int(len(FF[FF==2])/2),file=f)
            print("Numero maximo de RT entre usuarios:",int(np.max(RT)),file=f)
            print("Numero maximo de Rep de un usuario a otro:",int(np.max(REP)),file=f)
            print("Promedio de RT entre usuarios:",int(np.mean(RT)),file=f)
            print("Promedio de Rep entre usuarios:",int(np.mean(REP)),file=f)

f.close()
