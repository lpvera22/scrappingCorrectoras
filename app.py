from flask import Flask, request, json, Response,jsonify
import pandas as pd
from database.db import MongoAPI
from flask_cors import CORS, cross_origin
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


if __name__ == '__main__':
    app.run()
