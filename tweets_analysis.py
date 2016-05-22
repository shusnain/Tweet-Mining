import vincent
import numpy as np
import pandas as pd
import datetime as dt
import json
import sys

# source: https://marcobonzanini.com/2015/03/23/mining-twitter-data-with-python-part-4-rugby-and-term-co-occurrences/
args = sys.argv

df = pd.read_csv(args[1])
dates = df.created_at
ones = [1]*len(dates)
idx = pd.DatetimeIndex(dates).tz_localize('UTC').tz_convert('US/Eastern')
tweets = pd.Series(ones, index=idx)
per_minute = tweets.resample('1min').sum().fillna(0)

time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='Legend')
time_chart.to_json('time_chart.json')