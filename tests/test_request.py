from .base import BaseTestCase


class TestBaseRequest(BaseTestCase):
    def test_api_version(self):
        self.assertEqual(self.base_request.api_version, '/v2')

    def test_base_url(self):
        self.assertEqual(
            self.base_request.api_url,
            'https://api.semaphoreci.com/v2',
        )

    def test_make_url(self):
        self.assertEqual(
            self.base_request._make_url('/v3'),
            'https://api.semaphoreci.com/v3'
        )

    def test_fails_with_bad_url(self):
        """Checks whether make url raises AssertionError
        if an argument wasn't valid

            Args::
                request_client Fixture of Request instance
        """
        self.assertRaises(AssertionError, self.base_request._make_url, '1')
