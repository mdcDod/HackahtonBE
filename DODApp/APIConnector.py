import requests
import random
from pprint import pprint
from DODApp.data import dataDict
import wolframalpha

'''
connecting to luis and getting the intent and the entity of the the given slang
'''
def contact2Luiz(slang):
    print("\n------ Connecting to luis and getting the intent and the entity of the the given slang ------\n")
    data2Return = []
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '007c73816f1245dc8df0de64aaa9017e',
    }

    params = {
        # Query parameter
        'q': slang,
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
    }

    try:
        r = requests.get(
            'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/04ad6f50-90b1-4bf3-b420-1326b58f6dd3',
            headers=headers, params=params)
        data = r.json()
        print(data)
        intent = data["topScoringIntent"]["intent"]

        try:
            entity = data["entities"][0]["entity"]
            try:
                entity2 = data["entities"][1]["entity"]
                if len(entity) < entity2:
                    entity = entity2
            except Exception as e:
                print("There is one entity!!!!!")
        except Exception as e:
            if intent != 'GoodGreeting' and intent != 'BadGreeting' and intent != 'Quotes':
                intent = 'None'
            entity = 'None'

    except Exception as e:
        print("There is an exception(luiz)")
        intent = "None"
        entity = "None"

    data2Return.append(intent)
    data2Return.append(entity)
    print("intent = " + intent + " and the entity = " + entity)
    return data2Return


'''
Function for connecting to knowledge base and getting the answer for the entity by the intent
'''


def contact2KB(intent, entity):
    print("\n------ Connecting to knowledge base and getting the answer ------\n")
    try:
        endpoint = 'https://dod-search.search.windows.net/'
        api_version = '?api-version=2019-05-06'
        headers = {'Content-Type': 'application/json', 'api-key': '5C138BD2483D803143DA924834CCA220'}
        url = endpoint + "indexes" + api_version + "&$select=name"
        response = requests.get(url, headers=headers)
        index_list = response.json()
        pprint(index_list)
        searchstring = "&count=true&search=" + entity + "&queryType=full"
        print(dataDict[intent])
        url = endpoint + "indexes/" + dataDict[intent] + "/docs" + api_version + searchstring
        response = requests.get(url, headers=headers, json=searchstring)
        query = response.json()
        pprint(query)
        print(len(query))

        if len(query["value"]) == 0:
            returnData = "Sometimes, " + entity + " does't find what " + entity + " needs."
        elif intent == "People.GetPhone":
            returnData = query["value"][0]["name"] + "'s number is " + query["value"][0]["phone"]
        elif intent == "People.GetMail":
            returnData = query["value"][0]["name"] + "'s email is " + query["value"][0]["email"]
        elif intent == "Product.GetPrice":
            print("\n\n\n nigger")
            print(query["value"][0]["product_name"])
            print(query["value"][0]["product_price"])
            returnData = query["value"][0]["product_name"] + "'s price is " + str(query["value"][0]["product_price"])
        elif intent == "Environment.GetInCharge":
            returnData = "The " + query["value"][0]["relevant_group"] + " is in charge of " + query["value"][0]["subject"]
        else:
            returnData = "I do not understand what do you want."

    except Exception as e:
        returnData = "I was not able to find the information about " + entity + ' "Failure is only the opportunity to begin again. Only this time more wisely."'
        pass

    return returnData


def Wolf(text):
    print("hello wolf")
    print("text = " + text)
    try:
        if type(text) is list or type(text) is dict:
            text = text[0]
            print()
    except Exception as e:
        print(text)
    print("text = " + text)
    client = wolframalpha.Client("2GLGUV-8EA25Y85JA")
    res = client.query(text)
    # print(res)
    try:
        print(res.results)
        res = next(res.results).text
        print(res)
    except Exception as e:
        res = "None"
        print(res)

    return res

def FindLang(text):
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/detect?key=trnsl.1.1.20190729T163126Z.07d8bee6b2eb7896.8c9c9876111d29c46791a76c2b2e4325a4b1d42a&text=' + text)
        return response.json()['lang']

def Translate(text, direction):
    try:
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20190729T163126Z.07d8bee6b2eb7896.8c9c9876111d29c46791a76c2b2e4325a4b1d42a&text=' + text + '&lang=' + direction)
        data = response.json()["text"]
        print(data)
    except Exception as e:
        data = "en"
    return data