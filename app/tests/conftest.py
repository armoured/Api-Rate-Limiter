import pytest
from ..limiter.limiter import RateLimiter


@pytest.fixture(scope='function')
def limiter(request): 

    def _method(key, max_reqs, time_limit):
        limiter = RateLimiter(key, max_reqs, time_limit)

        def teardown():
            limiter.cache.delete(key)

        request.addfinalizer(teardown)
        return limiter
    
    return _method