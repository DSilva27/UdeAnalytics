import tweepy
import datetime
import time
import lib.tp_auth as api_auth
import lib.data_parser as dat_par


def status_iter(statuses, user, dl_lim, dh_lim, n, dates):
    ''' 
    Iterates over the statuses (aka tweets) of an user, and saves the ones 
    between the desired dates (this is used by the get_tweetOnDates function)
    Returns the updated list of tweets and two bool values that indicate 
    whether the desired time interval has been reached 
    
    INPUT: statuses: a list of statuese of the user
        user: the user id
        dl_lim: (bool) tells if the lower limit of the date interval has been reached
        dh_lim: (bool) tells if the higher limit of the date interval has been reached
        n: iteration number
        dates: date interval tuple
    '''
    # tweet count
    tweet_count = 1
    
    # list to store data
    tweets, date = [],[]
    
    for status in statuses[10*n:10*(n+1)]:
        
        # Creation date of the status
        c_date  = status.created_at

        # if the creation date is higher than the upper limit, dh_lim is set to True
        if c_date < dates[1] and dh_lim == False:
            dh_lim = True
            
        # if the creation date is lower than the upper limit, dh_lim is set to True
        if c_date > dates[0] and dh_lim == True:
            dl_lim = True
        
        # when status is between the date limits, the data is stored
        if c_date > dates[0] and c_date < dates[1]:
            #print("Yey! Tweet count: {}".format(tweet_count))
            tweet_count += 1
            
            # append the tweet and the date of publication to the data lists
            tweets.append(status.text)
            date.append(str(c_date))
    
    # return the tweet, date data and the state of the dl_lim and dh_lim variables
    return tweets, date, dl_lim, dh_lim


def set_date(year, month, day, hour, minute, second=0, microsecond=0):
    ''' 
    Creates a datetime object. This allows to compare 
    the date of creation from the tweets '''
    
    # return the date on the datetime format
    return datetime.datetime(year,month,day,hour,minute,second,microsecond)


def get_tweetOnDates(api, users, dates):
    ''' 
    Gets the tweets from users over the pair of dates specified 
    in the "dates" list. Returns data frame with username, date of tweet,
    and tweet text per user
    
    INPUT: api: the api object from the tweepy API
           users: list of the id of the users
           dates: tuple of the date interval for the tweet search
    '''
    
    # list to store the data
    tweet_json = []
    
    usr_count = 0
    
    # iterate on the users to get the tweets between the dates
    for user in users:

        usr_count += 1

        # Cursor obeject to get the data from a user timeline
        cursor = tweepy.Cursor(api.user_timeline, user_id=user)

        # the bool variables below tell if the tweets are between the date interval of the search
        date_low_lim, date_high_lim = False, False

        n = 0
        
        try:
            statuses = list(cursor.items(20000))

        except tweepy.TweepError as error:
            # if the error is due to a timeout, wait 15 minutes to make the call again
            if str(error)[-3:] == "429":
                time.sleep(60*15)
                statuses = list(cursor.items(20000))
            
            # if the error is something else, ignore user and continue
            else:
                continue

        # list to store tweets and dates
        t_list, d_list = [],[]
        
        # makes the search dividing the statuses in groups of 10. Stops when date_low_lim and date_high_lim are both True
        while date_low_lim*date_high_lim == False and n < len(statuses)/10:
            
            # get tweets and dates from the status_iter() function
            t_list, d_list, date_low_lim, date_high_lim = status_iter(statuses, user, date_low_lim, date_high_lim, n, dates)
            n += 1

        # return list of the tweets of each user between the specified dates
        tweet_json.append({"user_id":user, "dates":d_list, "tweets":t_list})

    return tweet_json
