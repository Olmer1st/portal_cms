#!/usr/bin/env python
# coding=utf-8


import json
import requests
import config as cfg
from flask import Flask, redirect, request, jsonify, render_template, render_template_string, make_response
from middleware.authentication import Authentication
from pcloud.service import PCloudService
from models.authors import Authors
from models.books import Books
from utils import change_level
from models.users import Users
from models.series import Series
from models.genres import Genres

app = Flask(__name__, template_folder='public', static_folder='public')
# app.config.from_pyfile('flaskapp.cfg') # production only
app.config['JSON_AS_ASCII'] = False


@app.route('/', defaults={'p': 'home'})
@app.route('/<path:p>')
def main(p):
    return render_template("index.html")


"""Library api start"""


@app.route('/api/v1/library/authors/search/<search_param>')
def find_author(search_param):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    with Authors() as authors_manager:
        result = authors_manager.find_by_fullname(search_param)
    return jsonify(result)


@app.route('/api/v1/library/series/search/<search_param>')
def find_serie(search_param):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    with Series() as series_manager:
        result = series_manager.find_serie_by_name(search_param)
    return jsonify(result)


@app.route('/api/v1/library/series/<int:page>/<int:max_rows>', methods=['GET'])
def get_series(page, max_rows):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")

    end = max_rows if page == 1 else  max_rows * page
    start = page if page == 1 else  end - max_rows

    with Series() as series:
        result = series.get_all_series(start, end)
    return jsonify(result)


@app.route('/api/v1/library/genres', methods=['GET'])
def get_genres():
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    result = {'children': []}
    with Genres() as genres_manager:
        groups = genres_manager.get_genre_groups()
        for group in groups['genregroups']:
            group['children'] = []
            genres = genres_manager.get_genres_by_group(group['gid'])
            for genre in genres['genres']:
                group['children'].append(genre)
            result['children'].append(group)
    return jsonify(result)


@app.route('/api/v1/library/languages')
def get_all_languages():
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    with Books() as books:
        langs = books.get_all_languages()

    return jsonify(rows=langs)


@app.route('/api/v1/library/books/bygenre/<int:gid>/<lang>/<hide>')
def find_books_bygenre(gid, lang, hide):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    """'AID': None, 'BID': None, 'SERIE_NAME':None, 'SERIE_NUMBER': None, 'GENRE': None,'FILE': None, 'EXT': None,
    'DEL': None, 'LANG': None, 'SIZE': None, 'DATE':None, 'PATH':None})"""
    data = []
    with Books() as books_manager:
        books_result = books_manager.find_by_gid_sp(gid, lang,  True if hide=="true" else False)
    authors = books_result['authors']
    series = books_result['series']
    books_by_serie = books_result['books_by_serie']
    books_no_serie = books_result['books_no_serie']
    for author in authors:
        author_tmp_arr = [change_level({'TITLE': author["FULLNAME"], 'type': 'author'}, 0)]
        tmp_series = filter(lambda x: x['AID'] == author['AID'], series)
        for serie in tmp_series:
            serie_tmp_arr = [change_level({'TITLE': serie['SERIE_NAME'], 'type': 'serie'}, 1)]
            author_tmp_arr = author_tmp_arr + serie_tmp_arr + [change_level(book, 2) for book in books_by_serie if
                                                               book['SERIE_NAME'] == serie['SERIE_NAME'] and book[
                                                                   'AID'] == serie['AID']]
        noseq = [change_level(book, 1) for book in books_no_serie if book['AID'] == author['AID']]
            # noseq = sorted(noseq, key=lambda book: book['TITLE'])
        data = data + author_tmp_arr + noseq

    return jsonify(rows=data)


@app.route('/api/v1/library/books/byauthor/<int:aid>/<lang>/<hide>')
def find_books_byauthor(aid, lang, hide):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    """'AID': None, 'BID': None, 'SERIE_NAME':None, 'SERIE_NUMBER': None, 'GENRE': None,'FILE': None, 'EXT': None,
    'DEL': None, 'LANG': None, 'SIZE': None, 'DATE':None, 'PATH':None})"""
    data = []
    with Books() as books_manager:
        books_result = books_manager.find_by_author(aid, lang, True if hide=="true" else False)

    books = books_result['rows']
    series = list(
        set([book['SERIE_NAME'] for book in books if
             book['SERIE_NAME'] is not None and len(book['SERIE_NAME']) > 0]))
    series.sort()
    noseq = [change_level(book, 0) for book in books if book['SERIE_NAME'] is None or len(book['SERIE_NAME']) == 0]
    noseq = sorted(noseq, key=lambda book: book['TITLE'])
    for serie_name in series:
        tmp_arr = [change_level({'TITLE': serie_name, 'type': 'serie'}, 0)]
        data = data + tmp_arr + [change_level(book, 1) for book in books if book['SERIE_NAME'] == serie_name]

    books_result['rows'] = data + noseq
    return jsonify(books_result)


