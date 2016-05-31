#!/usr/bin/env python
# coding=utf-8


def change_level(obj, level):
    if obj:
        obj['$$treeLevel'] = level

    return obj