from flask import Flask, session, flash, request, g
from flask import redirect, url_for, render_template
import MySQLdb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    cursor = g.db.cursor()
    cursor.execute('select * from cities')
    cities = cursor.fetchall()
    #cursor.execute('select * from trendCategory')
    #categories = cursor.fetchall()
    return render_template('index.html', cities = cities)

@app.route('/details', methods=['POST', 'GET'])
def details():
    if request.method == 'POST':
        city = request.form['city']
        cursor = g.db.cursor()
        cursor.execute('select id, phrase from trend where city = %s order by ID desc limit 10', (city))
        rows = cursor.fetchall()
        trends = [{'id':row[0], 'phrase':row[1]} for row in rows]
        cursor.execute('select last_updated from trend where city = %s order by ID desc limit 1', (city))
        rows = cursor.fetchall()
        last_updated = time.strftime('%d %b %Y %H:%M:%S', time.localtime(int(rows[0][0])))
        cursor.execute('select keywords, sentiment from trend where id = %s', trends[0]['id'])
        rows = cursor.fetchall()
        keywords = [word.title() for word in rows[0][0].split(';')]
        sentiment = round(rows[0][1], 2)
        cursor.execute('select title, url, clicks from news where trend_id = %s order by clicks desc limit 5', trends[0]['id'])
        rows = cursor.fetchall()
        news = [{'title':row[0], 'url':row[1], 'clicks':row[2]} for row in rows]
        cursor.execute('select text, user, location, sentiment from tweet where trend_id = %s order by id desc limit 20', trends[0]['id'])
        rows = cursor.fetchall()
        tweets = [{'text':row[0], 'user':row[1], 'location':row[2], 'sentiment':row[3]} for row in rows]
        return render_template('details.html', list = trends, city = city, news = news, tweets = tweets, trend_id = trends[0]['id'], keywords = keywords, sentiment = sentiment, last_updated = last_updated)
    else:
        city = request.args.get('city', '')
        trend_id = request.args.get('trend_id', '')
        cursor = g.db.cursor()
        cursor.execute('select id, phrase from trend where city = %s order by ID desc limit 10', (city))
        rows = cursor.fetchall()
        trends = [{'id':row[0], 'phrase':row[1]} for row in rows]
        cursor.execute('select last_updated from trend where city = %s order by ID desc limit 1', (city))
        rows = cursor.fetchall()
        last_updated = time.strftime('%d %b %Y %H:%M:%S', time.localtime(int(rows[0][0])))
        cursor.execute('select keywords, sentiment from trend where id = %s', trend_id)
        rows = cursor.fetchall()
        keywords = [word.title() for word in rows[0][0].split(';')]
        sentiment = round(rows[0][1], 2)
        cursor.execute('select title, url, clicks from news where trend_id = %s order by clicks desc limit 5', (trend_id))
        rows = cursor.fetchall()
        news = [{'title':row[0], 'url':row[1], 'clicks':row[2]} for row in rows]
        cursor.execute('select text, user, location, sentiment from tweet where trend_id = %s order by id desc limit 20', (trend_id))
        rows = cursor.fetchall()
        tweets = [{'text':row[0], 'user':row[1], 'location':row[2], 'sentiment':row[3]} for row in rows]
        return render_template('details.html', list = trends, city = city, news = news, tweets = tweets, trend_id = int(trend_id), keywords = keywords, sentiment = sentiment, last_updated = last_updated)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/slideshare')
def slideshare():
    return render_template('slideshare.html')

@app.before_request
def db_connect():
    g.db = MySQLdb.connect("localhost","insight","1234","trendsmagnifier")

@app.teardown_request
def db_disconnect(exception=None):
    g.db.close()
    
if __name__ == "__main__":
    app.run(debug = True)
