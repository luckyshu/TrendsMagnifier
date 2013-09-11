import re
import difflib

citymapping = '/Users/Shu/Desktop/Insight/v1/citymapping.csv'

def getWoeid(city):
    ofile = open(citymapping, 'r')
    for line in ofile:
        l = line.split(';')
        if (l[0] == city):
            return l[1]
    return 23424977

def getGeo(city):
    ofile = open(citymapping, 'r')
    for line in ofile:
        l = line.split(';')
        if (l[0] == city):
            return l[2]
    return '37.090240,-95.712891,3000km'

def formatPhrase(phrase):
    phrase = phrase.replace('#', '')
    l = re.findall('[A-Z][^A-Z]*', phrase)
    if (len(l) > 0):
        phrase = ' '.join(l)
    return phrase

def checkUnique(text, l):
    if text is None:
        return False
    list_text = [ch for ch in text if ch.isalnum() or ch == ' ']
    for s in l:
        list_s = [ch for ch in s if ch.isalnum() or ch == ' ']
        sm = difflib.SequenceMatcher(None, list_text, list_s)
        if (sm.ratio() > 0.7):
            return False
    return True


