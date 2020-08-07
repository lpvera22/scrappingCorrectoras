from flask import Flask, jsonify, Response
import pandas as pd
from database.db import initialize_db
from database.models import Scraping

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'mongodb+srv://admin:admin123@cluster0.hzfwu.mongodb.net/test?authSource=admin&replicaSet=atlas-nb4s9h'

}

initialize_db(app)


def getScraping():
    scraping = Scraping.objects().to_json()

    return Response(scraping, mimetype="application/json", status=200)


@app.before_request
def before():
    pass


@app.route('/api/scraping', methods=['GET', 'POST'])
def home():
    df = pd.read_csv('out/urlFinal.csv')
    # out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
    out = df.to_json(orient='records')
    return Response(out, mimetype='application/json')


if __name__ == '__main__':
    app.run()
