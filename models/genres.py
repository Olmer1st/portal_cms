#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.dbconnection import mysql_connection


class Genres(object):
    def __init__(self):
        self.connection = mysql_connection()

    def get_genre_groups(self):
        sql = "SELECT * FROM {0}".format(cfg.DB["allGenreGroups"])
        rows = self.connection.execute_fetch(sql, False)
        return {'genregroups': rows}

    def get_genres(self):
        sql = "SELECT * FROM {0}".format(cfg.DB["allGenres"])
        rows = self.connection.execute_fetch(sql, False)
        return {'genres': rows}

    def get_genres_by_group(self, gidm):
        sql = "SELECT * FROM {0} WHERE GIDM = {1}".format(cfg.DB["genreByGenreGroup"], gidm)
        rows = self.connection.execute_fetch(sql, False)
        return {'genres': rows}

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
