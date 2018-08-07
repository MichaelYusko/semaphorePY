from mock import patch

from .base import BaseTestCase


class TestBaseSemaphore(BaseTestCase):

    @patch('semaphore.requests.get')
    def test_default_resources(self, request):
        self.return_assert(request, self.semaphore.default_resources())

    @patch('semaphore.requests.get')
    def test_transform_resources_to_list(self, request):
        self.return_assert(
            request,
            self.semaphore.default_resources(as_list=True)
        )


class TestOrganizationResource(BaseTestCase):
    @patch('semaphore.requests.get')
    def test_organization_list(self, request):
        self.return_assert(request, self.semaphore.organization.list())

    @patch('semaphore.requests.get')
    def test_organization_by_name(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.by_name('test-org')
        )

    @patch('semaphore.requests.get')
    def test_organization_urls(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.urls('mikezz')
        )

    @patch('semaphore.requests.get')
    def test_organization_secret_urls(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.urls('mikezz')
        )

    @patch('semaphore.requests.get')
    def test_organization_users(self, request):
        self.return_assert(
            request,
            self.semaphore.organization.users('mikezz'),
        )


class TestTeamResource(BaseTestCase):
    @patch('semaphore.requests.get')
    def test_team_list(self, request):
        self.return_assert(request, self.semaphore.teams.all('mikezz'))
