import json
import pandas as pd


" Parse data from list of tweepy objects "
def data_parser(obj_list):
    
    parsed_data = []
    
    for obj in obj_list:
        json_str = json.dumps(obj._json)
        parsed = json.loads(json_str)
        parsed_data.append(parsed)
    
    return parsed_data


" Parse data from txt of tweepy objects "
def parse_from_txt(filename):
    
    rfile = open(filename, 'r')
    
    parsed_data = []
    for line in rfile:
        try:
            obj = json.loads(line)
            parsed_data.append(obj)
        
        except:
            continue
    
    return parsed_data


" Convert parsed data to data frame with selected columns"
" Must fix for nested dictionaries "
def data_to_df(parsed_data, dic):
    # dic: dictionary {column name : attribute}
    
    df = pd.DataFrame(columns=list(dic.keys()))
    
    for column in df.columns:
        df[column] = list(map(lambda obj: obj[dic[column]], parsed_data))
    
    return df



