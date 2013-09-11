from twitter import *
import sys
import calendar
import time
import re
import util 
import getSentiment

access_token_key = "134833802-ihkTufX0SeExjQsgbWEzMJ5r2pdmYS0zHbGJj4Vs"
access_token_secret = "Dplvd2COtKhLlm1ZVH2K6y3PmTyA1AHdgueyzI5k"

consumer_key = "Jro5MtJIYDUX5wxXecEQw"
consumer_secret = "GzurezzzB5to1zwe7ghzORuoBgekD2NULj0Qubew"

def getTweets(city, trend):
    twitter = Twitter(auth=OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret))
    geocode = util.getGeo(city)
    query = twitter.search.tweets(q = trend, lang = 'en', count = 100, geocode = geocode)
    l = []
    prev_name = 'ls'
    text_l = []

    for result in query['statuses']:
        d = {}
        #print "(%s, %s) @%s %s %s" % (result['created_at'], result['lang'], result['user']['location'], result['text'], result['user']['name'])

        '''
        if result['geo'] != None:
            d['location'] = result['geo']['coordinates']
        else:
            d['location'] = result['user']['location'].strip()
            '''
        text = result['text'].encode('utf-8').strip()
        p=re.compile('(@[A-Za-z0-9_]+)|([^0-9A-Za-z \#\t])|(\w+:\/\/\S+)')
        text = ' '.join(re.sub(p, '', text).split())

        if (text == trend):
            continue
        if (text.lower().find('rt') != -1):
            continue
        if (text.find('\xf0') != -1):
            continue 
        if not util.checkUnique(text, text_l):
            continue

        d['text'] = text

        p=re.compile('(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')
        text = re.sub(p, '', text)
        text_l.append(text)

        d['name'] = result['user']['name'].encode('utf-8').strip()
        if d['name'] == prev_name:
            continue
        prev_name = d['name']
        if trend.find('#') != -1:
            trend = util.formatPhrase(trend)
        trend_l = trend.split(' ')
        name_l = d['name'].split(' ')
        #if d['name'].find(trend) != -1:
            #continue
        for name in name_l:
            if name.title() in trend_l:
                #print "trend in name", d['name'], trend
                continue
        d['location'] = result['user']['location'].strip()

        timestamp = result['created_at']
        format = '%a %b %d %H:%M:%S +0000 %Y'
        s = time.strptime(timestamp, format)
        d['created_at'] = int(calendar.timegm(s))

        l.append(d)
    
    getSentiment.getSentiments(l)
    keywords = getSentiment.getKeywords(trend, text_l)
    l.insert(0, keywords)
    return l

        


