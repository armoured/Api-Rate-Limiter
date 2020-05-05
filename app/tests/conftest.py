import pytest
from ..limiter.limiter import RateLimiter


@pytest.fixture(scope='function')
def limiter(request): 
    """
    Pytest fixture that returns a callable method to init and tear down
    an instance of the rate limiter
    """

    def _method(key, max_reqs, time_limit):
        """
        Initialise the rate limiter and return it to the caller.
        When the caller exits, teardown is initiated on the rate limiter.
        """
        limiter = RateLimiter(key, max_reqs, time_limit)

        def teardown():
            limiter.cache.delete(key)

        request.addfinalizer(teardown)
        return limiter
    
    return _method