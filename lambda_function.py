import requests
from bs4 import BeautifulSoup


# Return json Builders------------------------------------------------------------------------------

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def statement(title, body, b):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = b
    return build_response(speechlet)
#-----------------------------------------------------------------Fetching data from Inshorts

def getShortNews(category):
    newsDictionary = {
        'success': True,
        'category': category,
        'data': []
    }
    try:
        htmlBody = requests.get('https://www.inshorts.com/en/read/' + category)
    except requests.exceptions.RequestException as e:
        newsDictionary['success'] = False
        newsDictionary['errorMessage'] = str(e.message)
        return newsDictionary

    soup = BeautifulSoup(htmlBody.text, 'lxml')
    newsCards = soup.find_all(class_='news-card')
    if not newsCards:
        newsDictionary['success'] = False
        newsDictionary['errorMessage'] = 'Invalid Category'
        return newsDictionary

    for card in newsCards:
        try:
            title = card.find(class_='news-card-title').find('a').text
        except AttributeError:
            title = None

        newsObject = {
            'title': title,            
            }
        newsDictionary['data'].append(newsObject)
    return newsDictionary

def trimshortNews(kk,category):
    News = "Your short news for category "+category+" is as follows  "
    for ll in kk['data']:
        NewsItem = ll['title']
        NewsItem = NewsItem.replace("'", "")
        News = News + NewsItem + ". "
    return News

#-----------------------------------------------------------------CUSTOM INTENT logic
def getAllNews(event, context):
    Abss = trimshortNews(getShortNews('technology'),'technology')
    return statement("getting_AllNews", Abs, False)

# ---------------------------------------------------------------Identifying intents
def intent_router(event, context):
    intent = event['request']['intent']['name']

    if intent == "getAllNews":
        return getAllNews(event, context)  

    if intent == "AMAZON.StopIntent":
        return stop_BMP(event, context)
# ----------------------------------------------------------------Welcome message
def on_launch(event, context):
    return statement("Welcome", "A very warm welcome to Short News", False)


#------------------------------------------------------------------Opening short news 
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
#-------------------------------------------------------------------------------------