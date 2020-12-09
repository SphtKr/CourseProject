# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.query_params import QueryParams  # noqa: E501
from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSearchController(BaseTestCase):
    """SearchController integration test stubs"""

    def test_search_get(self):
        """Test case for search_get

        Retrieve results for a given query
        """
        query_string = [('top', 2),
                        ('skip', 1)]
        response = self.client.open(
            '//search/{query}'.format(query='query_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_post(self):
        """Test case for search_post

        Retrieve results for a given query
        """
        body = QueryParams()
        response = self.client.open(
            '//search',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
