import vincent
import pandas as pd
import sys
import global_var as gv

# source: https://marcobonzanini.com/2015/04/01/mining-twitter-data-with-python-part-5-data-visualisation-basics/
args = sys.argv

df = pd.read_csv(gv.data_path + args[1])
df.created_at = pd.DatetimeIndex(df.created_at).tz_localize('UTC').tz_convert('US/Eastern')

dates_all = df.created_at
dates_0 = df.created_at[df.teams_mentioned == 0]
dates_1 = df.created_at[df.teams_mentioned == 1]
dates_2 = df.created_at[df.teams_mentioned == 2]
dates_3 = df.created_at[df.teams_mentioned == 3]

ones_all = [1]*len(dates_all)
ones_0 = [1]*len(dates_0)
ones_1 = [1]*len(dates_1)
ones_2 = [1]*len(dates_2)
ones_3 = [1]*len(dates_3)

#zeros = [0]*len(dates_all)

idx_all = pd.DatetimeIndex(dates_all)
idx_0 = pd.DatetimeIndex(dates_0)
idx_1 = pd.DatetimeIndex(dates_1)
idx_2 = pd.DatetimeIndex(dates_2)
idx_3 = pd.DatetimeIndex(dates_3)

tweets_all = pd.Series(ones_all, index=idx_all)
tweets_0 = pd.Series(ones_0, index=idx_0)
tweets_1 = pd.Series(ones_1, index=idx_1)
tweets_2 = pd.Series(ones_2, index=idx_2)
tweets_3 = pd.Series(ones_3, index=idx_3)

per_minute_all = tweets_all.resample('1min').sum().fillna(0)
per_minute_0 = tweets_0.resample('1min').sum().fillna(0)
per_minute_1 = tweets_1.resample('1min').sum().fillna(0)
per_minute_2 = tweets_2.resample('1min').sum().fillna(0)
per_minute_3 = tweets_3.resample('1min').sum().fillna(0)

result = pd.concat([per_minute_all, per_minute_0, per_minute_1, per_minute_2, per_minute_3], axis = 1)
result.columns = ['All', 'Neither', 'Raps Only', 'Cavs Only', 'Both']

#chart 1
time_chart = vincent.Line(result)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='Legend')
time_chart.to_json(gv.data_path + 'time_chart.json')

sentiment_all = df.sentiment.values.tolist()
sentiment_0 = df.sentiment[df.teams_mentioned == 0].values.tolist()
sentiment_1 = df.sentiment[df.teams_mentioned == 1].values.tolist()
sentiment_2 = df.sentiment[df.teams_mentioned == 2].values.tolist()
sentiment_3 = df.sentiment[df.teams_mentioned == 3].values.tolist()

tweets_sentiment_all = pd.Series(sentiment_all, index = idx_all)
tweets_sentiment_0 = pd.Series(sentiment_0, index = idx_0)
tweets_sentiment_1 = pd.Series(sentiment_1, index = idx_1)
tweets_sentiment_2 = pd.Series(sentiment_2, index = idx_2)
tweets_sentiment_3 = pd.Series(sentiment_3, index = idx_3)
#zeros = pd.Series(zeros, index = idx_all)

per_minute_sentiment_all = tweets_sentiment_all.resample('1min').sum().fillna(0)
per_minute_sentiment_0 = tweets_sentiment_0.resample('1min').sum().fillna(0)
per_minute_sentiment_1 = tweets_sentiment_1.resample('1min').sum().fillna(0)
per_minute_sentiment_2 = tweets_sentiment_2.resample('1min').sum().fillna(0)
per_minute_sentiment_3 = tweets_sentiment_3.resample('1min').sum().fillna(0)
#zeros = zeros.resample('1min').sum()

# result_sentiment = pd.concat([per_minute_sentiment_all, per_minute_sentiment_0, per_minute_sentiment_1, per_minute_sentiment_2, per_minute_sentiment_3], axis = 1)
# result_sentiment.columns = ['All', 'Neither', 'Raps Only', 'Cavs Only', 'Both']
result_sentiment = pd.concat([per_minute_sentiment_1, per_minute_sentiment_2], axis = 1)
result_sentiment.columns = ['Raps', 'Cavs']

#chart 2

sentiment_per_min_chart = vincent.Line(result_sentiment)
sentiment_per_min_chart.axis_titles(x='Time', y='Sentiment')
sentiment_per_min_chart.legend(title='Legend')
sentiment_per_min_chart.axes['y'].title_offset = 50
sentiment_per_min_chart.scales['color'].range = 'category10'
sentiment_per_min_chart.to_json(gv.data_path + 'sentiment_per_min_chart.json')

#chart 3

per_minute_sentiment_sum_all = tweets_sentiment_all.resample('1min').sum().fillna(0).cumsum()
per_minute_sentiment_sum_0 = tweets_sentiment_0.resample('1min').sum().fillna(0).cumsum()
per_minute_sentiment_sum_1 = tweets_sentiment_1.resample('1min').sum().fillna(0).cumsum()
per_minute_sentiment_sum_2 = tweets_sentiment_2.resample('1min').sum().fillna(0).cumsum()
per_minute_sentiment_sum_3 = tweets_sentiment_3.resample('1min').sum().fillna(0).cumsum()
#zeros = zeros.resample('1min').sum()

# result_sentiment = pd.concat([per_minute_sentiment_sum_all, per_minute_sentiment_sum_0, per_minute_sentiment_sum_1, per_minute_sentiment_sum_2, per_minute_sentiment_sum_3], axis = 1)
# result_sentiment.columns = ['All', 'Neither', 'Raps Only', 'Cavs Only', 'Both']
result_sentiment_sum = pd.concat([per_minute_sentiment_sum_1, per_minute_sentiment_sum_2], axis = 1)
result_sentiment_sum.columns = ['Raps', 'Cavs']

sentiment_chart = vincent.Line(result_sentiment_sum)
sentiment_chart.axis_titles(x='Time', y='Sentiment')
sentiment_chart.legend(title='Legend')
sentiment_chart.axes['y'].title_offset = 50
sentiment_chart.scales['color'].range = 'category10'
sentiment_chart.to_json(gv.data_path + 'sentiment_chart.json')