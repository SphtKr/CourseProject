import os
import metapy
import pytoml
from metapy import index #pylint: disable=E0611

class Engine:
    __ranker = None
    __idx = None
    __config = None
    __metadataDef = {}

    def __init__(self, configPath: str="./config.toml"):
        with open(configPath, 'rb') as fin:
            self.__config = pytoml.load(fin)

        self.__idx = index.make_inverted_index(configPath)

        mconfig = self.__config['metadata']
        self.__metadataDef = mconfig

        #TODO: There is no python binding for make_ranker for use with toml... reimplementing this would be straightforward but nontrivial. Just handle BM25 for now.
        rconfig = self.__config.get('ranker', {'method':'bm25'})
        if rconfig.get('method','bm25') == "bm25":
            k1 = rconfig.get("k1", 1.2)
            b = rconfig.get("b", 0.75)
            k3 = rconfig.get("k3", 500)
            self.__ranker = index.OkapiBM25(k1, b, k3)
        else:
            self.__ranker = index.OkapiBM25()
    
    def query(self, query: str=None, skip: int=0, top: int=10):
        #idx = metapy.index.make_inverted_index("./config.toml")
        qdoc = index.Document()
        qdoc.content(query)
        ranking = self.__ranker.score(self.__idx, qdoc, skip + top)[skip:]
        
        results = []
        for r in ranking:
            mdata = self.__idx.metadata(r[0])
            mdict = {}
            for f in self.__metadataDef:
                mdict[f['name']] = mdata.get(f['name'])
            results.append({
                "doc_id": str(r[0]),
                "score": r[1],
                "metadata": mdict,
            })

        return results
    
    def get_metadata_for_doc_id(self, n: str=""):
        doc = self.__idx.docs()[int(n)] #FIXME: This seems very bad for performance, no? Better way?
        mdata = self.__idx.metadata(doc)
        return mdata

    def get_stats(self):
        return {
            'num_docs': self.__idx.num_docs(),
            'num_terms': self.__idx.unique_terms(),
            'disk_size': 0 #TODO: calculate this outside metapy
        }