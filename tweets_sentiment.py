from nltk.sentiment.vader import SentimentIntensityAnalyzer

# reference: http://www.nltk.org/howto/sentiment.html
def nltk_sentiment(tweets):
	sentiment = []
	sid = SentimentIntensityAnalyzer()
	for tweet in tweets:
		st = sid.polarity_scores(tweet)
		sentiment.append(st['compound'])
	return sentiment