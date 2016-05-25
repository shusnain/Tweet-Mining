import json
from csv import writer
import pandas as pd
import tweets_sentiment
import sys
import global_var as gv

def classify_teams(texts, team1, team2):
	team = []
	for text in texts:
		text = text.lower()
		if (any(s in text for s in team1) and any(s in text for s in team2)):
			team.append(3)
		elif any(s in text for s in team1):
			team.append(1)
		elif any(s in text for s in team2):
			team.append(2)
		else:
			team.append(0)
	return team

args = sys.argv

tweets = []

for line in open(gv.data_path + args[1]):
  try: 
    tweets.append(json.loads(line))
  except:
    pass

ids = [tweet['id_str'] for tweet in tweets if 'id_str' in tweet]
langs = [tweet['lang'] for tweet in tweets if 'lang' in tweet]
texts = [tweet['text'] for tweet in tweets if 'text' in tweet]
timestamps = [tweet['timestamp_ms'] for tweet in tweets if 'timestamp_ms' in tweet]
times = [tweet['created_at'] for tweet in tweets if 'created_at' in tweet]
retweets = [tweet['retweet_count'] for tweet in tweets if 'retweet_count' in tweet]

# user-specific
screen_names = [tweet['user']['screen_name'] for tweet in tweets if 'user' in tweet]
names = [tweet['user']['name'] for tweet in tweets if 'user' in tweet]

out = open(gv.data_path + args[2], 'w', newline='')

rows = zip(ids, langs, texts, timestamps, times, retweets, screen_names, names)

csv = writer(out)
csv.writerow(['id', 'lang', 'text', 'timestamp_ms', 'created_at', 'retweet_count', 'screen_name', 'name'])
for row in rows:
	values = [(value.encode('unicode_escape') if hasattr(value, 'encode') else value) for value in row]
	csv.writerow(values)

out.close()

# remove 'b need to fix!! inefficient!!
df = pd.read_csv(gv.data_path + args[2])
ids = [tweet[2:-1] for tweet in df['id']]
langs = [tweet[2:-1] for tweet in df['lang']]
texts = [tweet[2:-1] for tweet in df['text']]
timestamps = [tweet[2:-1] for tweet in df['timestamp_ms']]
times = [tweet[2:-1] for tweet in df['created_at']]
screen_names = [tweet[2:-1] for tweet in df['screen_name']]
names = [tweet[2:-1] for tweet in df['name']]
sentiment = tweets_sentiment.nltk_sentiment(texts)

# teams mentioned in each tweet
t1 = ['okc', 'thunder']
t1_h = ['#'+s for s in t1]
team1 = t1 + t1_h

t2 = ['gsw', 'warriors']
t2_h = ['#'+s for s in t2]
team2 = t2 + t2_h

teams_mentioned = classify_teams(texts, team1, team2)

out = open(gv.data_path + args[2], 'w', newline='')

rows = zip(ids, langs, texts, timestamps, times, retweets, screen_names, names, teams_mentioned, sentiment)

csv = writer(out)
csv.writerow(['id', 'lang', 'text', 'timestamp_ms', 'created_at', 'retweet_count', 'screen_name', 'name', 'teams_mentioned', 'sentiment'])
for row in rows:
	values = [value for value in row]
	csv.writerow(values)

out.close()

