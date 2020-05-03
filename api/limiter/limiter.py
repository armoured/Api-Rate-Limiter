import redis
import time

ONE_MINUTE = 60

class RateLimiter:

    def __init__(self, id, max_reqs):
        self.id = id
        self.max_reqs = max_reqs
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
        pipeline.set(self.id, 0, ex=ONE_MINUTE, nx=True)
        pipeline.incr(self.id)
        results = pipeline.execute()

        count = results[1]
        if count > self.max_reqs:
            return True

        return False
        
        
            

        


    