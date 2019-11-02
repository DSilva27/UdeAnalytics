import tweepy
import json
        
def api_auth(usr_id):
    ''' Function to authenticate id. Reads credentials from json file. '''
    with open("keysAndTokens.json","r") as rfile:
        
        data = json.load(rfile)
    
        for usr in data:
            if usr["user_id"] == usr_id:
                auth = tweepy.OAuthHandler(usr["API_key"], usr["API_secret_key"])
                auth.set_access_token(usr["acces_token"], usr["acces_token_secret"])
                
                api = tweepy.API(auth)

                return api

            else:
                raise ValueError("User ID not found.")


def get_credentials(usr_id):
    ''' Function to get dict with credentials from specified user id on json file '''
    with open("keysAndTokens.json","r") as rfile:
        
        data = json.load(rfile)

        for usr in data:
            if usr["user_id"] == usr_id:

                return usr
