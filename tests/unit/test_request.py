import pytest


def test_api_version(request_client):
    """Checks whether request client has a correct API version

        Args::
            request_client Fixture of Request instance
    """
    assert request_client.api_version == '/v2'


def test_base_url(request_client):
    """Checks whether request client has a correct basic URL

        Args::
            request_client Fixture of Request instance
    """
    assert request_client.api_url == 'https://api.semaphoreci.com/v2'


def test_make_url(request_client):
    """Checks whether url build correctly for specific version of API

        Args::
            request_client Fixture of Request instance
    """
    assert request_client.make_url('/v3') == 'https://api.semaphoreci.com/v3'


def test_fails_with_bad_url(request_client):
    """Checks whether make url raises AssertionError
    if an argument wasn't valid

        Args::
            request_client Fixture of Request instance
    """
    with pytest.raises(AssertionError):
        request_client.make_url('1')
