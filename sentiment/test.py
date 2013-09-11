import re 
import nltk
import pickle
import operator

testfile = 'small_test_dataset.csv'
p = re.compile('(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')
word_features = []

def getTweets(file):
    ifile = open(file)
    tweets = []

    for line in ifile:
        fields = line.strip().split(',')
        sentiment = fields[1]
        tweet = re.sub(p, '', fields[3])
        words = tweet.split()
        words_filtered = [word.lower() for word in words if len(word) >= 3]
        tweets.append((words_filtered, sentiment))   
    ifile.close()
    return tweets

def get_words_in_tweets(tweets):
    all_words = []
    for(words,sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    sorted_words = sorted(wordlist.iteritems(), key = operator.itemgetter(1), reverse = True)
    for i in range(10):
        print '%s %d' % (sorted_words[i][0], sorted_words[i][1])
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def getSentiment(tweet)
def test():
    f = open('classifer.pickle')
    classifier = pickle.load(f)
    f.close()
    tweets = getTweets(testfile)
    word_features = get_word_features(get_words_in_tweets(tweets))
    i = 0
    for tweet,sentiment in tweets:
        #print classifier.classify(extract_features(tweet)), sentiment
        if classifier.classify(extract_features(tweet)) == sentiment:
            i += 1
    print i, len(tweets)
