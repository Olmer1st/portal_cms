#!/usr/bin/env python
# coding=utf-8

import config as cfg
import zipfile
import os
import models.book_info as book_info
import models.books as books
from tqdm import tqdm


books_manager = None


def extract_file(zip, path, filename):
    # print "extract file from zip and create new archive"
    newpath = zip.extract(filename, path)
    zipfile_path = "{0}{1}".format(newpath,".zip")
    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(newpath,filename)
    os.remove(newpath)

def create_folder(filename):
    # print "create new library folder"
    newpath = "{0}/{1}".format(cfg.LIBRARY["library_files"],filename.replace(".inp",""))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return  newpath


def find_zip(filename):
    # print "find and open zip file"
    filename = filename.replace(".inp",".zip")
    zip_filepath = "{0}/{1}".format( cfg.LIBRARY["archives_path"], filename)
    if not os.path.exists(zip_filepath):
        return None
    return zipfile.ZipFile(zip_filepath, 'r')



def parse_inpx(inpx):
    global  books_manager
    print "parse inpx file"
    infolist = inpx.infolist()
    pbar1 = tqdm(infolist)
    for inp in pbar1:
        if inp.filename.startswith("fb2"):
            doc = inpx.read(inp.filename)
            zip = find_zip(inp.filename)
            # pbar1.set_description("Processing inpx file  %s" % inp.filename)
            if doc is not None and zip is not None:
                path = create_folder(inp.filename)
                lines = doc.splitlines()
                pbar2 = tqdm(lines)
                for line in pbar2:
                    info = book_info.BookInfo()
                    info.load_from_line(line)
                    fnd_info = books_manager.find_by_file(info._libid, info._file)
                    if fnd_info is None or fnd_info._bid is None:
                        if books_manager.save_book(info) is not None:
                            extract_file(zip, path, "{0}.{1}".format(info._file, info._ext))
                            # pbar2.set_description("Extracting book file  %s" % info.file_name())
                pbar2.close()
    pbar1.close()


def open_inpx():
    print "open inpx file"
    return zipfile.ZipFile(cfg.LIBRARY["inpx_file"], 'r')




def start_process():
    inpx = open_inpx()
    parse_inpx(inpx)
    print "end of process"


if __name__ == "__main__":
    with books.Books() as books_manager:
        start_process()
