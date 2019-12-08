import tweepy
import datetime
import time
import lib.tp_auth as api_auth
import lib.data_parser as dat_par

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
            #print("Yey! Tweet count: {}".format(tweet_count))
            tweet_count += 1
            tweets.append(status.text)
            date.append(str(c_date))

    return tweets, date, dl_lim, dh_lim

def set_date(year,month,day,hour,minute,second=0,microsecond=0):
    ''' Creates a datetime object. This allows to compare 
        the date of creation from the tweets '''
    return datetime.datetime(year,month,day,hour,minute,second,microsecond)


def get_tweetOnDates(api, users, dates):
    ''' Gets the tweets from users over the pair of dates specified 
        in the "dates" list. Returns data frame with username, date of tweet,
        and tweet text per user'''
    
    tweet_json = []
    
    usr_count = 0
    
    print('[')
    
    for user in users:

        #print("User count: {}".format(usr_count))
        usr_count += 1

        cursor = tweepy.Cursor(api.user_timeline, user_id=user)

        date_low_lim, date_high_lim = False, False

        n = 0
        
        try:
            statuses = list(cursor.items(20000))

        except tweepy.TweepError as error:
            if str(error)[-3:] == "401":
                continue
            
            else:
                time.sleep(60*15)
                statuses = list(cursor.items(20000))

        t_list, d_list = [],[]
            
        while date_low_lim*date_high_lim == False and n < len(statuses)/10:
        
            t_list, d_list, date_low_lim, date_high_lim = status_iter(statuses, user, date_low_lim, date_high_lim, n, dates)
            n += 1

        #tweet_json.append({"user_id":user, "dates":d_list, "tweets":t_list})
        print('{"user_id\":', user, '\"dates\":', d_list, '\"tweets\":', t_list, '}')
            
    print(']')
    return #tweet_json