"""
:COPYRIGHT: Michael Yusko @ 2018
:LICENSE: MIT(see license file)
"""


__all__ = ['Semaphore']


class Request:
    """Class which responds for execution HTTP calls
    and contains Semaphore API version, basic Semaphore API URL and etc.

        Constants::
            BASE_URL basic Semaphore API url
            API_VERSION Semaphore's API version

        Properties::
            api_url Makes full url for HTTP calls, based on current API version

        Methods::
            make_url Makes API url for specific API version
    """
    _BASE_URL = 'https://api.semaphoreci.com'
    _API_VERSION = '/v1'

    @property
    def api_url(self) -> str:
        """Makes API URL

            Returns::
                string API's url with current API version
        """
        return self._BASE_URL + self._API_VERSION

    @property
    def api_version(self) -> str:
        """Shows current API version

            Returns::
                string current API version
        """
        return self._API_VERSION

    def make_url(self, api_version: str) -> str:
        """Makes API's url for specific API version

            Returns::
                string API's url for specific version
        """
        assert api_version.startswith('/'), f'URL must be looks like /v{api_version}'
        return self._BASE_URL + api_version


class Semaphore(Request):
    """Basic wrapper class for Semaphore API"""
    pass
