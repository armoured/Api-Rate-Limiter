import time
import pytest

ip_v6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'


class TestRateLimiterSequential:

    # @pytest.mark.skip(reason="toggled off")
    def test_fast_stress(self, limiter):
        """
        Send 250000 requests sequentially.
        """    

        rate_limiter = limiter(ip_v6, 3, 60)
        reqs = 0
        for i in range(0, 250000):
            if rate_limiter.get_blocked_time() == 0:
                reqs = 0
                time.sleep(1) # make sure the key expires
        
            if reqs < 3:
                assert(rate_limiter.is_blocked() == False)
            else:
                assert(rate_limiter.is_blocked() == True)
            reqs += 1

    # @pytest.mark.skip(reason="toggled off")
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

    # @pytest.mark.skip(reason="toggled off")
    def test_blocked_time(self, limiter):
        """
        Send three fast requests and check blocked time is 3 seconds
        Then check blocked time reduces every second until no longer blocked
        """
        rate_limiter = limiter(ip_v6, 3, 3)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.get_blocked_time() == 3)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.get_blocked_time() == 2)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.get_blocked_time() == 1)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.get_blocked_time() == 0)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.get_blocked_time() == 3)

    # @pytest.mark.skip(reason="toggled off")
    def test_one_request_per_second(self, limiter):
        """
        Send one request per second with a maximum of 1 requests every 1 second.
        Should pass
        """
        rate_limiter = limiter(ip_v6, 1, 1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)


    #@pytest.mark.skip(reason="toggled off")
    def test_two_request_one_second(self, limiter):
        """
        Send two request in 1 seconds with a maximum of 1 request every 1 second.
        Should block second request
        """
        rate_limiter = limiter(ip_v6, 1, 1)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == True)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(1)
        assert(rate_limiter.is_blocked() == False)

    #@pytest.mark.skip(reason="toggled off")
    def test_double_requests_end_start(self, limiter):
        """
        With a fixed window algorithm, it is possible to send 2n requests
        within a certain time period. For example, set max requests to 2 for
        a fixed time period of 1 second. after 0.5 seconds send two fast requests. 
        Then after 1 second send another two fast requests before 1.5 seconds. 
        We should have sent 4 requests in a rolling window of 1 second (1.5-0.5 seconds)
        thus breaking the rule of a maximum of 2 requests in 1 second.

        This is a known limitation of the fixed window algorithm. 
        """
        # my implementation requires us to have 1 call initially
        # to start the timer, so we must make the make max requests 3 instead of 2
        # to account for this starting request.
        rate_limiter = limiter(ip_v6, 3, 1)
        assert(rate_limiter.is_blocked() == False)

        time.sleep(0.5) # 0.5 seconds now
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)
        time.sleep(0.6) # 1.1 seconds now
        # requests are unblocked now as it has been more than 1 second since the
        # first request.
        assert(rate_limiter.is_blocked() == False)
        assert(rate_limiter.is_blocked() == False)

        # we've sent 4 requests in (1.1 - 0.5) = 0.6 seconds
        # which is currently greater than the maximum number of 3 requests.









        





        
        