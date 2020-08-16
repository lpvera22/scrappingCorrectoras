from flask import Flask, request, json, Response,jsonify,abort
import pandas as pd
from database.db import MongoAPI
from flask_cors import CORS, cross_origin
from datetime import datetime
data = {
    "database": "Corretoras",
    "collection": "",
}
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/api/urls', methods=['GET'])
@cross_origin()
def getURls():
    data['collection'] = 'urls'
    
        
    mongo_obj = MongoAPI(data)
    response = mongo_obj.read()
    print(response)
    return jsonify(response)
    # return Response(response=jsonify(response),
    #                 status=200,
    #                 mimetype='application/json')

@app.route('/api/urls', methods=["DELETE"])
@cross_origin()
def deleteallURls():
    data['collection'] = 'urls'

    mongo_obj = MongoAPI(data)
    response = mongo_obj.deleteAll()
    print(response)
    return jsonify(response)
    
@app.route('/api/urls/', methods=["PUT"])
@cross_origin()
def updatelURl():
    r=request.get_json()
    data['collection'] = 'urls'
    data['Filter']={'url':r['url']}
    data['state']={'state':r['state']}
    
    mongo_obj = MongoAPI(data)
    response = mongo_obj.update()
    print(response)
    return jsonify(response)

@app.route('/api/url/', methods=["GET"])
@cross_origin()
def getParamsURl():
    
    data['collection'] = 'urls'
    
    url=request.args.get('url')
    data['url']=url
    mongo_obj = MongoAPI(data)
    response = mongo_obj.readFromUrl()
    print(response)
    return jsonify(response)

@app.route('/api/anotacao/', methods=["POST"])
@cross_origin()
def postAnotacao():
    
    data['collection'] = 'anotacao'
    r=request.get_json()
    data['Document']={
        'domain':r['domain'],
        'title':r['title'],
        'content':r['content'],
        'resource':r['resource'],
        'data': datetime.today().strftime('%Y-%m-%d')
    }
    mongo_obj = MongoAPI(data)
    response = mongo_obj.write(data)
    # print(response)
    return jsonify(response)

@app.route('/api/anotacao/', methods=["GET"])
@cross_origin()
def getLatestAnotacao():
    
    data['collection'] = 'anotacao'
    domain=request.args.get('domain')
    resource=request.args.get('resource')
    print({'domain':domain,'resource':resource})
    mongo_obj = MongoAPI(data)
    response = mongo_obj.readQuery({'domain':domain,'resource':resource})
    
    if len(response)>0:
        
        response.sort(key=lambda x: x['data'], reverse=True)
        
        return jsonify(response[0])
    else:
        return abort(404)

if __name__ == '__main__':
    app.run()
