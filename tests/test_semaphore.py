from mock import patch

from .base import BaseTestCase


class TestBaseSemaphore(BaseTestCase):

    @patch('semaphore.client.r.get')
    def test_default_resources(self, request):
        self.return_assert(request, self.semaphore.default_resources())

    @patch('semaphore.client.r.get')
    def test_transform_resources_to_list(self, request):
        self.return_assert(
            request,
            self.semaphore.default_resources(as_list=True)
        )


class TestOrganizationResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_organization_list(self, request):
        self.return_assert(request, self.semaphore.organization.list())

    @patch('semaphore.client.r.get')
    def test_organization_by_name(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.by_name('test-org')
        )

    @patch('semaphore.client.r.get')
    def test_organization_urls(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.urls('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_organization_secret_urls(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.urls('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_organization_users(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.users('mikezz'),
        )


class TestTeamResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_team_list(self, request):
        self.return_assert(request, self.semaphore.teams.all('mikezz'))

    @patch('semaphore.client.r.get')
    def test_users_by_project(self, request):
        self.return_assert(
            request,
            self.semaphore.teams.by_project('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_team_secrets(self, request):
        self.return_assert(
            request,
            self.semaphore.teams.secrets('secret id')
        )

    @patch('semaphore.client.r.get')
    def test_get_team_by_id(self, request):
        self.return_assert(
            request,
            self.semaphore.teams.by_id('id')
        )

    @patch('semaphore.client.r.post')
    def test_create_team(self, requests):
        data = {
            'name': 'test name',
            'permission': 'read',
            'description': 'cool description'
        }
        self.return_assert(
            requests,
            self.semaphore.teams.create('id', **data)
        )

    @patch('semaphore.client.r.delete')
    def test_delete_team(self, request):
        return self.return_assert(
            request,
            self.semaphore.teams.delete('id')
        )


class TestUsersResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_list_of_users(self, request):
        self.return_assert(
            request,
            self.semaphore.users.list('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_members_of_team(self, request):
        self.return_assert(
            request,
            self.semaphore.users.team_members('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_members_of_project(self, request):
        self.return_assert(
            request,
            self.semaphore.users.project_members('mikezz')
        )

    @patch('semaphore.client.r.post')
    def test_add_user_to_team(self, request):
        self.return_assert(
            request,
            self.semaphore.users.add('project id', 'user id')
        )

    @patch('semaphore.client.r.delete')
    def test_remove_user_from_team(self, request):
        self.return_assert(
            request,
            self.semaphore.users.remove('project id', 'user id')
        )


class TestProjectsResource(BaseTestCase):
    TEST_DATA = {
        'name': 'name',
        'repo_name': 'repo name',
        'repo_owner': 'repo owner',
        'repo_provider': 'github'
    }

    @patch('semaphore.client.r.get')
    def test_list_of_projects(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.list('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_added_projects(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.added_projects('id')
        )

    @patch('semaphore.client.r.get')
    def test_project_secrets(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.project_secrets('id')
        )

    @patch('semaphore.client.r.post')
    def test_create_project(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.create('mikezz', **self.TEST_DATA)
        )

    @patch('semaphore.client.r.post')
    def test_add_project_for_team(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.add_team('project', 'team')
        )

    @patch('semaphore.client.r.delete')
    def test_delete_project_from_team(self, request):
        self.return_assert(
            request,
            self.semaphore.projects.delete_team('project', 'team')
        )


class TestSecretsResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_all_secrets(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.all('mikezz')
        )

    @patch('semaphore.client.r.get')
    def test_secrets_team(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.team('team id')
        )

    @patch('semaphore.client.r.get')
    def test_secrets_project(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.project('project id')
        )

    @patch('semaphore.client.r.get')
    def test_get_secret_by_id(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.by_id('project id')
        )

    @patch('semaphore.client.r.get')
    def test_create_secret(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.create('org name', 'secret name')
        )

    @patch('semaphore.client.r.patch')
    def test_update_secret(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.update('id of secret', 'update secret name')
        )

    @patch('semaphore.client.r.patch')
    def test_delete_secret(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.delete('secret id')
        )

    @patch('semaphore.client.r.patch')
    def test_attach_secret_to_project(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.attach_to_project('project id', 'secret id')
        )

    @patch('semaphore.client.r.delete')
    def test_delete_from_team(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.delete_from_team('team id', 'secret id')
        )

    @patch('semaphore.client.r.delete')
    def test_dettatach_secret(self, request):
        self.return_assert(
            request,
            self.semaphore.secrets.dettach_from_project('project id', 'secret id')
        )


class TestEnvironmentResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_all_environments(self, request):
        self.return_assert(
            request,
            self.semaphore.environment.all('project id')
        )

    @patch('semaphore.client.r.get')
    def test_secrets_environment(self, request):
        self.return_assert(
            request,
            self.semaphore.environment.secrets('secret id')
        )

    @patch('semaphore.client.r.post')
    def test_create_environment(self, request):
        self.return_assert(
            request,
            self.semaphore.environment.create(
                'secret id',
                'test',
                'test'
            )
        )

    @patch('semaphore.client.r.patch')
    def test_update_environment(self, request):
        self.return_assert(
            request,
            self.semaphore.environment.update(
                'environment id',
                'test two',
                'test two'
            )
        )

    @patch('semaphore.client.r.delete')
    def test_delete_environment(self, request):
        self.return_assert(
            request,
            self.semaphore.environment.delete('variable id')
        )


class TestConfigFileResource(BaseTestCase):
    @patch('semaphore.client.r.get')
    def test_all_files(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.all('project id')
        )

    @patch('semaphore.client.r.get')
    def test_secret_files(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.secrets('secret id')
        )

    @patch('semaphore.client.r.get')
    def test_by_id(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.by_id('config id')
        )

    @patch('semaphore.client.r.post')
    def test_create_file(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.create(
                'secret id',
                'path',
                'content',
                True
            )
        )

    @patch('semaphore.client.r.patch')
    def test_update_file(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.update(
                'config id',
                'update two',
                'update two'
            )
        )

    @patch('semaphore.client.r.patch')
    def test_delete_file(self, request):
        self.return_assert(
            request,
            self.semaphore.config_files.delete('config id')
        )
