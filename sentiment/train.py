import re 
import nltk
import pickle

trainfile = 'train_dataset.csv'
testfile = 'test_dataset.csv'
p = re.compile('(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')
word_features = []
stopwords = nltk.corpus.stopwords.words('english')

def getTweets(file):
    ifile = open(file)
    tweets = []

    for line in ifile:
        fields = line.strip().split(',')
        sentiment = fields[1]
        tweet = fields[3]
        words = re.sub(p, '', tweet).split()
        words_filtered = [w.lower() for w in words if not w.lower() in stopwords]
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
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

if __name__ == '__main__':
    tweets = getTweets(trainfile)
    word_features = get_word_features(get_words_in_tweets(tweets))
    f = open('word_feature', 'w')
    for word in word_features:
        f.write(word + '\n')
    f.close()

    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    f = open('classifer.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

    '''
    f = open('classifer.pickle')
    classifier = pickle.load(f)
    f.close()
    test_tweets = getTweets(testfile)
    
    i = 0
    for tweet,sentiment in test_tweets:
        #print classifier.classify(extract_features(tweet)), sentiment
        if classifier.classify(extract_features(tweet)) == sentiment:
            i += 1
    print i, len(test_tweets)
    '''
