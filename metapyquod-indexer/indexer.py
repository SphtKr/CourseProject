#!/usr/bin/env python3

import sys
import os
import shutil
import re
import argparse
import magic
from bs4 import BeautifulSoup
from metapy import index

class ScrapedDocument:
    def __init__(self, title, text, mtime, url):
        self.title = title
        self.text = text
        self.mtime = mtime
        self.url = url

def main():
    parser = init_argparse()
    args = parser.parse_args()

    corpus_id = 'sham' #TODO: Get id from args

    sham_dat_path,sham_md_path = make_sham_corpus(corpus_id)

    with open(sham_dat_path,'w') as sham_dat, open(sham_md_path,'w') as sham_md:
        doc_num = 0
        for protocol in os.listdir(args.mirror_path):
            pdir = os.path.join(args.mirror_path,protocol)
            if not(os.path.isdir(pdir)):
                continue
            for root,dirnames,filenames in os.walk(pdir):
                #print(root, dirnames, filenames)
                for f in filenames:
                    fullpath = os.path.join(root,f)
                    mtime = os.path.getmtime(fullpath)
                    m = magic.from_file(fullpath, mime=True)

                    # Reconstitute URL...
                    hostandpath = root[len(pdir)+1:]
                    url = "{}://{}/{}".format(protocol,hostandpath,f) 

                    doc = ScrapedDocument(f, None, mtime, url)
                    doc_num += 1
                    #print(doc_num)

                    #DELETE ME!
                    #if doc_num > 183:
                    #    break

                    if(m == "text/html"):
                        doc = slurp_html(fullpath, doc)

                    #print(doc.title, doc.url, doc.mtime, doc.text)

                    if(not(doc.text is None)):
                        sham_dat.write(doc.text)
                        sham_dat.write('\n')
                        sham_md.write('\t'.join([re.sub('\s+',' ',doc.title), doc.url, str(doc.mtime)]))
                        sham_md.write('\n')

    cleanup_sham_corpus(corpus_id, args.dest_path)


def make_sham_corpus(id: str='sham'):
    sham_path = os.path.join("/tmp",id)

    sham_main_toml = """prefix = "."
stop-words = "./lemur-stopwords.txt"
dataset = "%s"
corpus = "line.toml"
index = "./idx"
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]

[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
"""%(id)

    sham_line_toml = """type = "line-corpus"
encoding = "utf-8"
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]
"""

    sham_main_toml_path = os.path.join(sham_path, "%s.toml"%(id))
    sham_line_toml_path = os.path.join(sham_path, id, "line.toml")
    sham_dat_path = os.path.join(sham_path, id, "%s.dat"%(id))
    sham_md_path = os.path.join(sham_path, id, "metadata.dat")

    os.mkdir(sham_path)
    os.mkdir(os.path.join(sham_path, id))
    with open(sham_main_toml_path,'w') as f:
        f.write(sham_main_toml)
        f.write('\n')

    with open(sham_line_toml_path,'w') as f:
        f.write(sham_line_toml)
        f.write('\n')

    shutil.copyfile("lemur-stopwords.txt", os.path.join(sham_path, "lemur-stopwords.txt"))

    #os.mkfifo(sham_dat_path)
    #os.mkfifo(sham_md_path)
    return sham_dat_path,sham_md_path
    #with open(sham_dat_path,'w') as sham_dat, open(sham_md_path,'w') as sham_md:

def cleanup_sham_corpus(id: str='sham', dest: str=None):
    sham_path = os.path.join("/tmp",id)
    sham_main_toml_path = os.path.join(sham_path, "%s.toml"%(id))
    sham_line_toml_path = os.path.join(sham_path, id, "line.toml")
    sham_dat_path = os.path.join(sham_path, id, "%s.dat"%(id))
    sham_md_path = os.path.join(sham_path, id, "metadata.dat")
    
    oldpath = os.getcwd()
    os.chdir(sham_path)
    index.make_inverted_index(sham_main_toml_path)
    os.chdir(oldpath)

    with open(sham_main_toml_path,'r') as f:
        config_toml = ''.join(f.readlines())
    config_toml = re.sub('(prefix|index|stop-words) = ".', "\\1 = \"%s"%(dest), config_toml)
    
    os.remove(sham_main_toml_path)
    os.remove(sham_md_path)
    os.remove(sham_dat_path)
    shutil.move(sham_path, dest)

    with open(os.path.join(dest,"config.toml"),'w') as f:
        f.write(config_toml)

    #os.remove(sham_line_toml_path)
    #os.remove(sham_main_toml_path)
    #os.rmdir(sham_path)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] mirrorpath destination",
        description="Build MeTA indexes from wget mirrors."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = "MeTAPyquod wget mirror indexer version 0.1.0"
    )
    parser.add_argument('mirror_path',
        metavar='mirrorpath',
        type=str,
        help='The path where the root of the mirror is stored. Should contain protocol directories like "http" and "https".')
    parser.add_argument('dest_path',
        metavar='dest',
        type=str,
        help='The directory location into which the created index will be stored.')
    parser.add_argument('-i',
        '--id',
        type=str,
        help='The identifier for the index.')
    return parser

def slurp_html(path: str=None, doc: ScrapedDocument=None):
    with open(path) as fp:
        soup = BeautifulSoup(fp, "html.parser")

        try:
            doc.title = str(soup.title.string)
        except:
            pass

        for script in soup(["script", "style"]):
            script.decompose()

        doc.text = re.sub('\s+',' ', soup.get_text(separator=' '))
        return doc

if __name__ == '__main__':
    main()

