def  quickstart_add_data_two(multiplier,multiplicand,answer,headers):
    from google.cloud import firestore
    db = firestore.Client()
    doc_ref = db.collection(u'tableQuestions').document(headers['audioURL'])
    doc_ref.set({
        u'userID': headers['userID'],
        u'answer': headers['textmsg'],
        u'multiplier': multiplier,
        u'multiplicand': multiplicand
    })


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    import json
    import random

    
    print(request)
    request_json = {}
    queryResult = {}
    firstelement =[]
    multiplier = multiplicand = answer = 1
    fromtable = 2
    uptotable = 20
    print("request type", type(request))
    print("request headers", request.headers)
    request_json = json.loads(request.data)
    print("request json type", type(request_json))
    print(request_json['queryResult'])
    queryResult = request_json['queryResult']
    contextarray = queryResult['outputContexts']
    print(contextarray)
    for context in contextarray:
      if 'parameters' in context:
        if 'answer' in context['parameters']:
           firstelement = context
           break
    print(firstelement)
    if 'uptotable' in firstelement['parameters'] :
      uptotable = firstelement['parameters']['uptotable']
      fromtable = firstelement['parameters']['fromtable']
    if 'multiplier' in firstelement['parameters'] :
      multiplier = int(firstelement['parameters']['multiplier'])
      multiplicand = int(firstelement['parameters']['multiplicand'])
      answer = firstelement['parameters']['answer']
    parametersdict = {
      	  "multiplier": multiplier,
          "multiplicand": multiplicand,
          "answer": answer,
          "uptotable": uptotable,
          "fromtable": fromtable
    }
    if(queryResult['action'] == 'genMultiplicationDummyAction'):
      multiplier = int(random.randint(int(fromtable),int(uptotable)))
      multiplicand = int(random.randint(0,10))    
      followupEvent = "askMultiplicationEvent"
      parametersdict = {
      	  "multiplier": multiplier,
          "multiplicand": multiplicand,
          "answer": answer,
          "uptotable": uptotable,
          "fromtable": fromtable
      }
      
      print("genMultiplicationDummyAction ",multiplier, multiplicand)
      WebhookResponse = {
        "followupEventInput": {
          "name": followupEvent,
    	  "parameters": parametersdict 
        }
      }
    elif(queryResult['action'] == 'askMultiplicationAction'):
      responsetext = "what is "+ str(multiplier) + " "+ str(multiplicand) +"s are?"
      WebhookResponse = {
       "fulfillmentMessages": [
        { "text": {"text": [ responsetext ] } }
       ]
      }
      print("askMultiplicationAction  ", multiplier, multiplicand, responsetext)
    elif (queryResult['action'] == 'checkAnswerDummyAction'):
      if int(multiplier) * int(multiplicand) == answer :
        responsetext = "right answer"
        followupEvent = "genMultiplicationDummyEvent"
        quickstart_add_data_two(multiplier,multiplicand,answer,request.headers)
      else:
        responsetext = "wrong answer"
        followupEvent = "tryAnswerAgainEvent"
      print("checkAnswerDummyAction ", followupEvent,responsetext)
      WebhookResponse = {
        "followupEventInput": {
          "name": followupEvent,
    	  "parameters": parametersdict 
        }
      }      
    elif(queryResult['action'] == 'tryAnswerAgainAction'):
      responsetext = "Wrong Answer. Try again."
      WebhookResponse = {
       "fulfillmentMessages": [
        { "text": {"text": [ responsetext ] } }
       ]
      }
      print("tryAnswerAgainAction ", fromtable, uptotable,responsetext)
    else:
      print("no action ")
    return json.dumps(WebhookResponse)
