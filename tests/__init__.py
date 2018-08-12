from unittest import TestLoader, TextTestRunner, TestSuite

from .test_request import TestBaseRequest
from .test_semaphore import (
    TestBaseSemaphore,
    TestOrganizationResource,
    TestTeamResource,
    TestUsersResource,
    TestProjectsResource,
    TestSecretsResource,
    TestEnvironmentResource,
    TestConfigFileResource
)


if __name__ == "__main__":
    loader = TestLoader()
    test_classes = (
        TestBaseRequest,
        TestBaseSemaphore,
        TestOrganizationResource,
        TestTeamResource,
        TestUsersResource,
        TestProjectsResource,
        TestSecretsResource,
        TestEnvironmentResource,
        TestConfigFileResource
    )

    tests = [
        loader.loadTestsFromTestCase(test)
        for test in test_classes
    ]

    suite = TestSuite(tests)

    runner = TextTestRunner()
    runner.run(suite)
