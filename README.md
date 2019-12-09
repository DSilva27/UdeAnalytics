# CUFICO_proyecto_final

## Table of Contents

- [Main Repository](main%repository)
- [Data Mining](data%mining)
- [Credit](credit)

## Main Repository
### main_data_extractor
    DESCRIPCIÓN
    
## Data Mining
### get_data_follow.sh

### save_data_follow

### streaming_data

## Adding your credentials and getting data

1) Open utils/keysAndTokens.json and edit the file
2) Add a new dictionary with your credentials and set an username
3) Configure on_dates_data_gen.py by changing the user and the intervals which are assigned to you.
    - JP: 0-99
    - DSS: 100-199
    - Vadd: 200-299
    - CH212: 300-399
    
4) Run on_dates_data.py


## Equation used for redefining the metric

EdgeWa&b = (W1&#215;RT_ab) + (W2&#215;Qtd_ab) + (W3&#215;Rep_ab) + i&#215;W4; i = 0, 1, 2

Node_a = tweets_Daniel / #Tweets_total

# Infomap
https://www.mapequation.org/infomap/


## Credits

Ideas were taken from the following sources:
(esto luego lo cuadramos)
https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255