@app.route('/api/v1/library/books/byserie/<int:sid>/<lang>/<hide>')
def find_books_byserie(sid, lang, hide):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")
    """'AID': None, 'BID': None, 'SERIE_NAME':None, 'SERIE_NUMBER': None, 'GENRE': None,'FILE': None, 'EXT': None,
    'DEL': None, 'LANG': None, 'SIZE': None, 'DATE':None, 'PATH':None})"""
    data = []
    with Books() as books_manager:
        books_result = books_manager.find_by_sid(sid, lang,  True if hide=="true" else False)
    books = books_result['rows']
    aids = list(set([str(book["AID"]) for book in books]))
    with Authors() as authors_manager:
        authors_result = authors_manager.find_by_ids(aids)

    authors = authors_result['rows']
    authors = sorted(authors, key=lambda author: author["FULLNAME"])
    for author in authors:
        tmp_arr = [change_level({'TITLE': author["FULLNAME"], 'type': 'author'}, 0)]
        data = data + tmp_arr + [change_level(book, 1) for book in books if book['AID'] == author['AID']]

    books_result['rows'] = data
    return jsonify(books_result)


@app.route('/api/v1/library/books/download/<int:bid>/<folder_name>/<file_name>')
def get_download_info(bid, folder_name, file_name):
    if not Authentication.check_token('library', request):
        return jsonify(error="access denied")

    jdata = PCloudService.get_direct_link(folder_name, file_name)
    if jdata and jdata["result"] is 0:
        url = ""
        if jdata["hosts"]:
            url = "http://" + jdata["hosts"][0] + jdata["path"]
            response = requests.get(url)
            if response.ok:
                result = make_response(response.content)
                result.headers['Content-Type'] = 'application/zip'
                result.headers['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
                return result
    return jsonify(jdata)
"""Library api end """


# @app.route('/api/v1/public/test')
# def test():
#     jdata = PCloudService.get_link("fb2-000024-030559", "24.fb2.zip")
#     if jdata and jdata["result"] is 0:
#         url = ""
#         if jdata["hosts"]:
#             url = "//" + jdata["hosts"][0] + jdata["path"]
#         return render_template_string("<a href='{}'>24.fb2.zip</a>".format(url))
#     return jsonify(jdata)


"""admin api start"""


@app.route('/api/v1/admin/users/', defaults={'uid': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@app.route('/api/v1/admin/users/<int:uid>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def proccess_user(uid):
    if not Authentication.check_token('admin', request):
        return jsonify(error="access denied")
    result = None
    if request.method == 'GET' and uid is None:
        with Users() as users:
            result = {"users": users.get_users()}
    elif request.method == 'POST' and uid is None:
        user = json.loads(request.data)
        modules = map(lambda x: x["mid"], user["modules"])
        with Users() as users:
            result = {
                'uid': users.create_new(user["email"], user["display"], user["password"], user["role"], modules)}
    elif request.method == 'GET' and uid is not None:
        with Users() as users:
            result = users.get_user(uid)
    elif request.method == 'PUT' and uid is not None:
        user = json.loads(request.data)
        with Users() as users:
            result = {"uid": users.update_user(uid, user)}
    elif request.method == 'DELETE' and uid is not None:
        with Users() as users:
            result = {"uid": users.delete_user(uid)}
    else:
        result = {"error": "wrong parameters"}
    return jsonify(result)


@app.route('/api/v1/admin/modules', methods=['GET'])
def proccess_modules():
    if not Authentication.check_token('admin', request):
        return jsonify(error="access denied")
    with Users() as users:
        modules = users.get_modules()

    return jsonify(result=modules)


@app.route('/api/v1/admin/constants/<constant>', methods=['GET'])
def proccess_constants(constant):
    if not Authentication.check_token('admin', request):
        return jsonify(error="access denied")
    return jsonify(result=cfg.GLOBAL[constant])


"""unremark when needd t oadd admin
@app.route('/api/v1/admin/users/new/<email>/<display>/<password>/<role>/', defaults={'modules': None})
@app.route('/api/v1/admin/users/new/<email>/<display>/<password>/<role>/<modules>')
def new_user(email, display, password, role, modules):
    with Users() as users:
        result = users.create_new(email, display, password, role, modules)
    return jsonify(result)
"""


@app.route('/api/v1/public/authenticate', methods=['POST'])
def authenticate():
    if request.data is not None and "email" in request.data and "password" in request.data:
        login_params = json.loads(request.data)

        with Users() as users:
            result = users.login(login_params["email"], login_params["password"])
        return jsonify(result)

    return jsonify(error="Wrong credentials, please check email/password")


"""pcloud authenticate account"""


@app.route('/connect')
def connect():
    if not Authentication.check_token('admin', request):
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
