from DODApp import app
from DODApp.APIConnector import contact2Luiz
from DODApp.APIConnector import contact2KB

@app.route('/')
@app.route('/dod/<question>')

def dod(question):
    mydata = contact2Luiz(question)
    if mydata[0] == 'None' and mydata[1] == 'None':
        return "Sorry I can't find answer for your question :("
    elif mydata[0] == 'GoodGreeting':
        return "You are so nice!!!!! :)"
    elif mydata[0] == 'BadGreeting':
        return "You are not nice!!!!! :("
    else:
        return contact2KB(mydata[0], mydata[1])


