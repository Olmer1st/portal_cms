#!/usr/bin/env python
# coding=utf-8


import json
import requests
import config as cfg
from flask import Flask, redirect, request, jsonify, render_template, render_template_string
from middleware.authentication import Authentication
from pcloud.service import PCloudService

app = Flask(__name__, template_folder='public', static_folder='public')
auth = Authentication()


@app.route('/',  defaults={'p': 'home'})
@app.route('/<path:p>')
def main(p):
    return render_template("index.html")

@app.route('/test')
def test():
    jdata = PCloudService.get_link("fb2-000024-030559", "24.fb2.zip")
    if jdata and jdata["result"] is 0:
        url = ""
        if jdata["hosts"]:
            url = "//" + jdata["hosts"][0] + jdata["path"]
        return render_template_string("<a href='{}'>24.fb2.zip</a>".format(url))
    return jsonify(jdata)


@app.route('/connect')
def connect():
    if not auth.check_token():
        return render_template("index.html")
    url = "{0}?client_id={1}&response_type=code&redirect_uri={2}".format(cfg.PCLOUD["authorize_url"],
                                                                         cfg.PCLOUD["client_id"],
                                                                         cfg.PCLOUD["redirect_uri"])
    return redirect(url)


@app.route('/getcode/', methods=['GET'])
def get_code():
    code = request.args.get('code')
    # state = request.args.get('state')  # will be required if need to transfer specific data back
    if not code:
        return jsonify(error="no code, please try again")
    url = "{0}/{1}?code={2}&client_id={3}&client_secret={4}".format(cfg.PCLOUD["api_url"],
                                                                    cfg.PCLOUD["methods"]["o2token"]["name"], code,
                                                                    cfg.PCLOUD["client_id"],
                                                                    cfg.PCLOUD["client_secret"])
    response = requests.get(url)
    jdata = json.loads(response.content)
    return jsonify(jdata)


if __name__ == '__main__':
    app.run(debug=True)
