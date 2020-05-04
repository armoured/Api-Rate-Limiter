import redis
import time

class RateLimiter:

    def __init__(self, key, max_reqs, time_limit):
        self.key = key
        self.max_reqs = max_reqs
        self.time_limit = time_limit 
        self.cache = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def __call__(self, f):
        def wrapper(*args):
            if self.is_blocked():
                print("You are blocked")
                return
            print("not blocked")
            f(*args)
        return wrapper
    
    def is_blocked(self):
        """
        Returns true if user is blocked and false if user is not blocked
        """
        pipeline = self.cache.pipeline()
        pipeline.set(self.key, 0, ex=self.time_limit, nx=True)
        pipeline.incr(self.key)
        count = pipeline.execute()[1]

        if count > self.max_reqs:
            return True

        return False

    def get_blocked_time(self):
        return max(self.cache.ttl(self.key), 0)
        
        
            

        


    