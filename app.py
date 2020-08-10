from flask import Flask, request, json, Response
import pandas as pd
from database.db import MongoAPI

data = {
    "database": "Corretoras",
    "collection": "",
}
app = Flask(__name__)


@app.before_request
def before():
    pass


@app.route('/api/urls', methods=['GET'])
def getURls():
    data['collection'] = 'urls'

    mongo_obj = MongoAPI(data)
    response = mongo_obj.read()

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
