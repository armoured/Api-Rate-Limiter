import time
import pytest
from threading import Thread
ip_v6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'

blocked = []

def send_fast_requests(limiter):
    global blocked
    rate_limiter = limiter(ip_v6, 3, 60)
    # first request for both processes should be accepted
    res = rate_limiter.is_blocked()
    assert(res == False)
    blocked.append(res)
    # second request will be accepted for one process
    # and fail for the other
    # Check after execution
    res = rate_limiter.is_blocked()
    blocked.append(res)


class TestRateLimiterConcurrent:

    @pytest.mark.skip(reason="toggled off")
    def test_fast_concurrent(self, limiter):
        """
        Test concurrency with two threads. Send 4 requests in total. 
        The first two should pass and the last two should have one pass and
        one blocked.
        """    
        global blocked
        p1 = Thread(target=send_fast_requests, args=(limiter, ))
        p2 = Thread(target=send_fast_requests, args=(limiter, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        assert(len(blocked) == 4)
        assert(blocked[0] == False)
        assert(blocked[1] == False)
        # one of the responses must have been blocked
        if blocked[2] == False:
            assert(blocked[3] == True)
        else:
            assert(blocked[3] == False)

        
