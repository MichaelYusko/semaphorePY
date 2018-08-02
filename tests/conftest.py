import pytest

from semaphore import Request


@pytest.fixture(scope='session')
def request_client():
    """Fixture of Request class

        Returns:
            A instance of Request class
    """
    return Request()
