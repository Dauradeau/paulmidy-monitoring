import os

os.system('snscrape --jsonl --max-results 1000 twitter-user "paulmidy" > paulmidy_tweets.json')
os.system('snscrape --jsonl --max-results 1000 twitter-search "Paul Midy" > mentions_paulmidy.json')
