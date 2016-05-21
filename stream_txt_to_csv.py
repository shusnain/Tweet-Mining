import json
from csv import writer

tweets = []

for line in open('stream.txt'):
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

out = open('tweets.csv', 'w', newline='')

rows = zip(ids, langs, texts, timestamps, times, retweets, screen_names, names)

csv = writer(out)
csv.writerow(['id', 'lang', 'text', 'timestamp_ms', 'created_at', 'retweet_count', 'screen_name', 'name'])
for row in rows:
	values = [(value.encode('utf-8') if hasattr(value, 'encode') else value) for value in row]
	csv.writerow(values)

out.close()