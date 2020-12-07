import connexion
import six
from connexion.lifecycle import ConnexionResponse

import metapy

from swagger_server import util
#from swagger_server import appEngine


def click_get(query, url):  # noqa: E501
    """Click-through redirector for capturing implicit feedback

     # noqa: E501

    :param query: Original query content
    :type query: str
    :param url: URL of selected result
    :type url: str

    :rtype: None
    """

    idx = metapy.index.make_inverted_index("./config.toml")
    url = idx.metadata(idx.docs()[int(url)]).get("url")

    #FIXME: Validate that URL is something from the index metadata!
    response = ConnexionResponse(status_code=302, headers={'Location': url}) #,"X-Debug": r[0]["url"]})
    
    return response
    #return 'do some MAGIC with {} and {}!'.format(query, url)
