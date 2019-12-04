from utils import layer_generator as lg
from utils import tp_auth as tp
from utils import data_parser as dp
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

json_following = dp.parse_from_txt("data/data_followers.json")
users = [json_dict["user_id"] for json_dict in json_following]


# set api


api = tp.api_auth("ramon")

lg.get_tweetOnDates(api,users[100:200],dates)
#tweets.to_json("data/tweets_100to199.json")

