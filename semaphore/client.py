import requests as r


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
        return self._make_request(r.get, resource, **kwargs)

    def _post(self, resource: str=None, only_status=False, **kwargs):
        """Makes HTTP(POST) request

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(
            r.post,
            resource,
            only_status,
            **kwargs
        )

    def _delete(self, resource: str=None, **kwargs):
        """Makes HTTP(DELETE) request

            Args::
                resource(str): An Semaphore's API resource
                kwargs extra arguments

            Returns::
                An response from Semaphore API
        """
        return self._make_request(
            r.delete,
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
        return self._make_request(r.patch, resource, **kwargs)


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
            list: Returns an array with an organization objects
            by_name(str): Retrieve an organization by name
            urls(str): Retrieve urls of an organization
            secrets_url(str): Retrieve a secrets url of an organization
            users(str): Retrieve an users of an organization
    """

    _RESOURCE = 'orgs'

    def __init__(self, api_token: str):
        super().__init__(api_token)

    def list(self):
        """Returns an array with an organization objects"""
        return self._get(resource=self._RESOURCE)

    def by_name(self, user_name: str):
        """Searches an organization by username

            Args::
                user_name: A username of an organization

            Returns::
                A dictionary object with an organization info
                otherwise error object
        """
        resource = f'{self._RESOURCE}/{user_name}'
        return self._get(resource=resource)

    def urls(self, username):
        """Returns an organization project urls

            Args::
                username: A username of an organization

            Returns::
                An array with urls
        """
        resource = f'{self._RESOURCE}/{username}/projects'
        return self._get(resource=resource)

    def secret_urls(self, username):
        """Returns an organization project secret urls

            Args::
                username: A username of an organization

            Returns::
                An array with urls
        """
        resource = f'{self._RESOURCE}/{username}/secrets'
        return self._get(resource=resource)

    def users(self, username: str):
        """Returns all users of an organization

            Args::
                username: A username of an organization

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
            __check_permission(str): Checks if a permission is allowed
            for Semaphore API, otherwise raise the error.
            by_id(str): Retrieve a team by ID
            by_project(str): Retrieve a team by project ID
            secrets(str): Retrieve a team by secrets ID

            create(str, str, str): Create a team
            notice that `permission` argument must be
            one from  the ['read', 'edit', 'admin']
            otherwise raise the error.

            update(str): Update a team by ID
            delete(str): Delete a team by ID
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
                username: All related teams to username

            Returns::
                An array with team objects information
        """
        resource = f'orgs/{username}/{self._RESOURCE}'
        return self._get(resource=resource)

    def by_id(self, team_id: str):
        """Returns a team by id

            Args::
                team_id: A team ID which need to find

            Returns::
                A dictionary with team object
        """
        resource = f'{self._RESOURCE}/{team_id}'
        return self._get(resource=resource)

    def by_project(self, project_id: str):
        """Returns teams by project ID

            Args::
                project_id: A project ID which need to find

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
                organization_username: A username of an organization
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
                team_id: ID of a team which will be updated
                permission: Set a new permissions for a team
                name: Set a new name for a team
                desc: Set a description for a team

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
        """Delete a team from an organization by team ID

            Args::
                team_id: A team ID which will be deleted

            Returns::
                A HTTP status code
        """
        resource = f'{self._RESOURCE}/{team_id}'
        return self._delete(resource=resource)


class UsersResource(SemaphoreBaseResource):
    """Users resource class

        Args::
             api_token(str): A authentication token from Semaphore service

        Methods::
           list(str): Retrieves all users of an organization
           team_members(str): Retrieves all members of a team
           project_members(str): Retrieves all users of a project
           add(str): Add a user into a team
           remove(str): Remove a user from a team
    """
    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'users'

    def list(self, user_name: str):
        """Returns all users of an organization

            Args::
                user_name: For which need to find all users

            Returns::
                An array with user objects
        """
        resource = f'orgs/{user_name}/{self._RESOURCE}'
        return self._get(resource=resource)

    def team_members(self, team_id: str):
        """Returns all members of a team by ID

            Args::
                team_id: Team ID for which need to find an users

            Returns::
                An array with member objects
        """
        resource = f'orgs/{team_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def project_members(self, project_id: str):
        """Returns all members of a project

            Args::
                project_id: Project ID for which need to find an users

            Args::
                An array with user objects
        """
        resource = f'projects/{project_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def add(self, team_id: str, user_name: str):
        """Add a user into a team

            Args::
                team_id: ID of a team, in which will be added a user
                user_name: A user which will be added into a team

            Returns::
                A HTTP status code
        """
        resource = f'teams/{team_id}/{self._RESOURCE}/{user_name}'
        return self._post(resource=resource, only_status=True)

    def remove(self, team_id: str, user_name: str):
        """Delete a user from a team

            Args::
                team_id: ID of a team from which will be removed a user
                user_name: A user which will be removed from a team

            Returns::
                A HTTP status code
        """
        resource = f'teams/{team_id}/{self._RESOURCE}/{user_name}'
        return self._delete(resource=resource)


class ProjectsResource(SemaphoreBaseResource):
    """Projects resource class

        Args::
             api_token(str): A authentication token from Semaphore service

        Methods::
            list(str): Retrieve an project objects of an organization
            added_projects(str): Retrieve an projects which will be added to a team
            project_secrets(str): Retrieve an projects based on secrets ID
            create(str, str, str, str): Create a project in an organization
            add_team(str, str): Find a project by ID and added a project into a team
            delete_team(str, str): Remove a project from a team
    """
    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'projects'

    def list(self, user_name: str):
        """Returns an projects of an organization

            Args::
                user_name: Name of an organization
                for which need to retrieve an projects

            Returns::
                An array with project objects
        """
        resource = f'orgs/{user_name}/{self._RESOURCE}'
        return self._get(resource=resource)

    def added_projects(self, team_id: str):
        """Retrieves an projects added to a team

            Args::
                team_id: A team for which will need to find
                added projects

            Returns::
                An array with project objects
        """
        resource = f'teams/{team_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def project_secrets(self, secret_id: str):
        """Retrieves an projects by secrets ID

            Args::
                secret_id: ID of a secret resource

            Returns::
                An array with project objects
        """
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def create(self, user_name: str, name: str, repo_name: str,
               repo_owner, repo_provider: str):
        """
            Args::
                name: of the project on Semaphore
                repo_name: of the repository on GitHub or BitBucket
                repo_owner: of the repository owner on GitHub or BitBucket
                repo_provider: Repository Host

            Returns::
                A project object
        """
        if repo_provider not in ('github', 'bitbucket'):
            raise ValueError('repo_provider must be github or bitbucket')

        data = {
            'name': name,
            'repo_name': repo_name,
            'repo_owner': repo_owner,
            'repo_provider': repo_provider
        }
        resource = f'orgs/{user_name}/projects'
        return self._post(resource=resource, json=data)

    def add_team(self, team_id: str, project_id: str):
        """Add a team to a project

            Args::
                team_id: ID of a team, in which will be added a project
                project_id: ID of a project, which will be added into a team

            Returns::
                A HTTP status code
        """
        resource = f'teams/{team_id}/{self._RESOURCE}/{project_id}'
        return self._post(resource=resource, only_status=True)

    def delete_team(self, team_id: str, project_id: str):
        """Delete a team from a project

            Args::
                team_id: ID of a team, in which will be deleted from a project
                project_id: ID of a project, which will be deleted from a team

            Returns::
                A HTTP status code
       """
        resource = f'teams/{team_id}/{self._RESOURCE}/{project_id}'
        return self._delete(resource=resource)


class SecretsResource(SemaphoreBaseResource):
    """Secrets resource class

           Args::
                api_token(str): A authentication token from Semaphore service

           Methods::
               all(str): Retrieves all secret variables of an organization
               team(str): Retrieves all secret variables which related to a team
               project(str): Retrieves all secret variables which related to a project
               by_id(str): Returns a secret object by ID
               create(str, str, str): Creates a secret object in an organization

               update(str, str, str): Update a secret object by ID
               only `name`, `description` fields
               delete(str): Delete a secret by ID
               attach_to_project(str, str): Attach a secret in a project
               delete_from_team(str, str): Delete a secret from a team
               dettach_from_project(str, str): Dettatach a secret from a project
       """

    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'secrets'

    def all(self, org_username: str):
        """Returns all secret variables of an organization

            Args::
                org_username: Username of an organization, for which need
                to find secret variables

            Returns::
                An array with secret objects
        """
        resource = f'orgs/{org_username}/{self._RESOURCE}'
        return self._get(resource=resource)

    def team(self, team_id: str):
        """Returns secrets variables of a team

            Args::
                team_id: A team for which need to return secret variables

            Returns::
                An array with secret objects
        """
        resource = f'teams/{team_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def project(self, project_id: str):
        """Returns all attached secrets for a project

            Args::
                project_id: ID of a project, for which need to find a secrets
                variables and etc

            Returns::
                An array with secret objects
        """
        resource = f'projects/{project_id}/secrets'
        return self._get(resource=resource)

    def by_id(self, secret_id: str):
        """Returns a secret by ID

            Args::
                secret_id: A secret ID which need to return,
                otherwise 404 HTTP status code

            Returns::
                A object with secret information
        """
        resource = f'{self._RESOURCE}/{secret_id}'
        return self._get(resource=resource)

    def create(self, org_username: str, name: str, description: str=None):
        """Create a secret in an organization

            Args::
                org_username: A name of an organization for which
                will be created a secret
                name: of the secret
                description: for the secret

            Returns::
                A object with secret information
        """
        resource = f'orgs/{org_username}/secrets'
        data = {
            'name': name,
            'description': description
        }
        return self._post(resource=resource, json=data)

    def update(self, secret_id: str, name: str=None, description: str=None):
        """Updates a secret by ID

            Args::
                name: of the secret
                description: for the secrets.

            Returns::
                a dictionary with secret object
        """
        resource = f'{self._RESOURCE}/{secret_id}'
        data = {
            'name': name,
            'description': description
        }
        return self._patch(resource=resource, json=data)

    def delete(self, secret_id: str):
        """Delete a secret by ID

            Args::
                secret_id: ID of a secret which will be deleted

            Returns::
                The 204 HTTP status code
        """
        resource = f'{self._RESOURCE}/{secret_id}'
        return self._delete(resource=resource)

    def attach_to_project(self, project_id: str, secret_id: str):
        """Attaches a secret to a project

            Args::
                project_id: ID of a project for which will be attached a secret
                secret_id: ID of a secret which will be attached to a project

            Returns::
                A dictionary with secret information
        """
        resource = f'projects/{project_id}/secrets/{secret_id}'
        return self._post(resource=resource)

    def delete_from_team(self, team_id: str, secret_id: str):
        """Delete a secret from a team

            Args::
                team_id ID: of a team from which secret will be deleted
                secret_id: ID of a secret which will be deleted from a team

            Returns::
                The 204 HTTP status code
        """
        resource = f'teams/{team_id}/{self._RESOURCE}/{secret_id}'
        return self._delete(resource=resource)

    def dettach_from_project(self, project_id: str, secret_id: str):
        """Dettach a secret from a project

            Args::
                project_id: ID of a project from which will be dettatached secret
                secret_id: ID of a secret which will be dettatached from a project

            Returns::
                The 204 HTTP status code
        """
        resource = f'projects/{project_id}/{self._RESOURCE}/{secret_id}'
        return self._delete(resource=resource)


class EnvironmentResource(SemaphoreBaseResource):
    """Environment resource class

            Args::
                api_token(str): A authentication token from Semaphore service

            Methods::
                all(str): Retrieves all environment variables of a project
                secrets(str): Retrieves all variables belonging to a secret
                by_id(str): Retrieves a environment object by ID
                create(str, str, str, bool): Create environment
                variable within a secret

                update(str, str, str): Update a environment variable by ID
                delete(str): Delete a environment variable by ID
       """

    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'env_vars'

    def all(self, project_id: str):
        """Returns all environment variables which related to a project

            Args::
                project_id: ID of a project for which need to find
                an environment variables

            Returns::
                An array with environment objects
        """
        resource = f'projects/{project_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def secrets(self, secret_id: str):
        """Returns variables belonging to a secret

            Args::
                secret_id: ID of a secret for which need to return
                variables

            Returns::
                An array with secret objects
        """
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def by_id(self, env_var: str):
        """Returns a environment variable by ID

            Args::
                env_var: ID of environment variable which need to find

            Returns::
                A object with variable information
        """
        resource = f'{self._RESOURCE}/{env_var}'
        return self._get(resource=resource)

    def create(self, secret_id: str, name: str, content: str, encrypted: bool=True):
        """Create a environment variable within a secret

            Args::
                secret_id: ID of a secret for which will be created a variable
                name: of the environment variable.
                content: of the environment variable
                encrypted: Encrypt data or not
            Returns::
                A object with variable information
        """
        data = {
            'name': name,
            'content': content,
            'encrypted': encrypted
        }
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        return self._post(resource=resource, json=data)

    def update(self, env_var: str, name: str=None, content: str=None):
        """Updates a environment variable by ID

            Args::
                env_var: ID of a environment variable which will be updated
                name: of the environment variable
                content: of the environment variable

            Returns::
                A object with variable information
        """
        resource = f'env_vars/{env_var}'
        data = {
            'name': name,
            'content': content
        }
        return self._patch(resource=resource, json=data)

    def delete(self, env_var: str):
        """Delete a environment variable by ID

            Args::
                env_var: ID of environment which will be deleted

            Returns::
                The 204 HTTP status code
        """
        resource = f'{self._RESOURCE}/{env_var}'
        return self._delete(resource=resource)


class ConfigurationFileResource(SemaphoreBaseResource):
    """Configuration resource class

            Args::
                api_token(str): A authentication token from Semaphore service

            Methods::
                all(str): Retrieves all configuration files connected to a project
                secrets(str): Retrieves all configuration files
                which related to a secret
                by_id(str): Retrieve a configuration file by ID
                create(str, str, str, str): Create a configuration file
                within a secret
                update(str, str, str): Update a configuration file
                by ID
                delete(str): Delete configuration file by ID
       """

    def __init__(self, api_token):
        super().__init__(api_token)

    _RESOURCE = 'config_files'

    def all(self, project_id: str):
        """Returns all configuration files related to a project

            Args::
                project_id: ID of a project for which need to return
                a configuration file

            Returns::
                A object with configuration information
        """
        resource = f'projects/{project_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def secrets(self, secret_id: str):
        """Returns a configuration files related to a secret

            Args::
                secret_id: ID of a secret for which need
                to find a configuration file

            Returns::
                An array with configuration files
        """
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        return self._get(resource=resource)

    def by_id(self, config_file_id: str):
        """Returns a configuration file by ID

            Args::
                config_file_id: ID of a config file which will be returned

            Returns::
                A object with configuration file
        """
        resource = f'{self._RESOURCE}/{config_file_id}'
        return self._get(resource=resource)

    def create(self, secret_id: str, path: str, content: str, encrypted: bool):
        """Create a configuration file within a secret

            Args::
                secret_id: ID of a secret for which will be created
                a configuration file
                path: of the configuration file
                content: of the configuration file
                will be `null` if the file is encrypted.
                encrypted: `True` if the file is encrypted.

            Returns::
                A object with configuration file
        """
        resource = f'secrets/{secret_id}/{self._RESOURCE}'
        data = {
            'path': path,
            'content': content,
            'encrypted': encrypted
        }
        return self._post(resource=resource, json=data)

    def update(self, config_file_id: str, path: str=None, content: str=None):
        """Update a configuration file by ID

            Args::
                config_file_id: ID of a configuration file
                which will be updated
                path: of the configuration file
                content: of the configuration file
        """
        resource = f'{self._RESOURCE}/{config_file_id}'
        data = {
            'path': path,
            'content': content
        }
        return self._patch(resource=resource, json=data)

    def delete(self, config_file_id: str):
        """Delete a configuration file by ID

            Args::
                config_file_id: ID of a configuration file
                which will be deleted

            Returns::
                The 204 HTTP status code
        """
        resource = f'{self._RESOURCE}/{config_file_id}'
        return self._delete(resource=resource)


class Semaphore(SemaphoreBaseResource):
    """Main wrapper class"""
    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.organization = OrganizationResource(api_token)
        self.teams = TeamResource(api_token)
        self.users = UsersResource(api_token)
        self.projects = ProjectsResource(api_token)
        self.secrets = SecretsResource(api_token)
        self.environment = EnvironmentResource(api_token)
        self.config_files = ConfigurationFileResource(api_token)
