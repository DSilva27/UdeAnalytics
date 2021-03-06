#------------------------------------------------
# 
# Created by vlt-ro, Jumarulanda, DaviSS0397 and CH819
#------------------------------------------------

import json
import pandas as pd


# Parse data from list of tweepy objects
def data_parser(obj_list):
    ''' 
    Extracts the dictionaries out of the tweepy json objects
    INPUT: obj_list: list of json objects
           
    OUTPUT: parsed_data: list of dictionaries, which can be used as usual
    '''
    
    # list to store the dictionaries
    parsed_data = []
    
    for obj in obj_list:
        #read each dictionary in the json as string
        json_str = json.dumps(obj._json)
        
        # load the dictionary
        parsed = json.loads(json_str)
        
        # append the dictionary to the data list
        parsed_data.append(parsed)
    
    return parsed_data


# Parse data from txt of tweepy objects 
def parse_from_txt(filename):
    ''' 
    INPUT: filename: path of txt or json file
           
    OUTPUT: parsed_data: list of dictionaries, which can be used as usual
    '''
    
    # open and read the json file in txt format 
    rfile = open(filename, 'r')
    
    # list to store the data
    parsed_data = []
    
    # iterate on each line of the read json file
    for line in rfile:
        try:
            # load the line string into a dictionary
            obj = json.loads(line)
            
            # append the dictionary to the data list
            parsed_data.append(obj)
        
        except:
            continue
    
    return parsed_data


# Convert parsed data to data frame with selected columns
# Nested dictionaries are not implemented
def data_to_df(parsed_data, dic):
    ''' 
    INPUT: parsed_data: list of dictionaries
           dic: dictionary with columns to be selected: {column name : attribute}
           
    OUTPUT: df: dataframe with selected columns
    '''
    
    df = pd.DataFrame(columns=list(dic.keys()))
    
    for column in df.columns:
        df[column] = list(map(lambda obj: obj[dic[column]], parsed_data))
    
    return df



