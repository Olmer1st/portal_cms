#!/usr/bin/env python
# coding=utf-8

import config as cfg
import zipfile
import os
import models.book_info as book_info
import models.books as books
from tqdm import trange

books_manager = None
# TODO - cont save authors might be split for details
def create_authors_table():
    global books_manager
    authors_list = books_manager.get_authors_from_books()
    lst_len=len(authors_list)
    if authors_list is not None and lst_len>0:
        for i in trange(lst_len, desc='fill authors table'):
            author_name = authors_list[i]
            if author_name:
                tmp_arr = author_name.split(":")


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
    # print "parse inpx file"
    infolist = inpx.infolist()
    for i in trange(len(infolist), desc='parse inpx file'):
        inp = infolist[i]
        if inp.filename.startswith("fb2"):
            doc = inpx.read(inp.filename)
            zip = find_zip(inp.filename)
            if doc is not None and zip is not None and not books_manager.is_inp_exist(inp.filename):
                inp_id= books_manager.add_inp(inp.filename)
                path = create_folder(inp.filename)
                lines = doc.splitlines()
                for j in trange(len(lines)):
                    line = lines[j]
                    info = book_info.BookInfo()
                    info.load_from_line(line)
                    fnd_info = books_manager.find_by_file(info._libid, info._file)
                    if fnd_info is None or fnd_info._bid is None:
                        if books_manager.save_book(info) is not None:
                            extract_file(zip, path, "{0}.{1}".format(info._file, info._ext))
                    else:
                        books_manager.update_book(info, fnd_info._bid)
                books_manager.update_inp(inp_id)
            zip.close()


def open_inpx():
    print "open inpx file"
    return zipfile.ZipFile(cfg.LIBRARY["inpx_file"], 'r')


def start_process():
    global books_manager
    with books.Books() as books_manager:
        inpx = open_inpx()
        parse_inpx(inpx)
        inpx.close()
        print "end of process"

def stop_process():
    global books_manager
    books_manager.close()

if __name__ == "__main__":
    start_process()
