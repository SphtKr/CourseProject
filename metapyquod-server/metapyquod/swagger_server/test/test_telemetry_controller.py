# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.query_result import QueryResult  # noqa: E501
from swagger_server.models.stats_result import StatsResult  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTelemetryController(BaseTestCase):
    """TelemetryController integration test stubs"""

    def test_telemetry_recent_get(self):
        """Test case for telemetry_recent_get

        Get the most recently indexed documents.
        """
        response = self.client.open(
            '//telemetry/recent',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_telemetry_stats_get(self):
        """Test case for telemetry_stats_get

        Get statistics about the search index.
        """
        response = self.client.open(
            '//telemetry/stats',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
