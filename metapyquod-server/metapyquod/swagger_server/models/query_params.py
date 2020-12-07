# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class QueryParams(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, query: str=None, top: int=10, skip: int=0):  # noqa: E501
        """QueryParams - a model defined in Swagger

        :param query: The query of this QueryParams.  # noqa: E501
        :type query: str
        :param top: The top of this QueryParams.  # noqa: E501
        :type top: int
        :param skip: The skip of this QueryParams.  # noqa: E501
        :type skip: int
        """
        self.swagger_types = {
            'query': str,
            'top': int,
            'skip': int
        }

        self.attribute_map = {
            'query': 'query',
            'top': 'top',
            'skip': 'skip'
        }
        self._query = query
        self._top = top
        self._skip = skip

    @classmethod
    def from_dict(cls, dikt) -> 'QueryParams':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QueryParams of this QueryParams.  # noqa: E501
        :rtype: QueryParams
        """
        return util.deserialize_model(dikt, cls)

    @property
    def query(self) -> str:
        """Gets the query of this QueryParams.

        Query content  # noqa: E501

        :return: The query of this QueryParams.
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query: str):
        """Sets the query of this QueryParams.

        Query content  # noqa: E501

        :param query: The query of this QueryParams.
        :type query: str
        """

        self._query = query

    @property
    def top(self) -> int:
        """Gets the top of this QueryParams.

        Return this many results (pagination)  # noqa: E501

        :return: The top of this QueryParams.
        :rtype: int
        """
        return self._top

    @top.setter
    def top(self, top: int):
        """Sets the top of this QueryParams.

        Return this many results (pagination)  # noqa: E501

        :param top: The top of this QueryParams.
        :type top: int
        """

        self._top = top

    @property
    def skip(self) -> int:
        """Gets the skip of this QueryParams.

        Skip this many results (pagination)  # noqa: E501

        :return: The skip of this QueryParams.
        :rtype: int
        """
        return self._skip

    @skip.setter
    def skip(self, skip: int):
        """Sets the skip of this QueryParams.

        Skip this many results (pagination)  # noqa: E501

        :param skip: The skip of this QueryParams.
        :type skip: int
        """

        self._skip = skip
