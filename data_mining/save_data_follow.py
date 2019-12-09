import numpy as np
import pandas as pd
import tweepy
import time

from lib import tp_auth as tp

"""

Prints dictionaries on a file with user ID, friends
and followers. Friends are requested first, then followers.

To use, run 'get_data_follow.sh'

"""

def save_data_follow(api, df):
    
    print('# --------- FOLLOWING ----------------')
    
    for i, user_id in enumerate(df.User_ID):
        
        try:
            follow = []
            for page in tweepy.Cursor(api.friends_ids, user_id=user_id).pages():
                follow.extend(page)
                
            print('{ \"user_id\":', user_id, ', \"following\":', follow, '}')
        
        except:
            follow = [0]
            
            print('{ \"user_id\":', user_id, ', \"following\":', follow, '}')
        
        if i%10 == 0:
            time.sleep(905)
    
    if i%10 == 0:
        time.sleep(905)
    
    print('# --------- FOLLOWERS ----------------')
    
    for i, user_id in enumerate(df.User_ID):
        
        try:
            follow = []
            for page in tweepy.Cursor(api.followers_ids, user_id=user_id).pages():
                follow.extend(page)
            
            print('{ \"user_id\":', user_id, ', \"followers\":', follow, '}')
        
        except:
            follow = [0]
            
            print('{ \"user_id\":', user_id, ', \"followers\":', follow, '}')
            
        if i%15 == 0:
                time.sleep(905)
    
    return


if __name__ == "__main__":
    
    id_list = pd.read_csv('../data/user_id.csv')
    
    api = tp.api_auth("CH212")
    
    save_data_follow(api, id_list)
    
