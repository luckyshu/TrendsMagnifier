import re 
import nltk
import pickle
import operator
import util

p = re.compile('(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')
word_features = []
stopwords = nltk.corpus.stopwords.words('english')

def getTweets(tweets):
    tweets_filtered = []
    for tweet in tweets:
        words = tweet.split()
        words_filtered = [w.lower() for w in words if not w.lower() in stopwords]
        tweets_filtered.append(words_filtered)   
    return tweets_filtered

def getTweet(tweet):
    words = tweet.split()
    words_filtered = [w.lower() for w in words if not w.lower() in stopwords]
    return words_filtered

def get_words_in_tweets(tweets):
    all_words = []
    for words in tweets:
        all_words.extend(words)
    return all_words

def get_top(trend, wordlist):
    d = {}
    wordlist = nltk.FreqDist(wordlist)
    sorted_words = sorted(wordlist.iteritems(), key = operator.itemgetter(1), reverse = True)
    i = 0
    if trend.find('#') != -1:
        trend = util.formatPhrase(trend)
    l = trend.split(' ')
    lower_l = [word.lower() for word in l]

    for word,frequency in sorted_words:
        if not word.isdigit() and word not in lower_l and word != ''.join(lower_l):
            d[word.lower()] = frequency 
            i += 1
        if i == 10:
            break
    return d

def get_word_features_from_file(file):
    f = open(file)
    for line in f:
        word_features.append(line.strip())
    f.close()

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def getKeywords(trend, tweets):
    tweets_filtered = getTweets(tweets)
    return get_top(trend, get_words_in_tweets(tweets_filtered))

def getSentiment(tweet):
    f = open('/Users/Shu/Desktop/Insight/v1/classifer.pickle')
    classifier = pickle.load(f)
    f.close()
    word_features = get_word_features_from_file('/Users/Shu/Desktop/Insight/v1/word_feature')
    words_filtered = getTweet(tweet)
    return int(classifier.classify(extract_features(words_filtered)))

def getSentiments(l):
    f = open('/Users/Shu/Desktop/Insight/v1/classifer.pickle')
    classifier = pickle.load(f)
    f.close()
    word_features = get_word_features_from_file('/Users/Shu/Desktop/Insight/v1/word_feature')
    for d in l:
        tweet = d['text']
        words_filtered = getTweet(tweet)
        d['sentiment'] = int(classifier.classify(extract_features(words_filtered)))
    return l

