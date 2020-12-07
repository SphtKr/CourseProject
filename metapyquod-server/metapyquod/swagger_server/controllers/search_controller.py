import connexion
import six
import metapy

from swagger_server.models.query_params import QueryParams  # noqa: E501
from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server import util
#from swagger_server import appEngine

import swagger_server.engine

def search_get(query, top=None, skip=None):  # noqa: E501
    """Retrieve results for a given query

     # noqa: E501

    :param query: Query content
    :type query: str
    :param top: Return this many results (pagination)
    :type top: int
    :param skip: Skip this many results (pagination)
    :type skip: int

    :rtype: List[QueryResult]
    """
    metapy.log_to_stderr()
    idx = metapy.index.make_inverted_index("./config.toml")
    ranker = metapy.index.OkapiBM25()
    #ranker = metapy.index.PivotedLength()
    qdoc = metapy.index.Document()
    qdoc.content(query)
    ranking = ranker.score(idx, qdoc, skip + top)[skip:]
    qresult = ranking #appEngine.query(query, skip, top)
    result = []
    for r in qresult:
        url = idx.metadata(r[0]).get('url')
        result.append(QueryResult(doc_id= r[0], url= url, score= r[1]))
    return result


def search_post(body):  # noqa: E501
    """Retrieve results for a given query

     # noqa: E501

    :param body: Search parameters
    :type body: dict | bytes

    :rtype: List[QueryResult]
    """
    if connexion.request.is_json:
        body = QueryParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
