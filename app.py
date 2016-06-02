#!/usr/bin/env python
# coding=utf-8


import json
import requests
import config as cfg
from flask import Flask, redirect, request, jsonify, render_template, render_template_string
from middleware.authentication import Authentication
from pcloud.service import PCloudService
from models.authors import Authors
from models.books import Books
from utils import change_level
from models.users import Users

# from models.series import Series

app = Flask(__name__, template_folder='public', static_folder='public')
app.config['JSON_AS_ASCII'] = False
auth = Authentication()


@app.route('/', defaults={'p': 'home'})
@app.route('/<path:p>')
def main(p):
    return render_template("index.html")


"""Library api start"""


# TODO make authentication by path
@app.route('/api/v1/library/authors/search/<path:s>')
def find_author(s):
    with Authors() as authors_manager:
        result = authors_manager.find_by_fullname(s)
    return jsonify(result)


@app.route('/api/v1/library/books/byauthor/<path:aid>')
def find_books(aid):
    """'AID': None, 'BID': None, 'SERIE_NAME':None, 'SERIE_NUMBER': None, 'GENRE': None,'FILE': None, 'EXT': None,
    'DEL': None, 'LANG': None, 'SIZE': None, 'DATE':None, 'PATH':None})"""
    data = []
    with Books() as books_manager:
        books_result = books_manager.find_by_author(aid)

    books = books_result['rows']
    series = list(
        set([book['SERIE_NAME'] for book in books if book['SERIE_NAME'] is not None and len(book['SERIE_NAME']) > 0]))
    series.sort()
    noseq = [change_level(book, 0) for book in books if book['SERIE_NAME'] is None or len(book['SERIE_NAME']) == 0]
    noseq = sorted(noseq, key=lambda book: book['TITLE'])
    for serie_name in series:
        tmp_arr = [change_level({'TITLE': serie_name}, 0)]
        data = data + tmp_arr + [change_level(book, 1) for book in books if book['SERIE_NAME'] == serie_name]

    books_result['rows'] = data + noseq
    return jsonify(books_result)


"""Library api end """


@app.route('/api/v1/public/test')
def test():
    jdata = PCloudService.get_link("fb2-000024-030559", "24.fb2.zip")
    if jdata and jdata["result"] is 0:
        url = ""
        if jdata["hosts"]:
            url = "//" + jdata["hosts"][0] + jdata["path"]
        return render_template_string("<a href='{}'>24.fb2.zip</a>".format(url))
    return jsonify(jdata)


"""admin api start"""


@app.route('/api/v1/admin/users/new/<email>/<display>/<password>/<role>/', defaults={'modules': None})
@app.route('/api/v1/admin/users/new/<email>/<display>/<password>/<role>/<modules>')
def new_user(email, display, password, role, modules):
    with Users() as users:
        result = users.create_new(email, display, password, role, modules)
    return jsonify(result)


@app.route('/api/v1/public/authenticate', methods=['POST'])
def authenticate():
    if request.data is not None and "email" in request.data and "password" in request.data:
        login_params = json.loads(request.data)

        with Users() as users:
            result = users.login(login_params["email"], login_params["password"])
        return jsonify(result)

    return jsonify(error="access denied")


"""pcloud authenticate account"""


@app.route('/connect')
def connect():
    if not auth.check_token():
        return render_template("index.html")
    url = "{0}?client_id={1}&response_type=code&redirect_uri={2}".format(cfg.PCLOUD["authorize_url"],
                                                                         cfg.PCLOUD["client_id"],
                                                                         cfg.PCLOUD["redirect_uri"])
    return redirect(url)


"""pcloud get token"""


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
