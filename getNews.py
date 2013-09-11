import requests
import json
import util
    
linkClicksUrl = 'https://api-ssl.bitly.com/v3/link/clicks?access_token={0}&link={1}'

searchUrl = "https://api-ssl.bitly.com/v3/search?access_token={0}&query={1}&limit={2}&lang=en&fields=aggregate_link%2Ctitle"
link_limit = 5

categoryUrl = 'https://api-ssl.bitly.com/v3/link/category?access_token={0}&link={1}'

token = '900ec1b80e3a44d65daebc12acf830d2a415cf79'


def getClicks(link):
    r = requests.get(linkClicksUrl.format(token, link))
    response = json.loads(r.content)
    if (response['status_code'] == 200):
        return response['data']['link_clicks']
    else:
        print 'getNews/getClicks', response['status_code']

def getLinks(phrase):
    if phrase.find('#') != -1:
        phrase = util.formatPhrase(phrase)
    
    list = phrase.split(' ')
    if len(list) > 3:
        phrase = ' '.join(list[:3])

    r = requests.get(searchUrl.format(token, phrase, link_limit))
    response = json.loads(r.content)
    links = {}
    if (response['status_code'] == 200):
        for result in response['data']['results']:
            title = result.get('title', None)
            if util.checkUnique(title, links.values()):
                links[result['aggregate_link']] = title
        return links
    else:
        print 'getNews/getLinks', response['status_code']

        
def getCategory(link):
    all = ['Sports', 'Entertainment', 'Celebrity', 'Food', 'Technology', 'Politics', 'Business', 'News']
    r = requests.get(categoryUrl.format(token, link))
    response = json.loads(r.content)
    if (response['status_code'] == 200):
        list = response['data']['categories']
        result = ['News']
        for c in list:
            if c in all and c not in result:
                result.append(c)
        return ';'.join(result)

    else:
        print 'getNews/getInfo', response['status_code']

