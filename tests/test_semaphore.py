def test_default_resources(semaphore):
    """Checks whether we got basic Semaphore's resources

        Args::
            semaphore Fixture of Semaphore instance
    """
    response = semaphore.default_resources()
    assert isinstance(response, dict)


def test_transform_resources_to_list(semaphore):
    """Checks whether we got a list with resources links

        Args::
            semaphore Fixture of Semaphore instance
    """
    response = semaphore.default_resources(as_list=True)
    assert isinstance(response, list)
