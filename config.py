#!/usr/bin/env python
# coding=utf-8

DB = {
    "host": "127.0.0.1",
    "servername": "localhost",
    "dbname": "simple_library",
    "username": "library_admin",
    "password": "123456",
    "main_table": "lib_books",
    "inp_table": "inp_list",
    "authors_table": "lib_authors",
    "genres_table": "lib_genres",
    "series_table": "lib_series",
    "author2book": "lib_author2book",
    "genre2book": "lib_genre2book",
    "genre2group": "lib_genre2group",
    "serie2book": "lib_serie2book",
    "module2user": "portal_module2user",
    "modules": "portal_modules",
    "users": "portal_users",
    "modulesByUser": "view_modulesByUser",
    "authorsByBook": "view_authorsByBook",
    "booksByAuthor": "view_booksByAuthor",
    "booksByGenre": "view_booksByGenre",
    "booksBySerie": "view_booksBySerie",
    "seriesByBook": "view_seriesByBook",
    "allUsers": "view_AllUsers",
    "charset": "utf8"

}

LIBRARY = {
    "archives_path": "/media/olmer/Documents - HDD4/_Lib.rus.ec - Официальная/lib.rus.ec",
    "inpx_file": "/media/olmer/Documents - HDD4/_Lib.rus.ec - Официальная/librusec_local_fb2.inpx",
    "library_files": "/home/olmer/library_files"
}

PCLOUD = {
    "client_id": "R3Qp2U2jzLz",
    "client_secret": "XnuHTHSaCBQ4RJtl3vyYxm2R2rok",
    "access_token": "fAJLZR3Qp2U2jzLzZCKltq7ZqARlEFYiSmuXklWlY83PkR8Y3zgk",
    "authorize_url": "https://my.pcloud.com/oauth2/authorize",
    "api_url": "https://api.pcloud.com",
    "redirect_uri": "http://localhost:5000/getcode",
    "methods": {
        "o2token": {"name": "oauth2_token"},
        "listfolder": {"name": "listfolder", "params": {"path": "/"}},
        "getfilelink": {"name": "getfilelink", "params": {"path": "/%s/%s"}}
    }
}

GLOBAL = {
    "secret_key": "lib.rus.ec.forever",
    "user_role": ("user", "admin")
}
