import connexion
import six

import metapy

from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server.models.stats_result import StatsResult  # noqa: E501
from swagger_server import util


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
    idx = metapy.index.make_inverted_index("./config.toml")
    model = StatsResult(num_docs= idx.num_docs(), num_terms= idx.unique_terms(), disk_size= 0)

    return model
