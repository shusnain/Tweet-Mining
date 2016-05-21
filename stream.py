from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import auth as ath

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(ath.CONSUMER_KEY, ath.CONSUMER_SECRET)
    auth.set_access_token(ath.OAUTH_TOKEN, ath.OAUTH_TOKEN_SECRET)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#FACupFinal'])