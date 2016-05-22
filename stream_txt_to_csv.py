import json
from csv import writer
import pandas as pd
import sys

args = sys.argv

tweets = []

for line in open(args[1]):
  try: 
    tweets.append(json.loads(line))
  except:
    pass

ids = [tweet['id_str'] for tweet in tweets]
langs = [tweet['lang'] for tweet in tweets]
texts = [tweet['text'] for tweet in tweets]
timestamps = [tweet['timestamp_ms'] for tweet in tweets]
times = [tweet['created_at'] for tweet in tweets]
retweets = [tweet['retweet_count'] for tweet in tweets]

# user-specific
screen_names = [tweet['user']['screen_name'] for tweet in tweets]
names = [tweet['user']['name'] for tweet in tweets]

out = open(args[2], 'w', newline='')

rows = zip(ids, langs, texts, timestamps, times, retweets, screen_names, names)

csv = writer(out)
csv.writerow(['id', 'lang', 'text', 'timestamp_ms', 'created_at', 'retweet_count', 'screen_name', 'name'])
for row in rows:
	values = [(value.encode('unicode_escape') if hasattr(value, 'encode') else value) for value in row]
	csv.writerow(values)

out.close()

# remove 'b need to fix!! inefficient!!
df = pd.read_csv(args[2])
ids = [i[2:-1] for i in df['id']]
langs = [i[2:-1] for i in df['lang']]
texts = [i[2:-1] for i in df['text']]
timestamps = [i[2:-1] for i in df['timestamp_ms']]
times = [i[2:-1] for i in df['created_at']]
screen_names = [i[2:-1] for i in df['screen_name']]
names = [i[2:-1] for i in df['name']]

out = open(args[2], 'w', newline='')

rows = zip(ids, langs, texts, timestamps, times, retweets, screen_names, names)

csv = writer(out)
csv.writerow(['id', 'lang', 'text', 'timestamp_ms', 'created_at', 'retweet_count', 'screen_name', 'name'])
for row in rows:
	values = [value for value in row]
	csv.writerow(values)

out.close()

