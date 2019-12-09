#-------------------------------------------------------
# This file ....
# Created by Jumarulanda
#-------------------------------------------------------

import lib.layer_generator as lg
import lib.tp_auth as tp
import lib.data_parser as dp
# import pandas
import json

def save_json(json_list, name):
    with open("data/"+name+".json", "+w") as wfile:
        json.dump(json_list, wfile)


# set date interval of data recollection

date_0 = lg.set_date(2019,10,18,19,23,second=3)
date_f = lg.set_date(2019,10,19,14,8,second=2)

dates = (date_0, date_f)


# get users from the followers of Daniel Quintero

json_following = dp.parse_from_txt("../data/data_followers.json")
users = [json_dict["user_id"] for json_dict in json_following]


# set api
user = "username"
i = 0 #Initial Value
f = 100 #Final Value

try:
    api = tp.api_auth(user)
    lg.get_tweetOnDates(api,users[i:f],dates)
    
except NameError:
    print("You must define a user and/or the initial and final indices")

