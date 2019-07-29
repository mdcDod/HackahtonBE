import requests
from pprint import pprint
from DODApp.data import dataDict

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
            if intent != 'GoodGreeting' and intent != 'BadGreeting':
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
            returnData = "Sorry can't find " + entity + " data :("
        elif intent == "People.GetPhone":
            returnData = "The number of " + query["value"][0]["name"] + " is " + query["value"][0]["phone"]
        elif intent == "People.GetMail":
            returnData = "The Email of " + query["value"][0]["name"] + " is " + query["value"][0]["email"]
        else:
            returnData = "Sorry I can't understand what you want :("

    except Exception as e:
        returnData = "Sorry I can't find any Data :("

    return returnData
