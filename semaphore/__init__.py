"""
:COPYRIGHT: Michael Yusko @ 2018
:LICENSE: MIT(see license file)
"""

import requests


__all__ = ['Semaphore']
__version__ = '0.0.1'
__author__ = 'Michael Yusko'


class BaseRequest:
    """Class which responds for execution HTTP calls
    and contains Semaphore API version, basic Semaphore API URL and etc.

        Args::
            api_token A authentication token from Semaphore service

        Constants::
            BASE_URL basic Semaphore API url
            API_VERSION Semaphore's API version


        Properties::
            api_url Makes full url for HTTP calls, based on current API version


        Methods::
            make_url(str) Makes API url for specific API version
            _get Makes HTTP GET request.
    """

    def __init__(self, api_token):
        self.token = api_token
        self._default_headers = {'Authorization': f'Token {self.token}'}

    _BASE_URL = 'https://api.semaphoreci.com'
    _API_VERSION = '/v2'

    @property
    def api_url(self) -> str:
        """Makes API URL

            Returns::
                API url
        """
        return self._BASE_URL + self._API_VERSION

    @property
    def api_version(self) -> str:
        """Shows current API version

            Returns::
                current Semaphore API version
        """
        return self._API_VERSION

    def make_url(self, api_version: str) -> str:
        """Makes API's url for specific API version

            Returns::
                Url with specific version
        """
        assert api_version.startswith('/'), f'URL must be looks like /v{api_version}'
        return self._BASE_URL + api_version

    def _make_request(self, method, resource: str=None, **kwargs):
        """Factory method for HTTP requests

            Args::
                method an HTTP request
                resource An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An JSON response
        """
        resource = '/' + resource if resource else ''
        url = self.api_url + '/' + resource
        return method(url, headers=self._default_headers, **kwargs).json()

    def _get(self, resource: str=None, **kwargs):
        """Makes HTTP(GET) request for basic Semaphore's API url

            Args::
                resource An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(requests.get, resource, **kwargs)


class SemaphoreBaseResource(BaseRequest):
    """Basic wrapper class for Semaphore API

        Args::
            api_token A authentication token from Semaphore service

        Methods::
            default_resources(boolean) Returns available Semaphore's API resources
    """
    def __init__(self, api_token: str):
        super().__init__(api_token)

    def default_resources(self, as_list: bool=False):
        """Returns all available Semaphore resources

            Args::
                as_list Returns a dictionary with all available resources
                default `False` if you set the flag as `True`, the method
                will return an array with link, which resources are available

            Returns::
                A dictionary object or
                an array(if flag `as_list` is `True`), with available resources
        """
        response = self._get()
        if as_list:
            return [value for value in response.values()]
        return response


class OrganizationResource(SemaphoreBaseResource):
    """Organization resource class

        Args::
            api_token A authentication token from Semaphore service

        Methods::
            list Returns an array with organization objects
            by_name(str) Return a organization by name
    """

    _BASE_RESOURCE = 'orgs'

    def __init__(self, api_token: str):
        super().__init__(api_token)

    def list(self):
        """Returns an array with organization objects"""
        return self._get(resource=self._BASE_RESOURCE)

    def by_name(self, user_name: str):
        """Searches a organization by username

            Args::
                user_name An username of a organization

            Returns::
                A dictionary object with organization info
                otherwise error object
        """
        resource = f'{self._BASE_RESOURCE}/{user_name}'
        return self._get(resource=resource)


class Semaphore(SemaphoreBaseResource):
    """Main wrapper class"""
    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.organization = OrganizationResource(api_token)


semaphore = Semaphore('WN_sz9weps1E9H1zmj8y')
print(semaphore.organization.by_name('mikezztest'))