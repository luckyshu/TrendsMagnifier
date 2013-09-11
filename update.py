#!/usr/bin/env python

import getTrends
import getNews
import MySQLdb
import time
import sys
import getTweet
import util
import json
import os

cities = [['San Francisco', 'New York', 'Chicago'], ['Seattle', 'Washington', 'Houston'], ['Indianapolis', 'Boston', 'Miami'], ['Phoenix', 'Denver', 'Los Angeles']]


db = MySQLdb.connect("localhost","insight","1234","trendsmagnifier")
cursor = db.cursor()
category_mapping = {'Sports':1, 'Entertainment':2, 'Celebrity':3, 'Food':4, 'Technology':5, 'Politics':6, 'Business':7, 'News':8}
city_group_id = int(sys.argv[1])

for city in cities[city_group_id]:
    trends = getTrends.getTwitterTrends(city)
    ts = int(time.time())
    try:
        for trend in trends:
            print trend
            positive = 0
            trend_insert_query = """
                INSERT INTO TREND
                (last_updated, phrase, city)
                VALUES
                (%s, %s, %s)
                """
            cursor.execute(trend_insert_query, (ts, trend, city))
            #db.commit()
            #trend_id = int(cursor.lastrowid)
            trend_id = db.insert_id()

            tweet_list = getTweet.getTweets(city, trend)
            tweet_insert_query = """
                INSERT INTO TWEET
                (created_at, trend_id, text, location, user, sentiment)
                VALUES
                (%s, %s, %s, %s, %s, %s)
                """
            for tweet in tweet_list[1:]:
                cursor.execute(tweet_insert_query, (tweet['created_at'], trend_id, tweet['text'], tweet['location'], tweet['name'], tweet['sentiment']))
                positive += tweet['sentiment']
        
            keywords = ';'.join(tweet_list[0].keys())
            sentiment = float(positive) / len(tweet_list)
            print keywords,sentiment,len(tweet_list[1:])
            trend_update = """
                UPDATE TREND
                SET sentiment=%s, keywords=%s
                WHERE id=%s
                """
            cursor.execute(trend_update, (sentiment, keywords, trend_id))

            categories = []
            news_exist = False
            if os.path.exists('/Users/Shu/Desktop/Insight/v1/news_results'):
                newsresults = open('/Users/Shu/Desktop/Insight/v1/news_results', 'r')
                for line in newsresults:
                    record = json.loads(line)
                    if 'trend' in record.keys():
                        if record['trend'] == trend:
                            print 'same trend'
                            news_exist = True
                            for link_record in record['links']:
                                news_insert_query = """
                                    INSERT INTO NEWS
                                    (last_updated, trend_id, clicks, url, category, title)
                                    VALUES
                                    (%s, %s, %s, %s, %s, %s)
                                    """
                                cursor.execute(news_insert_query, (link_record['link_ts'], trend_id, link_record['clicks'], link_record['link'], link_record['categories'], link_record['title']))
                            
                                for category in link_record['categories'].split(';'):
                                    if category not in categories:
                                        categories.append(category)
                            newsresults.close()
                            break

            if news_exist == False:
                result = {} 
                newsresults = open('/Users/Shu/Desktop/Insight/v1/news_results', 'a')
                result['trend'] = trend;
                result['links'] = []
                links = getNews.getLinks(trend)
                for link in links.keys():
                    link_record = {}
                    clicks = getNews.getClicks(link)  
                    title = links[link]
                    link_record['link'] = link
                    link_record['clicks'] = clicks
                    link_record['title'] = title

                    news_categories = getNews.getCategory(link)
                    link_record['categories'] = news_categories
                    for category in news_categories.split(';'):
                        if category not in categories:
                            categories.append(category)
                    link_ts = str(int(time.time()))
                    link_record['link_ts'] = link_ts
                    news_insert_query = """
                        INSERT INTO NEWS
                        (last_updated, trend_id, clicks, url, category, title)
                        VALUES
                        (%s, %s, %s, %s, %s, %s)
                        """
                    cursor.execute(news_insert_query, (link_ts, trend_id, clicks, link, news_categories, title))
                    result['links'].append(link_record)

                with newsresults as outfile:
                    json.dump(result, outfile)
                    outfile.write('\n')
                newsresults.close()
             
            cid = []
            for c in categories:
                cid.append(category_mapping[c])
            trend_category_insert_query = """
                INSERT INTO trend_category_junction
                (trend_id, category_id)
                VALUES
                (%s, %s)
                """
            for category_id in cid:
                cursor.execute(trend_category_insert_query, (trend_id, category_id))
                       
            db.commit()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        db.rollback()
        sys.exit(1)


