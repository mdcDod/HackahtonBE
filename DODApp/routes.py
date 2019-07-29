from DODApp import app
from DODApp.APIConnector import contact2Luiz
from DODApp.APIConnector import contact2KB
from DODApp.APIConnector import FindLang
from DODApp.APIConnector import Translate
import random
from DODApp.data import dodQuotes


@app.route('/')
@app.route('/dod/<question>')

def dod(question):
    sourceLang = FindLang(question)
    if sourceLang != 'en':
        print(sourceLang)
        print("not english")
        lang = sourceLang + "-en"
        question = Translate(question, lang)
    else:
        print("english")

    tempDict = {}
    mydata = contact2Luiz(question)
    if mydata[0] == 'None' and mydata[1] == 'None':
        tempDict = {"data": "Sometimes in life you cannot find all the answers. This is one of theses times.", "type":"Text"}
    elif mydata[0] == 'GoodGreeting':
        tempDict = {"data": "I thank you.", "type":"Text"}
    elif mydata[0] == 'BadGreeting':
        tempDict = {"data": "This is not a nice thing to say.", "type":"Text"}
    elif mydata[0] == "Quotes":
        tempDict = {"data": random.choice(dodQuotes), "type":"Text"}
    else:
        data = contact2KB(mydata[0], mydata[1])
        if sourceLang != 'en':
            data = Translate(data, "en-" + sourceLang)
        tempDict = {"data": data, "type": "Text"}
    return tempDict
