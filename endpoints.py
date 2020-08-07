from flask import Flask, jsonify, Response
import pandas as pd

app = Flask(__name__)


@app.before_request
def before():
    pass


@app.route('/api/urls', methods=['GET', 'POST'])
def home():
    df = pd.read_csv('out/urlFinal.csv')
    # out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
    out = df.to_json(orient='records')
    return Response(out, mimetype='application/json')


if __name__ == '__main__':
    app.run()
