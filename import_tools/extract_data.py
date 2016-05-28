#!/usr/bin/env python
# coding=utf-8

import config as cfg
import zipfile
import os
import models.book_info as book_info
import models.books as books
from tqdm import trange

books_manager = None


def parse_multiple_value(value):
    tmp_arr = [field.replace(",", " ").rstrip() if len(field) > 0 else None for field in
               value.split(":")]
    return tmp_arr


def work_on_author(info):
    global books_manager
    if info and info._author:
        for author in parse_multiple_value(info._author):
            if author:
                aid = books_manager.is_author_exist(author)
                if aid is None:
                    aid = books_manager.insert_author(author)
                books_manager.insert_author2book(aid, info._bid)


def work_on_serie(info):
    global books_manager
    if info and info._series is not None and len(info._series) > 0:
        sid = books_manager.is_serie_exist(info._series)
        if sid is None:
            sid = books_manager.insert_serie(info._series)
        books_manager.insert_serie2book(sid, info._bid, info._serno)


def work_on_genre(info):
    global books_manager
    if info and info._genre:
        for genre in parse_multiple_value(info._genre):
            if genre:
                gid = books_manager.is_genre_exist(genre)
                books_manager.insert_genre2book(gid, info._bid)


def create_all_tables():
    global books_manager
    all_books = books_manager.get_all_books()
    lst_len = len(all_books)
    if all_books is not None and lst_len > 0:
        for i in trange(lst_len, desc='fill other tables'):
            info = book_info.BookInfo()
            info.load_from_row_partial(all_books[i])
            # authors
            work_on_author(info)
            # series
            work_on_serie(info)
            # genres
            work_on_genre(info)


def extract_file(zip, path, filename):
    # print "extract file from zip and create new archive"
    try:
        newpath = zip.extract(filename, path)
        zipfile_path = "{0}{1}".format(newpath, ".zip")
        with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
            myzip.write(newpath, filename)
        os.remove(newpath)
    except Exception as error:
        print(error)


def create_folder(filename):
    # print "create new library folder"
    newpath = "{0}/{1}".format(cfg.LIBRARY["library_files"], filename.replace(".inp", ""))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def find_zip(filename):
    # print "find and open zip file"
    filename = filename.replace(".inp", ".zip")
    zip_filepath = "{0}/{1}".format(cfg.LIBRARY["archives_path"], filename)
    if not os.path.exists(zip_filepath):
        return None
    return zipfile.ZipFile(zip_filepath, 'r')


def parse_inpx(inpx):
    global books_manager
    if inpx is None:
        return
    # print "parse inpx file"
    infolist = inpx.infolist()
    for i in trange(len(infolist), desc='parse inpx file'):
        inp = infolist[i]
        if inp.filename.startswith("fb2"):
            doc = inpx.read(inp.filename)
            zip = find_zip(inp.filename)
            if doc is not None and zip is not None and not books_manager.is_inp_exist(inp.filename):
                inp_id = books_manager.add_inp(inp.filename)
                path = create_folder(inp.filename)
                lines = doc.splitlines()
                for j in trange(len(lines)):
                    line = lines[j]
                    info = book_info.BookInfo()
                    info.load_from_line(line)
                    info.set_path(inp.filename.replace(".inp", ""))
                    fnd_info = books_manager.find_by_file(info._libid, info._file)
                    if fnd_info is None or fnd_info._bid is None:
                        bid = books_manager.save_book(info)
                        if  bid is not None:
                            info.set_bid(bid)
                            extract_file(zip, path, "{0}.{1}".format(info._file, info._ext))
                            # authors
                            work_on_author(info)
                            # series
                            work_on_serie(info)
                            # genres
                            work_on_genre(info)
                    # else:
                    #     # authors
                    #     work_on_author(fnd_info)
                    #     # series
                    #     work_on_serie(fnd_info)
                    #     # genres
                    #     work_on_genre(fnd_info)
                    #     books_manager.update_book(info, fnd_info._bid)
                books_manager.update_inp(inp_id)
            zip.close()


def open_inpx():
    print "open inpx file"
    zip_inpx = None
    try:
        zip_inpx = zipfile.ZipFile(cfg.LIBRARY["inpx_file"], 'r')
    except:
        pass
    return zip_inpx


def start_process():
    global books_manager
    with books.Books() as books_manager:
        inpx = open_inpx()
        parse_inpx(inpx)
        if inpx:
            inpx.close()
        #   create_all_tables()
        print "end of process"


def stop_process():
    global books_manager
    books_manager.close()


if __name__ == "__main__":
    start_process()
