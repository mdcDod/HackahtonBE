from DODApp import app
from DODApp.APIConnector import contact2Luiz
from DODApp.APIConnector import contact2KB
import json


@app.route('/')
@app.route('/dod/<question>')
def dod(question):
    tempDict = {}
    mydata = contact2Luiz(question)
    if mydata[0] == 'None' and mydata[1] == 'None':
        tempDict.update({"data": "Sorry I can't find answer for your question :("})
    elif mydata[0] == 'GoodGreeting':
        tempDict.update({"data": "You are so nice!!!!! :)"})
    elif mydata[0] == 'BadGreeting':
        tempDict.update({"data": "You are not nice!!!!! :("})
    else:
        tempDict.update({"data": contact2KB(mydata[0], mydata[1])})
    return tempDict
