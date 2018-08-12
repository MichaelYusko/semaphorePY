import json
import unittest

from mock import MagicMock

from semaphore.client import BaseRequest, Semaphore


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases"""
    def setUp(self):
        self.base_request = BaseRequest('Api-token')
        self.semaphore = Semaphore('Api-Token')
        self.json_data = json.dumps([{'id': '31312312312', 'name': 'Mike'}])
        self.mock_data = MagicMock(
            status_code=200,
            json_data=self.json_data
        )

    def tearDown(self):
        pass

    def return_assert(self, request, func):
        request.get.return_value = self.mock_data
        return self.assertTrue(self.json_data, func)
