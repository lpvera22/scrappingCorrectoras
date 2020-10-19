from flask import Flask, request, json, Response,jsonify,abort
import pandas as pd
from database.db import MongoAPI
from flask_cors import CORS, cross_origin
from datetime import datetime
from flask_selfdoc  import Autodoc

import time

data = {
    "database": "DEVCorretoras",
    "collection": "",
}
app = Flask(__name__)
auto = Autodoc(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return " <h1 style='color:blue'>Root!</h1>"


@app.route('/api/urls', methods=['GET'])
@auto.doc()
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
@auto.doc()
@cross_origin()
def deleteallURls():
    data['collection'] = 'urls'

    mongo_obj = MongoAPI(data)
    response = mongo_obj.deleteAll()
    print(response)
    return jsonify(response)
    
@app.route('/api/urls/', methods=["PUT"])
@auto.doc()
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
@auto.doc()
@cross_origin()
def getParamsURl():
    
    data['collection'] = 'urls'
    
    url=request.args.get('url')
    data['url']=url
    mongo_obj = MongoAPI(data)
    response = mongo_obj.readFromUrl()
    print(response)
    return jsonify(response)
@app.route('/api/anotacao/', methods=["GET"])
@auto.doc()
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
@app.route('/api/anotacao/', methods=["POST"])
@auto.doc()
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


@app.route('/api/images/', methods=["GET"])
@auto.doc()
@cross_origin()
def getImg():
    
    data['collection'] = 'imgs'
    domain=request.args.get('domain')
    
    # print({'domain':domain})
    mongo_obj = MongoAPI(data)
    response = mongo_obj.readQuery({'domain':domain})
    
    if len(response)>0:
        
        
        
        return jsonify(response)
    else:
        return abort(404)
@app.route('/api/test/', methods=["GET","POST"])

@cross_origin()
def test():
    print(request.get_json()['data']['video']['title'])
    return {}

@app.route('/api/clock',methods=["GET"])
@cross_origin()
def time():
    now = datetime.now()
    FMT="%H:%M:%S"
    current_time = now.strftime(FMT)

    tdelta = datetime.strptime(current_time, FMT) - datetime.strptime("06:00:00", FMT)
    print(tdelta)
    return str(tdelta)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
