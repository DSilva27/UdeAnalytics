# CUFICO_proyecto_final

## Table of Contents

- [Main Repository](#main)
- [Data Mining](#mining)
- [How to use it](#use)
- [Credits](#credits)

<a name="main"></a>
## Main Repository
### main_data_extractor
Gathers all the information you have mined and creates a proximity matrix. It also creates two files EdgesW.csv and NodeW.csv, which can be used to create your .net file and visualize your network using [Infomap](#infomap).
    
<a name="mining"></a>    
## Data Mining

### save_data_follow

Prints dictionaries on a file with user ID, following and followers. Following are requested first, then followers. To use, run 'get_data_follow.sh'.

### streaming_data
Prints all the tweets and retweets that are tweeted from the moment you run the program. The tweets are filtered by           certain keywords.

<a name="use"></a>  
## How to use it

1) Open data/keysAndTokens.json and edit the file
2) Add a new dictionary with your credentials and set an username 

4) Run on_dates_data.py


## Credits

<a name="infomap"></a> 
### Infomap
https://www.mapequation.org/infomap/

### References
- Shaham. (2018, December 12). Generating A Twitter Ego-Network & Detecting Communities. Retrieved from https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255

- Moujahid, A. (2014, July 21). An Introduction to Text Mining using Twitter Streaming API and Python. Retrieved from http://adilmoujahid.com/posts/2014/07/twitter-analytics/

- Blondel, Vincent D et al. “Fast Unfolding of Communities in Large Networks.” Journal of Statistical Mechanics: Theory and    Experiment 2008.10 (2008): P10008. Crossref. Web.

- Bohlin, L., Edler, D., Lancichinetti, A., & Rosvall, M. (2014). Community detection and visualization of networks with the map equation framework. In Measuring Scholarly Impact (pp. 3-34). Springer, Cham.

