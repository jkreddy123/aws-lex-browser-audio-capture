from google.cloud import firestore
import json
import flask

def usersignedin(request):
    # Set CORS headers for the preflight request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers',
        'Access-Control-Max-Age': '3600'
    }
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s


        return ('', 204, headers)
    
    userdata = request.get_json(silent=True)
    print("request json",userdata)
    
    db = firestore.Client()
    doc_ref = db.collection(u'usersignins').document(userdata['Email'])
    doc_ref.set({
        u'ID': userdata['ID'],
        u'Name': userdata['Name'],
        u'ImageURL': userdata['ImageURL'],
        u'Email': userdata['Email']
    })
    return ("Hello ",200, headers)
