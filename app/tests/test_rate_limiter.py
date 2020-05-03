import time
import pytest

ip_v6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'


class TestRateLimiterSequential:

    @pytest.mark.skip(reason="toggled off")
    def test_fast_stress(self, limiter):
        """
        Send 200000 requests sequentially.
        """    

        rate_limiter = limiter(ip_v6, 3, 60)
        reqs = 0
        for i in range(0, 250000):
            if rate_limiter.get_blocked_time() < 0:
                reqs = 0
        
            if reqs < 3:
                assert(rate_limiter.is_blocked() == False)
            else:
                assert(rate_limiter.is_blocked() == True)
            reqs += 1

    def test_edge(self, limiter):
        """
        Send three fast requests which get accepted, then wait 4 seconds
        Send a request which should fail, then wait one more second and send
        Three requests which should get accepted
        """    

        rate_limiter = limiter(ip_v6, 3, 5)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(4)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == True)




        
        