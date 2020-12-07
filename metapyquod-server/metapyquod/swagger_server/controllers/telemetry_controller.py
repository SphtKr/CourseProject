import connexion
import six

import metapy

from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server.models.stats_result import StatsResult  # noqa: E501
from swagger_server import util
from swagger_server import mainEngine

def telemetry_recent_get():  # noqa: E501
    """Get the most recently indexed documents.

     # noqa: E501


    :rtype: List[QueryResult]
    """
    return 'do some magic!'


def telemetry_stats_get():  # noqa: E501
    """Get statistics about the search index.

     # noqa: E501


    :rtype: StatsResult
    """
    statsDict = mainEngine.get_stats()
    model = StatsResult(num_docs= statsDict['num_docs'], num_terms= statsDict['num_terms'], disk_size= statsDict['disk_size'])

    return model
