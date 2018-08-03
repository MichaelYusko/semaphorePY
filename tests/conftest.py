import pytest

from semaphore import BaseRequest, Semaphore


@pytest.fixture(scope='session')
def request_client():
    """Fixture of Request class

        Returns:
            A instance of Request class
    """
    return BaseRequest('Api-token')


@pytest.fixture(scope='session')
def semaphore():
    return Semaphore('Api-Token')
