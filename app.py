import os
import json
import requests
import config as cfg
from flask import Flask, redirect, request, jsonify

app = Flask(__name__, template_folder='public', static_folder='public')


@app.route('/connect')
def connect():
    url = "{0}?client_id={1}&response_type=code&redirect_uri={2}".format(cfg.PCLOUD["authorize_url"],
                                                                         cfg.PCLOUD["client_id"],
                                                                         cfg.PCLOUD["redirect_uri"])
    return redirect(url)


@app.route('/getcode/', methods=['GET'])
def get_code():
    code = request.args.get('code')
    state = request.args.get('state')
    print state
    url = "{0}/{1}?code={2}&client_id={3}&client_secret={4}".format(cfg.PCLOUD["api_url"],
                                                                    cfg.PCLOUD["methods"]["o2token"]["name"], code,
                                                                    cfg.PCLOUD["client_id"],
                                                                    cfg.PCLOUD["client_secret"])
    response = requests.get(url)
    jdata = json.loads(response.content)
    return jsonify(jdata)


if __name__ == '__main__':
    app.run(debug=True)
