# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class StatsResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, num_docs: int=None, num_terms: int=None):  # noqa: E501
        """StatsResult - a model defined in Swagger

        :param num_docs: The num_docs of this StatsResult.  # noqa: E501
        :type num_docs: int
        :param num_terms: The num_terms of this StatsResult.  # noqa: E501
        :type num_terms: int
        """
        self.swagger_types = {
            'num_docs': int,
            'num_terms': int
        }

        self.attribute_map = {
            'num_docs': 'num_docs',
            'num_terms': 'num_terms'
        }
        self._num_docs = num_docs
        self._num_terms = num_terms

    @classmethod
    def from_dict(cls, dikt) -> 'StatsResult':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StatsResult of this StatsResult.  # noqa: E501
        :rtype: StatsResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def num_docs(self) -> int:
        """Gets the num_docs of this StatsResult.

        The number of documents currently in the index  # noqa: E501

        :return: The num_docs of this StatsResult.
        :rtype: int
        """
        return self._num_docs

    @num_docs.setter
    def num_docs(self, num_docs: int):
        """Sets the num_docs of this StatsResult.

        The number of documents currently in the index  # noqa: E501

        :param num_docs: The num_docs of this StatsResult.
        :type num_docs: int
        """

        self._num_docs = num_docs

    @property
    def num_terms(self) -> int:
        """Gets the num_terms of this StatsResult.

        The number of terms currently in the index  # noqa: E501

        :return: The num_terms of this StatsResult.
        :rtype: int
        """
        return self._num_terms

    @num_terms.setter
    def num_terms(self, num_terms: int):
        """Sets the num_terms of this StatsResult.

        The number of terms currently in the index  # noqa: E501

        :param num_terms: The num_terms of this StatsResult.
        :type num_terms: int
        """

        self._num_terms = num_terms
