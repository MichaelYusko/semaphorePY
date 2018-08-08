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
            api_token(str): A authentication token from Semaphore service

        Constants::
            BASE_URL: basic Semaphore API url
            API_VERSION: Semaphore's API version
            RESOURCE: Name of a particular resource

        Properties::
            api_url: Makes full url for HTTP calls, based on current API version


        Methods::
            _make_url(str): Makes API url for specific API version
            _get(requests object): Makes HTTP GET request.
    """

    def __init__(self, api_token):
        self.token = api_token
        self._default_headers = {'Authorization': f'Token {self.token}'}

    _BASE_URL = 'https://api.semaphoreci.com'
    _API_VERSION = '/v2'
    _RESOURCE = None

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

    def _make_url(self, api_version: str) -> str:
        """Makes API's url for specific API version

            Returns::
                Url with specific version
        """
        assert api_version.startswith('/'), f'URL must be looks like /v{api_version}'
        return self._BASE_URL + api_version

    def _make_request(self, method, resource: str=None, only_status=False, **kwargs):
        """Factory method for HTTP requests

            Args::
                method(requests object): an HTTP request
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An JSON response
        """
        resource = '/' + resource if resource else ''
        url = self.api_url + '/' + resource

        if only_status:
            return method(url, headers=self._default_headers, **kwargs).status_code

        return method(url, headers=self._default_headers, **kwargs).json()

    def _get(self, resource: str=None, **kwargs):
        """Makes HTTP(GET) request for basic Semaphore's API url

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(requests.get, resource, **kwargs)

    def _post(self, resource: str=None, **kwargs):
        """Makes HTTP(POST) request

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(requests.post, resource, **kwargs)

    def _delete(self, resource: str=None, **kwargs):
        """Makes HTTP(DELETE) request

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(
            requests.delete,
            resource,
            only_status=True,
            **kwargs
        )

    def _patch(self, resource: str=None, **kwargs):
        """Makes HTTP(POST) request

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(requests.patch, resource, **kwargs)


class SemaphoreBaseResource(BaseRequest):
    """Basic wrapper class for Semaphore API

        Args::
            api_token(str): A authentication token from Semaphore service

        Methods::
            default_resources(boolean): Returns available Semaphore's API resources
    """
    def __init__(self, api_token: str):
        super().__init__(api_token)

    def default_resources(self, as_list: bool=False):
        """Returns all available Semaphore resources

            Args::
                as_list(boolen): Returns a dictionary with all available resources
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
            api_token(str): A authentication token from Semaphore service

        Methods::
            list: Returns an array with organization objects
            by_name(str): Return a organization by name
    """

    _RESOURCE = 'orgs'

    def __init__(self, api_token: str):
        super().__init__(api_token)

    def list(self):
        """Returns an array with organization objects"""
        return self._get(resource=self._RESOURCE)

    def by_name(self, user_name: str):
        """Searches a organization by username

            Args::
                user_name(str): A username of a organization

            Returns::
                A dictionary object with organization info
                otherwise error object
        """
        resource = f'{self._RESOURCE}/{user_name}'
        return self._get(resource=resource)

    def urls(self, username):
        """Returns a organization project urls

            Args::
                username A username of a organization

            Returns::
                An array with urls
        """
        resource = f'{self._RESOURCE}/{username}/projects'
        return self._get(resource=resource)

    def secret_urls(self, username):
        """Returns a organization project secret urls

            Args::
                username(str): A username of a organization

            Returns::
                An array with urls
        """
        resource = f'{self._RESOURCE}/{username}/secrets'
        return self._get(resource=resource)

    def users(self, username: str):
        """Returns all users of a organization

            Args::
                username(str): A username of a organization

            Returns::
                An array with user objects
        """
        resource = f'{self._RESOURCE}/{username}/users'
        return self._get(resource=resource)


class TeamResource(SemaphoreBaseResource):
    """Team resource class

        Args::
             api_token(str): A authentication token from Semaphore service

        Methods::
            all(str): Returns all team objects by username
    """
    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'teams'
    ALLOWED_PERMISSIONS = ('read', 'edit', 'admin')

    def __check_permission(self, permission: str):
        """Checks if permission is allowed

            Args::
                permission(str): A permission argument for POST/PATCH methods
        """
        if permission not in self.ALLOWED_PERMISSIONS:
            raise ValueError('Permission argument must be "read", "edit" or "admin"')

    def all(self, username):
        """Returns all teams objects, with related information

            Args::
                username(str): All related teams to username

            Returns::
                An array with team objects information
        """
        resource = f'orgs/{username}/{self._RESOURCE}'
        return self._get(resource=resource)

    def by_id(self, team_id: str):
        """Returns a team by id

            Args::
                team_id(str): A team ID which need to find

            Returns::
                A dictionary with team object
        """
        resource = f'{self._RESOURCE}/{team_id}'
        return self._get(resource=resource)

    def by_project(self, project_id: str):
        """Returns teams by project ID

            Args::
                project_id(str): A project ID which need to find

            Returns::
                An array with team objects
        """
        resource = f'projects/{project_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def secrets(self, secret_id: str):
        """Returns teams by secrets

            Args::
                secret_id(str): A secret ID which need to find

            Returns::
                An array with team objects
        """
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def create(self, organization_username: str, update=False, **kwargs):
        """Creates a team for a organization

            Args::
                organization_username A username of organization
                for which will be created a team

            Extra Arguments::
                name(str): Name for a team
                permission(str): Set permission for a team
                Notice that only three type of permission are allowed
                "read", "edit" and "admin"
                description(str): An description for a team

        """

        self.__check_permission(kwargs['permission'])
        data = {
            'name': kwargs['name'],
            'permission': kwargs['permission'],
            'description': kwargs['description']
        }

        resource = f'orgs/{organization_username}/{self._RESOURCE}'
        return self._post(resource=resource, json=data)

    def update(self, team_id: str, permission: str, name=None, desc=None):
        """Updates a team by id

            Args::
                team_id(str): ID of a team which will be updated
                permission(str): Set a new permissions for a team
                name(str): Set a new name for a team
                desc(str): Set a description for a team

            Returns::
                A dictionary object with team information
        """
        self.__check_permission(permission)
        data = {
            'name': name,
            'description': desc,
            'permission': permission
        }
        resource = f'{self._RESOURCE}/{team_id}'
        return self._patch(resource=resource, json=data)

    def delete(self, team_id: str):
        """Delete a team from organization by team ID

            Args::
                team_id(str): A team ID which will be deleted

            Returns::
                A HTTP status code
        """
        resource = f'{self._RESOURCE}/{team_id}'
        return self._delete(resource=resource)


class Semaphore(SemaphoreBaseResource):
    """Main wrapper class"""
    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.organization = OrganizationResource(api_token)
        self.teams = TeamResource(api_token)
