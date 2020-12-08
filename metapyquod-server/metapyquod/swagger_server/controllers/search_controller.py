import connexion
import six
import metapy

from swagger_server.models.query_params import QueryParams  # noqa: E501
from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server import util
from swagger_server import mainEngine

import swagger_server.engine

def search_get(query, top=None, skip=None):  # noqa: E501
    """Retrieve results for a given query

    :param query: Query content
    :type query: str
    :param top: Return this many results (pagination)
    :type top: int
    :param skip: Skip this many results (pagination)
    :type skip: int

    :rtype: List[QueryResult]
    """
    resultDicts = mainEngine.query(query, skip, top)
    result = []
    for r in resultDicts:
        result.append(QueryResult(doc_id= r["doc_id"], url= r["metadata"]["url"], score= r["score"], title=r["metadata"]["title"]))
    return result


def search_post(body):  # noqa: E501
    """Retrieve results for a given query

    :param body: Search parameters
    :type body: dict | bytes

    :rtype: List[QueryResult]
    """
    if connexion.request.is_json:
        body = QueryParams.from_dict(connexion.request.get_json())  # noqa: E501
    
    resultDicts = mainEngine.query(body.query, body.skip, body.top)
    result = []
    for r in resultDicts:
        result.append(QueryResult(doc_id= r["doc_id"], url= r["metadata"]["url"], score= r["score"], title=r["metadata"]["title"]))
    return result
