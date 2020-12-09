# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestFeedbackController(BaseTestCase):
    """FeedbackController integration test stubs"""

    def test_click_get(self):
        """Test case for click_get

        Click-through redirector for capturing implicit feedback
        """
        response = self.client.open(
            '//click/{query}/{url}'.format(query='query_example', url='url_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
