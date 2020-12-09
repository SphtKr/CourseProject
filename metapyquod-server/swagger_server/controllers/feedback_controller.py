import connexion
import six
from connexion.lifecycle import ConnexionResponse

import metapy

from swagger_server import util
from swagger_server import mainEngine


def click_get(query, doc_id):  # noqa: E501
    """Click-through redirector for capturing implicit feedback

    :param query: Original query content
    :type query: str
    :param url: URL of selected result
    :type url: str

    :rtype: None
    """

    url = mainEngine.get_metadata_for_doc_id(doc_id).get("url")

    #FIXME: Validate that URL is something from the index metadata!
    response = ConnexionResponse(status_code=302, headers={'Location': url}) #,"X-Debug": r[0]["url"]})
    
    return response
    #return 'do some MAGIC with {} and {}!'.format(query, url)
