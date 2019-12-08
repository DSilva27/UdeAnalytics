#---------------------------------------------------------
# This file ...
# To save the data ... e.e
# Created by DaviSS0397
#---------------------------------------------------------

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API 
access_token = "1085741390527692800-v73KoVugFbFTXOu3dkIIxqIYeVLnkt"
access_token_secret = "63mbPu6TZtE9gfsduUk546Va1ouV1PHfhH43pqPDRdRXj"
consumer_key = "gMnJKIu3seBg2ddk6khg49V5w"
consumer_secret = "ST42Rjo0d6MBqJYL2Wbba0o3sSdByN1Ds1D2F0tYoiZN5v1Nrx"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['DanielQuinteroAlcalde','@QuinteroCalle','#QuinteroPorMedellín', 'MedellínAdelante', '@AlfredoRamosM',"#VamosPorMás"])