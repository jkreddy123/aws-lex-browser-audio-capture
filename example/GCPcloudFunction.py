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
    print("request type", type(request))
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
      multiplier = firstelement['parameters']['multiplier']
      multiplicand = firstelement['parameters']['multiplicand']
      answer = firstelement['parameters']['answer']
    parametersdict = {
      	  "multiplier": multiplier,
          "multiplicand": multiplicand,
          "answer": answer,
          "uptotable": uptotable,
          "fromtable": fromtable
    }
    if(queryResult['action'] == 'genMultiplicationDummyAction'):
      multiplier = random.randint(int(fromtable),int(uptotable))
      multiplicand = random.randint(0,10)    
      followupEvent = "genMultiplicationDummyEvent"
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
      responsetext = "what is"+ str(multiplier) + " "+ str(multiplicand) +"s are?"
      WebhookResponse = {
       "fulfillmentMessages": [
        { "text": {"text": [ responsetext ] } }
       ]
      }
      print("askMultiplicationAction  ", multiplier, multiplicand, responsetext)
    elif (queryResult['action'] == 'checkAnswerDummyAction'):
      if int(uptotable) * int(fromtable) == answer :
        responsetext = "right answer"
        followupEvent = "genMultiplicationDummyEvent"
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
      responsetext = "Wrong Answer. Train again."
      WebhookResponse = {
       "fulfillmentMessages": [
        { "text": {"text": [ responsetext ] } }
       ]
      }
      print("tryAnswerAgainAction ", fromtable, uptotable,responsetext)
    else:
      print("no action ")
    return json.dumps(WebhookResponse)

