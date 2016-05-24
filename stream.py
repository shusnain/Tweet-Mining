from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import global_var as gv

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(gv.twitter_consumer_key, gv.twitter_consumer_secret)
    auth.set_access_token(gv.twitter_oauth_token, gv.twitter_oauth_token_secret)
    stream = Stream(auth, l)

    q1 = ['OKC', 'GSW', 'Thunder', 'Warriors', 'OKCvsGSW', 'GSWvsOKC']
    q2 = ['#'+s for s in q1]
    query = q1 + q2
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=query)