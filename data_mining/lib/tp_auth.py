import tweepy
import json
        
def api_auth(usr_id):
    ''' Function to authenticate id. Reads credentials from json file. '''

    try:
<<<<<<< HEAD:data_mining/lib/tp_auth.py
        with open("../data/keysAndTokens.json","r") as rfile:
=======
        with open("keysAndTokens.json","r") as rfile:
>>>>>>> c048a71e359ecf4bf1668be3778bb18c8367a245:utils/tp_auth.py
        
            data = json.load(rfile)
            
            usr_found = False
            for usr in data:
                if usr["user_id"] == usr_id:
                    auth = tweepy.OAuthHandler(usr["API_key"], usr["API_secret_key"])
                    auth.set_access_token(usr["acces_token"], usr["acces_token_secret"])
                
                    api = tweepy.API(auth)
                        
                    usr_found = True
            
                    return api
              
            if not usr_found:
                raise ValueError("User ID not found.")

    except FileNotFoundError:
         with open("../data/keysAndTokens.json","r") as rfile:
        
            data = json.load(rfile)
            
            usr_found = False
            for usr in data:
                if usr["user_id"] == usr_id:
                    auth = tweepy.OAuthHandler(usr["API_key"], usr["API_secret_key"])
                    auth.set_access_token(usr["acces_token"], usr["acces_token_secret"])
                
                    api = tweepy.API(auth)

                    usr_found = True 

                    return api
            if not usr_found:
                raise ValueError("User ID not found.")


def get_credentials(usr_id):
    ''' Function to get dict with credentials from specified user id on json file '''
    with open("keysAndTokens.json","r") as rfile:
        
        data = json.load(rfile)

        for usr in data:
            if usr["user_id"] == usr_id:

                return usr
