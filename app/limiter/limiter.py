import redis
import time

class RateLimiter:
    """
    This rate limiter utilises a fixed window algorithm which allows an api 
    to be rate limited for a specific number of requests in a specific 
    time period. 
    """

    def __init__(self, key, max_reqs, time_limit):
        """
        Initialise the rate limiter with a unique key and the maximum number of requests
        that can be sent to the limiter within a fixed time period specified in seconds.
        """
        self.key = key
        self.max_reqs = max_reqs
        self.time_limit = time_limit 
        # TODO have cache passed in
        self.cache = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def __call__(self, f):
        """
        Allows this class to be used as a decorator to automatically rate limit
        a function reducing the boilerplate required.
        """
        def wrapper(*args):
            if self.is_blocked():
                return "blocked", 429
            f(*args)
        return wrapper
    
    def is_blocked(self):
        """
        Returns true if user is blocked and false if user is not blocked.
        Automatically increments the counter that keeps track of requests 
        each time this function is called. 
        """
        pipeline = self.cache.pipeline()
        pipeline.set(self.key, 0, ex=self.time_limit, nx=True)
        pipeline.incr(self.key)
        count = pipeline.execute()[1]

        if count > self.max_reqs:
            return True

        return False

    def get_blocked_time(self):
        """Returns the time left until the user is no longer blocked in seconds"""
        return max(self.cache.ttl(self.key), 0)
        
        
            

        


    