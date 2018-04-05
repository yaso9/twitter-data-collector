import sys
import sqlite3
import requests
from requests_oauthlib import OAuth1
import json
import math

con = sqlite3.connect('database.sqlite')

args = sys.argv
del args[0]

quantity = int(args[0])
del args[0]

auth = OAuth1('cGwbiXwrw33DnBWGhHzJUffxc', 'rZn51eTjYJHui2SBHZgNJefKxtEUi86jyEW8VGAjUSRSNNs6U5', '1227859512-hkcgEIb8OC56i9FfSKsIyKKf59pRRAFqK5tIAMz', 'BzFkadS6ogx6FGQz8gMGwHceOMxII5QXnPyNBjP2mWOBt')

for i, hashtag in enumerate(args):
    lowId = 0
    cur = con.cursor()
    cur.execute('INSERT INTO hashtags (name) VALUES (?)', (hashtag,))
    cur.close()

    for hundred in range(int(math.floor(quantity / 100)) + 1):
        request = requests.get('https://api.twitter.com/1.1/search/tweets.json?count=' +
                               str(quantity if quantity < 100 else 100) +
                               '&q=%23' + hashtag, auth=auth)
        tweets = json.loads(request.text)

        for tweet in tweets['statuses']:
            if lowId > tweet['id']:
                lowId = tweet['id']
            cur = con.cursor()
            cur.execute('INSERT INTO tweets (hashtag_id, body) VALUES (?, ?)', (i + 1, tweet['text']))
            cur.close()
        quantity - 100

con.commit()
