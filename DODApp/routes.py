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
        tempDict = {"data": "Sorry I can't find answer for your question :(", "type":"Text"}
    elif mydata[0] == 'GoodGreeting':
        tempDict = {"data": "You are so nice!!!!! :)", "type":"Text"}
    elif mydata[0] == 'BadGreeting':
        tempDict = {"data": "You are not nice!!!!! :(", "type":"Text"}
    else:
        tempDict = {"data": contact2KB(mydata[0], mydata[1]), "type":"Text"}
    return tempDict
